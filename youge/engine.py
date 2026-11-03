"""Pure, deterministic scoring and evidence-bound reporting for 游格 v0.2."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "youge.v0.2.0.json"


class InputError(ValueError):
    """The response cannot be interpreted without silently changing its meaning."""


def load_config(path: str | Path = DEFAULT_CONFIG) -> dict:
    with Path(path).open(encoding="utf-8-sig") as stream:
        config = json.load(stream)
    validate_config(config)
    return config


def _index(items, key="id"):
    return {item[key]: item for item in items}


def _numeric(value):
    return type(value) in (int, float)


def _fact_paths(condition):
    if "fact" in condition:
        yield condition["fact"]
    for key in ("all", "any"):
        for child in condition.get(key, []):
            yield from _fact_paths(child)
    if "not" in condition:
        yield from _fact_paths(condition["not"])


def validate_config(config):
    dims = config["dimensions"]
    questions = config["core_questions"]
    followups = config["followup_questions"]
    dim_ids = [d["id"] for d in dims]
    ids = [q["id"] for q in questions + followups]
    if len(dims) != 8 or len(questions) != 32 or len(followups) != 12:
        raise InputError("v0.2必须包含八维、32道核心题和12道条件追问。")
    if len(set(ids)) != len(ids) or len(set(dim_ids)) != 8:
        raise InputError("题号和维度ID必须唯一。")
    if sorted(q["display_order"] for q in questions) != list(range(1, 33)):
        raise InputError("核心题序必须完整覆盖1—32。")
    for dim in dims:
        actual = [q["id"] for q in questions if q["dimension"] == dim["id"]]
        if actual != dim["question_ids"] or len(actual) != 4:
            raise InputError("每维必须恰有四题，维度题号必须一致。")
    for q in questions:
        if q["dimension"] not in dim_ids or not q["scored"] or q["weight"] != 1:
            raise InputError("核心题只能等权计入一个已声明维度。")
        if q["score_map"] != {str(i): i for i in range(1, 6)}:
            raise InputError("核心题必须使用同一五点评分映射。")
    if config["manifest"]["allowed_score_inputs"] != ["core"]:
        raise InputError("计分输入只能是core。")
    for q in followups:
        if q["scored"] or q["dimension"] is not None:
            raise InputError("条件追问不得计入八维。")
        if q["gate"]["module"] != q["module"]:
            raise InputError("追问模块与适用性入口不一致。")
        if "depends_on" in q and q["depends_on"]["question_id"] not in ids:
            raise InputError("追问引用了不存在的前置题。")
    rule_ids = [r["id"] for r in config["report_rules"]]
    if len(set(rule_ids)) != len(rule_ids):
        raise InputError("文案规则ID必须唯一。")
    for rule in config["report_rules"]:
        if not rule["evidence"]:
            raise InputError("具体判断必须声明证据。")
        for path in _fact_paths(rule["condition"]):
            parts = path.split(".")
            if parts[0] in ("scores", "positive_counts") and parts[1] not in dim_ids:
                raise InputError("文案条件引用了不存在的维度。")
            if parts[0] == "followups" and parts[1] not in ids:
                raise InputError("文案条件引用了不存在的题目。")
        for selector in rule["evidence"]:
            if selector["kind"] in ("dimension", "positive_core") and selector["dimension"] not in dim_ids:
                raise InputError("证据引用了不存在的维度。")
            if selector["kind"] == "answer" and selector["id"] not in ids:
                raise InputError("证据引用了不存在的题目。")
    return True


def _validate_core(core, config):
    if not isinstance(core, dict):
        raise InputError("core必须是题号到答案的对象。")
    known = {q["id"] for q in config["core_questions"]}
    if set(core) - known:
        raise InputError(f"未知核心题号：{sorted(set(core) - known)}")
    for qid, value in core.items():
        if value is not None and (type(value) is not int or not 1 <= value <= 5):
            raise InputError(f"{qid}必须是1—5的整数或null；缺失不能用0代替。")


def _exact_score(row):
    if row["score"] is None:
        return None
    return Fraction(25) * (Fraction(row["sum"], row["valid_n"]) - 1)


def score_core(core: dict, config: dict) -> dict:
    """Only accepts core answers: taste and followups cannot enter this function."""
    _validate_core(core, config)
    result = {}
    minimum = config["display_rules"]["min_valid_per_dimension"]
    for dim in config["dimensions"]:
        answered = {qid: core.get(qid) for qid in dim["question_ids"]}
        valid = [value for value in answered.values() if value is not None]
        enough = len(valid) >= minimum
        exact = Fraction(25) * (Fraction(sum(valid), len(valid)) - 1) if enough else None
        result[dim["id"]] = {
            "name": dim["name"], "answers": answered, "valid_n": len(valid),
            "sum": sum(valid), "mean": sum(valid) / len(valid) if valid else None,
            "score": float(exact) if exact is not None else None,
            "display_score": float(Decimal(str(float(exact))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)) if exact is not None else None,
            "positive_n": sum(v >= config["display_rules"]["positive_value"] for v in valid),
            "status": "scored" if enough else "insufficient",
        }
    return result


def classify_profile(scores: dict, config: dict) -> dict:
    """Classifies with exact fractions, before display rounding or sensitivity handling."""
    order = [d["id"] for d in config["dimensions"]]
    rules = config["display_rules"]
    values = {d: _exact_score(scores[d]) for d in order}
    if any(v is None for v in values.values()):
        return {"category": "partial", "primary": [], "secondary": [], "leading": []}
    if all(v >= Fraction(str(rules["all_high_threshold"])) for v in values.values()):
        return {"category": "all_high", "primary": [], "secondary": [], "leading": order}
    if all(v <= Fraction(str(rules["all_low_threshold"])) for v in values.values()):
        return {"category": "all_low", "primary": [], "secondary": [], "leading": []}
    threshold = Fraction(str(rules["preference_threshold"]))
    peak = max(values.values())
    if peak < threshold:
        return {"category": "no_clear", "primary": [], "secondary": [], "leading": []}
    gap = Fraction(str(rules["leading_gap"]))
    leading = [d for d in order if values[d] >= threshold and peak - values[d] <= gap]
    if len(leading) >= 3:
        return {"category": "multi", "primary": [], "secondary": [], "leading": leading}
    if len(leading) == 2:
        return {"category": "dual", "primary": leading, "secondary": [], "leading": leading}
    others = [d for d in order if d not in leading and values[d] >= threshold]
    second_max = max((values[d] for d in others), default=None)
    secondary = [d for d in others if values[d] == second_max]
    return {"category": "single", "primary": leading, "secondary": secondary, "leading": leading}


def _primary_signature(classification):
    return classification["category"], tuple(classification["primary"]), tuple(classification["leading"])


def sensitivity_check(core: dict, config: dict, baseline=None) -> dict:
    _validate_core(core, config)
    baseline = baseline or classify_profile(score_core(core, config), config)
    cases = []
    secondary_candidates = set(baseline["secondary"])
    for q in sorted(config["core_questions"], key=lambda x: x["display_order"]):
        qid, value = q["id"], core.get(q["id"])
        if value is None:
            continue
        for delta in (-1, 1):
            changed_value = value + delta
            if not 1 <= changed_value <= 5:
                continue
            perturbed = dict(core)
            perturbed[qid] = changed_value
            classification = classify_profile(score_core(perturbed, config), config)
            secondary_candidates.update(classification["secondary"])
            primary_change = _primary_signature(classification) != _primary_signature(baseline)
            secondary_change = classification["secondary"] != baseline["secondary"]
            cases.append({"question_id": qid, "from": value, "to": changed_value,
                          "primary_changed": primary_change, "secondary_changed": secondary_change,
                          "category_changed": classification["category"] != baseline["category"],
                          "result": classification})
    applicable = baseline["category"] != "partial" and bool(cases)
    return {
        "method": "each_valid_answer_plus_or_minus_one", "tested_changes": len(cases),
        "applicable": applicable,
        "primary_stable": not any(c["primary_changed"] for c in cases) if applicable else None,
        "secondary_stable": not any(c["secondary_changed"] for c in cases) if applicable else None,
        "category_stable": not any(c["category_changed"] for c in cases) if applicable else None,
        "secondary_candidates": [d["id"] for d in config["dimensions"] if d["id"] in secondary_candidates],
        "changes": [c for c in cases if c["primary_changed"] or c["secondary_changed"] or c["category_changed"]],
        "interpretation": "仅检查称号对单题小幅变化的敏感性，不是准确率、置信度或重测概率。",
    }


def _name_key(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def _normalize_game(item, config, *, negative=False):
    if not isinstance(item, dict) or not isinstance(item.get("title"), str) or not item["title"].strip():
        raise InputError("作品必须包含非空名称title。")
    result = deepcopy(item)
    result["title"] = result["title"].strip()
    catalog = _index(config["game_catalog"])
    aliases = {_name_key(alias): game for game in catalog.values() for alias in [game["title"], *game["aliases"]]}
    specified_id = item.get("game_id")
    if specified_id is not None and (not isinstance(specified_id, str) or not specified_id):
        raise InputError("作品ID必须是非空字符串。")
    known = catalog.get(specified_id) if specified_id else aliases.get(_name_key(item["title"]))
    named_game = aliases.get(_name_key(item["title"]))
    if known and named_game and known["id"] != named_game["id"]:
        raise InputError("作品名称与已指定的作品ID对应不同作品，请先确认。")
    if specified_id and not known and not specified_id.startswith("custom:"):
        raise InputError(f"作品ID {specified_id} 不在字典中；未知作品应保留名称或使用custom: ID。")
    if known:
        result.update(game_id=known["id"], title=known["title"], series_id=known["series_id"])
        result["edition"] = item.get("edition", known["edition"])
        result["identity_status"] = "catalog"
    else:
        generated = "custom:" + sha256(_name_key(item["title"]).encode()).hexdigest()[:16]
        result.update(game_id=specified_id or generated, series_id=None,
                      edition=item.get("edition", "unspecified"), identity_status="self_entered")
    if not isinstance(result["edition"], str) or not result["edition"].strip():
        raise InputError("作品版本edition必须是非空字符串。")
    if item.get("experience") not in {"yes", "no", "unknown"}:
        raise InputError("每款作品必须明确experience为yes、no或unknown。")
    result.setdefault("note", "")
    if not isinstance(result["note"], str):
        raise InputError("作品补充原话必须是字符串。")
    if negative:
        if item["experience"] != "yes":
            raise InputError("没有喜欢起来的可选作品必须亲自体验过。")
        reasons = item.get("reasons", [])
        allowed = {x["value"] for x in config["taste"]["negative_reasons"]}
        if not isinstance(reasons, list) or not reasons or any(not isinstance(x, str) for x in reasons) or len(reasons) > config["taste"]["negative_max_reasons"] or len(set(reasons)) != len(reasons) or set(reasons) - allowed:
            raise InputError("未喜欢作品需提供1—2项有效且不重复的原因。")
        result["reasons"] = reasons
    else:
        attractions = item.get("attractions", [])
        allowed = {x["id"] for x in config["taste"]["attractions"]}
        if not isinstance(attractions, list) or any(not isinstance(x, str) for x in attractions) or len(attractions) > config["taste"]["max_attractions_per_game"] or len(set(attractions)) != len(attractions) or set(attractions) - allowed:
            raise InputError("每款喜欢作品最多选择两项有效且不重复的吸引点。")
        result["attractions"] = attractions
    return result


def _validate_selection(value, question):
    allowed = {o["value"] for o in question["options"]}
    kind = question["response_type"]
    if kind == "single":
        if not isinstance(value, str) or value not in allowed:
            raise InputError(f"{question['id']}含无效选项。")
        return value
    values = value.get("purposes") if kind == "multi_with_basis" and isinstance(value, dict) else value
    if not isinstance(values, list) or not values or any(not isinstance(x, str) for x in values) or len(set(values)) != len(values) or set(values) - allowed or len(values) > question.get("max_selections", len(allowed)):
        raise InputError(f"{question['id']}需要有效、不重复且不超上限的多选答案。")
    exclusive = set(question.get("exclusive_options", []))
    if exclusive.intersection(values) and len(values) > 1:
        raise InputError(f"{question['id']}的独占选项不能和其他选项并选。")
    order = [o["value"] for o in question["options"]]
    values = sorted(values, key=order.index)
    if kind == "multi_with_basis":
        if value.get("basis") not in {o["value"] for o in question["basis_options"]}:
            raise InputError("Mod用途必须区分实际使用与假设意愿。")
        return {"basis": value["basis"], "purposes": values}
    return values


def normalize_response(response: dict, config: dict) -> dict:
    if not isinstance(response, dict):
        raise InputError("答卷必须是对象。")
    if response.get("versions") != config["manifest"]["versions"]:
        raise InputError("答卷版本与当前配置不一致；需显式选择原版本或提供兼容映射。")
    core = response.get("core", {})
    _validate_core(core, config)
    result = deepcopy(response)
    result["core"] = {q["id"]: core.get(q["id"]) for q in config["core_questions"]}
    reasons = result.setdefault("core_missing_reasons", {})
    if not isinstance(reasons, dict):
        raise InputError("核心题缺失原因必须是对象。")
    allowed_missing = {x["value"] for x in config["answer_scale"]["missing_reasons"]}
    for qid, reason in reasons.items():
        if qid not in result["core"] or result["core"][qid] is not None or reason not in allowed_missing:
            raise InputError("缺失原因只能用于真实缺失的核心题，且须使用已声明原因。")
    result.setdefault("respondent_id", "anonymous")
    result.setdefault("display_name", result["respondent_id"])
    result.setdefault("fictional", False)
    favorites = result.get("favorites", [])
    if not isinstance(favorites, list):
        raise InputError("favorites必须是列表。")
    normalized = []
    existing = {}
    for item in favorites:
        game = _normalize_game(item, config)
        key = (game["game_id"], game["edition"])
        if key not in existing:
            existing[key] = game
            normalized.append(game)
            continue
        previous = existing[key]
        if previous["experience"] != game["experience"]:
            raise InputError("重复作品的亲玩状态不同，请确认后再合并。")
        combined = list(dict.fromkeys(previous["attractions"] + game["attractions"]))
        if len(combined) > config["taste"]["max_attractions_per_game"]:
            raise InputError("重复作品合并后超过两项吸引点，请先确认保留哪两项。")
        previous["attractions"] = combined
        previous["note"] = " / ".join(dict.fromkeys(x for x in (previous["note"], game["note"]) if x))
    if len(normalized) > config["taste"]["max_games"]:
        raise InputError("最多填写五款不同喜欢作品。")
    attraction_order = [x["id"] for x in config["taste"]["attractions"]]
    for game in normalized:
        game["attractions"].sort(key=attraction_order.index)
    result["favorites"] = normalized
    negative = result.get("disliked")
    result["disliked"] = _normalize_game(negative, config, negative=True) if negative is not None else None
    if negative is not None and any((g["game_id"], g["edition"]) == (result["disliked"]["game_id"], result["disliked"]["edition"]) for g in normalized):
        raise InputError("同一版本作品不能同时标为喜欢与没有喜欢起来；请在补充原话中说明复杂体验。")
    supplement = result.get("supplement", [])
    if not isinstance(supplement, list):
        raise InputError("补充体验清单必须是列表；跳过时使用空列表。")
    supplement_q = {"id": "X01", "response_type": "multi", "options": config["supplement"]["options"]}
    result["supplement"] = _validate_selection(supplement, supplement_q) if supplement else []
    backgrounds = result.get("background", {})
    if not isinstance(backgrounds, dict) or set(backgrounds) - {q["id"] for q in config["background_questions"]}:
        raise InputError("背景题号无效。")
    result["background"] = {}
    for q in config["background_questions"]:
        value = backgrounds.get(q["id"])
        if value:
            result["background"][q["id"]] = _validate_selection(value, q)
    applicability = result.get("applicability", {})
    modules = config["branch_applicability"]["modules"]
    statuses = {x["value"] for x in config["branch_applicability"]["statuses"]}
    if not isinstance(applicability, dict) or set(applicability) - set(modules) or any(s not in statuses | {"not_provided"} for s in applicability.values()):
        raise InputError("模块适用性须明确区分适用、缺乏经历、不适用和跳过。")
    result["applicability"] = {m: applicability.get(m, "not_provided") for m in modules}
    followups = result.get("followups", {})
    qindex = _index(config["followup_questions"])
    if not isinstance(followups, dict) or set(followups) - set(qindex):
        raise InputError("条件追问题号无效。")
    result["followups"] = {}
    for q in config["followup_questions"]:
        value = followups.get(q["id"])
        if value is None:
            continue
        if result["applicability"][q["module"]] != "applicable":
            raise InputError(f"{q['id']}尚未声明适用，不能使用隐藏或未触发的答案。")
        dependency = q.get("depends_on")
        if dependency and result["followups"].get(dependency["question_id"]) not in dependency["accepted"]:
            raise InputError(f"{q['id']}前置条件未满足。")
        normalized_value = _validate_selection(value, q)
        if q["id"] == "R02":
            intention = result["followups"]["R01"]
            forbidden = q["option_groups"]["negative" if intention in ("willing", "conditional") else "positive"]
            if set(normalized_value).intersection(forbidden):
                raise InputError("二刷原因应与当前意愿分支相符；复杂变化请写补充原话。")
        if q["id"] == "M02" and normalized_value["basis"] == "actual" and result["followups"]["M01"] != "actual_use":
            raise InputError("没有实际使用经历时，Mod用途只能标为假设意愿。")
        result["followups"][q["id"]] = normalized_value
    result["branch_status"] = {}
    for q in config["followup_questions"]:
        module_status = result["applicability"][q["module"]]
        dependency = q.get("depends_on")
        if module_status != "applicable":
            state = module_status
        elif dependency and result["followups"].get(dependency["question_id"]) not in dependency["accepted"]:
            state = "not_triggered"
        elif q["id"] in result["followups"]:
            state = "answered"
        else:
            state = "unanswered"
        result["branch_status"][q["id"]] = state
    return result


def _label_answer(question, value):
    labels = {o["value"]: o["label"] for o in question["options"]}
    if isinstance(value, dict):
        basis = {o["value"]: o["label"] for o in question["basis_options"]}[value["basis"]]
        return basis + "：" + "、".join(labels[v] for v in value["purposes"])
    if isinstance(value, list):
        return "、".join(labels[v] for v in value)
    return labels[value]


def _evidence_registry(response, scores, config):
    evidence = {}
    scale = {x["value"]: x["label"] for x in config["answer_scale"]["options"]}
    for q in config["core_questions"]:
        value = response["core"][q["id"]]
        item_labels = {x["value"]: x["label"] for x in q.get("response_options", [])} or scale
        evidence[f"answer:{q['id']}"] = {
            "source": "core", "question_id": q["id"], "question": q["text"],
            "context": q["context"], "value": value,
            "label": item_labels[value] if value is not None else "无法判断／不适用或未回答",
            "missing_reason": response["core_missing_reasons"].get(q["id"]),
            "scope": "通常的游戏偏好",
        }
    for d in config["dimensions"]:
        row = scores[d["id"]]
        evidence[f"score:{d['id']}"] = {
            "source": "dimension", "dimension": d["id"], "name": d["name"],
            "score": row["score"], "valid_n": row["valid_n"], "sum": row["sum"],
            "formula": "25 × (有效题平均分 − 1)",
            "answer_refs": [f"answer:{qid}" for qid in d["question_ids"]],
            "scope": "问卷偏好分，不是百分位或能力分",
        }
    for q in config["followup_questions"]:
        if q["id"] in response["followups"]:
            value = response["followups"][q["id"]]
            evidence[f"answer:{q['id']}"] = {
                "source": "followup", "question_id": q["id"], "question": q["text"],
                "value": value, "label": _label_answer(q, value),
                "scope": "特定行为或条件，不计入八维",
            }
    attractions = _index(config["taste"]["attractions"])
    for i, game in enumerate(response["favorites"]):
        evidence[f"favorite:{i}"] = {
            "source": "favorite", "game_id": game["game_id"], "title": game["title"],
            "edition": game["edition"], "experience": game["experience"],
            "attractions": game["attractions"], "scope": "喜欢作品的明确自述，不计入八维",
        }
        for tag in game["attractions"]:
            evidence[f"favorite:{i}:{tag}"] = {
                "source": "attraction", "game_id": game["game_id"], "title": game["title"],
                "experience": game["experience"], "value": tag,
                "label": attractions[tag]["label"], "scope": "作品吸引点的自述，不验证模型",
            }
    negative = response["disliked"]
    if negative:
        labels = {x["value"]: x["label"] for x in config["taste"]["negative_reasons"]}
        for reason in negative["reasons"]:
            evidence[f"negative:{reason}"] = {
                "source": "negative_game", "title": negative["title"], "experience": "yes",
                "value": reason, "label": labels[reason], "scope": "该作品的体验，不能泛化为对所有同类内容的厌恶",
            }
    labels = {x["value"]: x["label"] for x in config["supplement"]["options"]}
    for tag in response["supplement"]:
        evidence[f"supplement:{tag}"] = {"source": "supplement", "value": tag, "label": labels[tag], "scope": "补充体验，不计入八维"}
    return evidence


def _get_path(data, path):
    current = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _condition(condition, facts):
    if "all" in condition:
        return all(_condition(c, facts) for c in condition["all"])
    if "any" in condition:
        return any(_condition(c, facts) for c in condition["any"])
    if "not" in condition:
        return not _condition(condition["not"], facts)
    value = _get_path(facts, condition["fact"])
    expected, op = condition["value"], condition["op"]
    if op == "exists":
        return (value is not None) == expected
    if value is None:
        return False
    if op == "eq":
        return value == expected
    if op == "in":
        return value in expected
    if op == "contains":
        return isinstance(value, list) and expected in value
    if op == "gte":
        return _numeric(value) and value >= expected
    if op == "lte":
        return _numeric(value) and value <= expected
    raise InputError(f"未声明的条件运算：{op}")


def _resolve_evidence(selectors, response, config):
    refs = []
    dims = _index(config["dimensions"])
    for selector in selectors:
        if selector["kind"] == "answer":
            if selector["id"] not in response["followups"] and response["core"].get(selector["id"]) is None:
                return []
            refs.append(f"answer:{selector['id']}")
        elif selector["kind"] == "dimension":
            refs.append(f"score:{selector['dimension']}")
        elif selector["kind"] == "positive_core":
            ids = [qid for qid in dims[selector["dimension"]]["question_ids"]
                   if response["core"].get(qid) is not None and response["core"][qid] >= selector["min_value"]]
            if len(ids) < selector["minimum"]:
                return []
            refs.extend(f"answer:{qid}" for qid in ids)
    return list(dict.fromkeys(refs))


def _rule_claims(section, response, scores, evidence, config):
    facts = {"scores": {d: row["score"] for d, row in scores.items()},
             "positive_counts": {d: row["positive_n"] for d, row in scores.items()},
             "followups": response["followups"]}
    selected, groups, covered = [], set(), set()
    for rule in sorted(config["report_rules"], key=lambda r: (-r["priority"], r["id"])):
        if rule["section"] != section or not _condition(rule["condition"], facts):
            continue
        if rule.get("dedup_group") in groups:
            continue
        dimensions = set(rule.get("covered_dimensions", []))
        if section == "insight" and dimensions and dimensions.issubset(covered):
            continue
        refs = _resolve_evidence(rule["evidence"], response, config)
        if not refs or any(ref not in evidence for ref in refs):
            continue
        selected.append({"rule_id": rule["id"], "text": rule["text"], "evidence_refs": refs,
                         "condition_snapshot": {path: _get_path(facts, path) for path in _fact_paths(rule["condition"])},
                         "scope": "现实习惯自我核对问题，不作结论" if section == "self_check" else "本次问卷的游戏偏好与具体行为"})
        groups.add(rule.get("dedup_group"))
        covered.update(dimensions)
    limits = {"insight": "max_insights", "tag": "max_behavior_tags", "self_check": "max_self_checks"}
    if section in limits:
        selected = selected[:config["display_rules"][limits[section]]]
    return selected


def _profile_display(classification, sensitivity, scores, config):
    dims = _index(config["dimensions"])
    templates = config["system_templates"]
    category = classification["category"]
    primary = classification["primary"][:]
    secondary = classification["secondary"][:]
    secondary_candidates = []
    lines = []
    if category in ("partial", "all_high", "all_low", "no_clear"):
        title = templates["profile_labels"][category]
        one_line = templates["profile_explanations"][category]
        primary, secondary = [], []
    elif not sensitivity["primary_stable"]:
        title = templates["profile_labels"]["sensitive"]
        one_line = templates["profile_explanations"]["sensitive"]
        primary, secondary = [], []
    elif category == "single":
        title = dims[primary[0]]["archetype"]["name"]
        one_line = dims[primary[0]]["archetype"]["one_line"]
        if not sensitivity["secondary_stable"]:
            secondary_candidates = [d for d in sensitivity["secondary_candidates"]
                                    if scores[d]["score"] is not None and scores[d]["score"] >= config["display_rules"]["preference_threshold"]]
            secondary = []
            lines.append(templates["secondary_sensitive"])
    elif category == "dual":
        title = " ＋ ".join(dims[d]["archetype"]["name"] for d in primary)
        one_line = templates["profile_explanations"]["dual"]
    else:
        title = templates["profile_labels"]["multi"]
        one_line = templates["profile_explanations"]["multi"]
    refs = [f"score:{d['id']}" for d in config["dimensions"]]
    return {"title": title, "one_line": one_line, "category": category,
            "primary_dimensions": primary, "secondary_dimensions": secondary,
            "secondary_names": [dims[d]["archetype"]["name"] for d in secondary],
            "secondary_candidate_dimensions": secondary_candidates,
            "secondary_candidate_names": [dims[d]["archetype"]["name"] for d in secondary_candidates],
            "notes": lines, "evidence_refs": refs, "rule_id": "DISPLAY_" + category.upper(),
            "condition_snapshot": {"classification": classification, "primary_stable": sensitivity["primary_stable"],
                                   "secondary_stable": sensitivity["secondary_stable"], "display_rules": config["display_rules"]},
            "scope": "连续画像的展示摘要，阈值未经过真实样本验证"}


def _taste_report(response, scores, config):
    games = response["favorites"]
    templates = config["system_templates"]
    tag_index = _index(config["taste"]["attractions"])
    claims, alignment = [], []
    groups = [("played", [i for i, g in enumerate(games) if g["experience"] == "yes"]),
              ("anticipated", [i for i, g in enumerate(games) if g["experience"] != "yes"])]
    for group_name, indices in groups:
        repeated = False
        for tag in config["taste"]["attractions"]:
            if tag["id"] == "other":
                continue
            selected_all = [i for i in indices if tag["id"] in games[i]["attractions"]]
            seen_work_ids = set()
            selected = []
            for i in selected_all:
                if games[i]["game_id"] not in seen_work_ids:
                    selected.append(i)
                    seen_work_ids.add(games[i]["game_id"])
            if len(selected) < 2:
                continue
            repeated = True
            titles = "、".join(f"《{games[i]['title']}》" for i in selected)
            refs = [f"favorite:{i}:{tag['id']}" for i in selected]
            text = templates["taste_repeat_" + group_name].format(titles=titles, attraction=tag["label"])
            series = {games[i]["series_id"] for i in selected}
            same_series = len(series) == 1 and None not in series
            if same_series:
                text += templates["taste_same_series"]
            claims.append({"rule_id": "T_REPEAT_" + group_name.upper(), "text": text,
                           "evidence_refs": refs, "condition_snapshot": {"distinct_games": len(selected), "attraction": tag["id"], "same_series": same_series},
                           "scope": "作品吸引点的重复自述，不验证八维模型"})
            dim = tag["report_dimension"]
            if group_name == "played" and dim and scores[dim]["score"] is not None:
                score = scores[dim]["score"]
                if score >= config["display_rules"]["all_high_threshold"]:
                    text = templates["taste_echo"].format(attraction=tag["label"], dimension=scores[dim]["name"])
                    code = "T_ECHO"
                elif score <= config["display_rules"]["all_low_threshold"]:
                    text = templates["taste_difference"].format(attraction=tag["label"], dimension=scores[dim]["name"])
                    code = "T_DIFFERENCE"
                else:
                    continue
                alignment.append({"rule_id": code, "text": text, "evidence_refs": refs + [f"score:{dim}"],
                                  "condition_snapshot": {"distinct_games": len(selected), "score": score},
                                  "scope": "并列解释两份自述，不能作为模型有效性证据"})
        if not repeated:
            for i in indices:
                labels = [tag_index[t]["label"] for t in games[i]["attractions"]]
                if not labels:
                    continue
                claims.append({"rule_id": "T_SINGLE_" + group_name.upper(),
                               "text": templates["taste_single_" + group_name].format(title=games[i]["title"], attractions="、".join(labels)),
                               "evidence_refs": [f"favorite:{i}:{t}" for t in games[i]["attractions"]],
                               "condition_snapshot": {"repeated_tag_found": False}, "scope": "仅解释点名作品，不推断共同口味"})
    if not games:
        note = templates["taste_empty"]
    elif not claims:
        note = templates["taste_no_attractions"]
    elif len(games) >= 2 and not any(c["rule_id"].startswith("T_REPEAT") for c in claims):
        note = templates["taste_varied"]
    else:
        note = templates["taste_scope"]
    free_text = [{"title": g["title"], "text": g["note"], "policy": "玩家原话；未解析为计分或人格证据"} for g in games if g["note"]]
    if response["disliked"] and response["disliked"]["note"]:
        free_text.append({"title": response["disliked"]["title"], "text": response["disliked"]["note"], "policy": "未喜欢作品的原话；仅用于该作品"})
    return {"claims": claims, "alignment": alignment, "note": note, "free_text": free_text}


def _advice(response, config):
    result = []
    for topic in config["advice_topics"]:
        qid = topic["question_id"]
        value = response["followups"].get(qid)
        known = value is not None and value != "uncertain"
        text = topic["fallback"]
        if known and topic["by_answer"]:
            text = topic["by_answer"].get(value, text)
        elif known and topic["id"] == "guide":
            text = config["system_templates"]["guide_advice"].format(
                purposes=_label_answer(_index(config["followup_questions"])[qid], value))
        refs = [f"answer:{qid}"] if known else []
        if topic["id"] == "mod" and "M02" in response["followups"]:
            q = _index(config["followup_questions"])["M02"]
            text += " " + config["system_templates"]["mod_advice"].format(purposes=_label_answer(q, response["followups"]["M02"]))
            refs.append("answer:M02")
        result.append({"topic": topic["id"], "title": topic["title"], "text": text,
                       "basis": "explicit_answer" if known else "needs_confirmation",
                       "kind": "suggestion", "evidence_refs": refs,
                       "rule_id": "ADVICE_" + topic["id"].upper(),
                       "condition_snapshot": {"answer": value, "branch_status": response["branch_status"][qid]},
                       "scope": "同游安排建议；未回答时不声称知道玩家偏好"})
    return result


def build_report(response: dict, config: dict) -> dict:
    normalized = normalize_response(response, config)
    scores = score_core(normalized["core"], config)
    classification = classify_profile(scores, config)
    sensitivity = sensitivity_check(normalized["core"], config, classification)
    evidence = _evidence_registry(normalized, scores, config)
    valid_values = [v for v in normalized["core"].values() if v is not None]
    neutral_n = sum(v == config["display_rules"]["neutral_value"] for v in valid_values)
    neutral_ratio = neutral_n / len(valid_values) if valid_values else None
    frequency = {str(value): valid_values.count(value) for value in range(1, 6)}
    quality = {"valid_n": len(valid_values), "total_n": 32, "neutral_n": neutral_n,
               "neutral_ratio": neutral_ratio,
               "many_neutral": neutral_ratio is not None and neutral_ratio >= config["display_rules"]["many_neutral_ratio"],
               "response_distribution": frequency,
               "same_option_repeated": bool(valid_values) and max(frequency.values()) / len(valid_values) >= 0.75,
               "automatically_invalidated": False}
    insights = _rule_claims("insight", normalized, scores, evidence, config)
    drains = _rule_claims("drain", normalized, scores, evidence, config)
    if normalized["disliked"]:
        game = normalized["disliked"]
        labels = {x["value"]: x["label"] for x in config["taste"]["negative_reasons"]}
        for reason in game["reasons"]:
            drains.append({"rule_id": "D_NEGATIVE_GAME", "text": config["system_templates"]["negative_game"].format(title=game["title"], reason=labels[reason]),
                           "evidence_refs": [f"negative:{reason}"], "condition_snapshot": {"reason": reason, "experience": "yes"},
                           "scope": "只针对点名作品，不泛化为所有同类体验"})
    report = {
        "product": config["manifest"]["product"], "versions": deepcopy(config["manifest"]["versions"]),
        "schema_version": config["manifest"]["schema_version"], "fictional": normalized["fictional"],
        "respondent_id": normalized["respondent_id"], "display_name": normalized["display_name"],
        "response": normalized, "scores": scores, "classification": classification,
        "display": _profile_display(classification, sensitivity, scores, config),
        "sensitivity": sensitivity, "quality": quality, "insights": insights,
        "insight_gap": max(0, config["display_rules"]["max_insights"] - len(insights)),
        "behavior_tags": _rule_claims("tag", normalized, scores, evidence, config),
        "taste": _taste_report(normalized, scores, config),
        "enjoyments": _rule_claims("enjoyment", normalized, scores, evidence, config),
        "drains": drains, "advice": _advice(normalized, config),
        "self_checks": _rule_claims("self_check", normalized, scores, evidence, config),
        "supplement": [{"text": evidence[f"supplement:{t}"]["label"], "evidence_refs": [f"supplement:{t}"], "rule_id": "SUPPLEMENT_SELECTED", "condition_snapshot": {"selected": t}} for t in normalized["supplement"]],
        "evidence": evidence,
        "limitations": config["system_templates"]["limitations"],
    }
    canonical = json.dumps({"versions": report["versions"], "response": normalized}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    report["answer_fingerprint"] = sha256(canonical.encode()).hexdigest()
    verify_report_evidence(report)
    return report


def verify_report_evidence(report):
    registry = report["evidence"]
    claims = [report["display"], *report["insights"], *report["behavior_tags"],
              *report["taste"]["claims"], *report["taste"]["alignment"],
              *report["enjoyments"], *report["drains"], *report["self_checks"], *report["supplement"]]
    for claim in claims:
        if not claim["evidence_refs"] or not claim.get("rule_id") or "condition_snapshot" not in claim:
            raise InputError("具体报告判断缺少规则、触发快照或证据。")
        if any(ref not in registry for ref in claim["evidence_refs"]):
            raise InputError("具体报告判断引用了不存在的证据。")
        for ref in claim["evidence_refs"]:
            source = registry[ref]
            if source["source"] == "core" and source["value"] is None:
                raise InputError("缺失核心答案不能充当具体偏好的直接证据。")
    for advice in report["advice"]:
        if advice["basis"] == "explicit_answer" and not advice["evidence_refs"]:
            raise InputError("个性化建议缺少直接回答。")
    return True


def compare_reports(left: dict, right: dict, config: dict) -> dict:
    """Comparison is a coordination aid; it never computes a compatibility percentage."""
    same_version = left["versions"] == right["versions"] == config["manifest"]["versions"]
    templates = config["system_templates"]
    if not same_version:
        return {"status": "version_mismatch", "left_versions": left["versions"], "right_versions": right["versions"],
                "text": templates["comparison_version_mismatch"], "profiles_separate": True,
                "common_games": [], "profile_rows": [], "coordination": [], "evidence": {}}
    lres, rres = left["response"], right["response"]
    evidence = {f"{side}:{key}": deepcopy(value) for side, report in (("left", left), ("right", right)) for key, value in report["evidence"].items()}
    attractions = _index(config["taste"]["attractions"])
    common, related = [], []
    for i, lg in enumerate(lres["favorites"]):
        for j, rg in enumerate(rres["favorites"]):
            if lg["game_id"] != rg["game_id"]:
                continue
            if lg["edition"] != rg["edition"]:
                related.append({"title": lg["title"], "left_edition": lg["edition"], "right_edition": rg["edition"],
                                "evidence_refs": [f"left:favorite:{i}", f"right:favorite:{j}"]})
                continue
            common.append({"game_id": lg["game_id"], "title": lg["title"], "edition": lg["edition"],
                           "left_experience": lg["experience"], "right_experience": rg["experience"],
                           "left_attractions": [attractions[t]["label"] for t in lg["attractions"]],
                           "right_attractions": [attractions[t]["label"] for t in rg["attractions"]],
                           "shared_attractions": [attractions[t]["label"] for t in lg["attractions"] if t in rg["attractions"]],
                           "evidence_refs": [f"left:favorite:{i}", f"right:favorite:{j}"],
                           "rule_id": "PAIR_COMMON_GAME", "condition_snapshot": {"same_id": True, "same_edition": True}})
    rows = [{"dimension": d["id"], "name": d["name"], "left_score": left["scores"][d["id"]]["score"],
             "right_score": right["scores"][d["id"]]["score"],
             "left_valid_n": left["scores"][d["id"]]["valid_n"], "right_valid_n": right["scores"][d["id"]]["valid_n"],
             "evidence_refs": [f"left:score:{d['id']}", f"right:score:{d['id']}"]} for d in config["dimensions"]]
    coordination = []
    for topic in config["advice_topics"]:
        qid = topic["question_id"]
        lv, rv = lres["followups"].get(qid), rres["followups"].get(qid)
        refs = [f"{side}:answer:{qid}" for side, value in (("left", lv), ("right", rv)) if value is not None]
        status, recommendation = "insufficient", topic["fallback"]
        known = lv is not None and rv is not None and lv != "uncertain" and rv != "uncertain"
        if known:
            status = "shared" if lv == rv else "coordinate"
            recommendation = templates["pair_shared"].format(title=topic["title"]) if status == "shared" else templates["pair_coordinate"].format(title=topic["title"])
            if topic["id"] == "spoiler":
                if "ask_each_time" in (lv, rv):
                    status = "shared" if lv == rv else "coordinate"
                    recommendation = templates["pair_spoiler_ask"]
                else:
                    permissions = {"no_story_or_puzzle": set(), "puzzle_ok": {"谜底"}, "story_ok": {"剧情"}, "all_ok": {"剧情", "谜底"}}
                    common_permission = permissions[lv] & permissions[rv]
                    allowed = "、".join(x for x in ("剧情", "谜底") if x in common_permission) or "仅机制与操作，先不展开剧情和谜底"
                    recommendation = templates["pair_spoiler"].format(allowed=allowed)
            elif topic["id"] == "mod":
                restricted = {"platform_unavailable", "device_time_limited"}
                if lv in restricted or rv in restricted:
                    status, recommendation = "coordinate", templates["pair_mod_limited"]
                elif lv == rv == "not_interested":
                    status, recommendation = "shared", templates["pair_mod_no_interest"]
                else:
                    lm, rm = lres["followups"].get("M02"), rres["followups"].get("M02")
                    if lm is None or rm is None:
                        status, recommendation = "insufficient", templates["pair_mod_insufficient"]
                    else:
                        refs += ["left:answer:M02", "right:answer:M02"]
                        status = "shared" if lm == rm else "coordinate"
                        recommendation = templates["pair_mod_purposes"]
            elif topic["id"] == "guide":
                recommendation = templates["pair_guide"]
            elif lv == rv and topic["by_answer"]:
                recommendation = topic["by_answer"][lv]
        label_question = _index(config["followup_questions"])[qid]
        coordination.append({"topic": topic["id"], "title": topic["title"], "status": status,
                             "status_label": {"shared": "已有共同选择", "coordinate": "需要协调", "insufficient": "资料不足"}[status],
                             "left_answer": _label_answer(label_question, lv) if lv is not None else "未提供可用回答",
                             "right_answer": _label_answer(label_question, rv) if rv is not None else "未提供可用回答",
                             "recommendation": recommendation, "evidence_refs": refs,
                             "rule_id": "PAIR_" + topic["id"].upper(),
                             "condition_snapshot": {"left": lv, "right": rv},
                             "scope": "只比较明确回答；待协调不代表性格冲突"})
    return {"status": "comparable", "versions": deepcopy(left["versions"]), "fictional": left["fictional"] and right["fictional"],
            "left_name": left["display_name"], "right_name": right["display_name"],
            "left_id": left["respondent_id"], "right_id": right["respondent_id"],
            "common_games": common, "related_editions": related, "profile_rows": rows,
            "coordination": coordination, "evidence": evidence,
            "note": templates["pair_scope"]}
