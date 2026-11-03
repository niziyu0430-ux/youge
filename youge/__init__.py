"""游格内容规格的确定性参考实现；不包含网站或外部服务。"""

from .engine import (
    InputError, build_report, classify_profile, compare_reports, load_config,
    normalize_response, score_core, sensitivity_check, validate_config,
)

__all__ = [
    "InputError", "build_report", "classify_profile", "compare_reports", "load_config",
    "normalize_response", "score_core", "sensitivity_check", "validate_config",
]
