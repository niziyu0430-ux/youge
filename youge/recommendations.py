"""Match the choices in a completed report to verified game mechanics."""
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import json
import logging

from . import v04


CURATED = v04.ROOT / 'config/game-recommendations.json'
CROSS_QUESTIONS = {'X13', 'X14', 'X15', 'X16'}
BROAD_GENRES = {'action', 'adventure', 'simulation', 'casual'}


@lru_cache(maxsize=1)
def curated_games():
    try:
        return json.loads(CURATED.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        logging.getLogger(__name__).exception('Could not load curated game recommendations')
        return {}


def preferences(report):
    """Use only answers verified by the original instrument, including its actual variants."""
    cross, anchors = Counter(), Counter()
    supplements = set()
    motives = {persona['id'] for persona in v04.config()['personas']}
    supplemental_ids = {answer['question_id'] for answer in report['response']['extra_answers']}
    for choice in report['evidence'].values():
        signal = choice.get('signal')
        if 'weights' in choice:
            positive = {key: weight for key, weight in choice['weights'].items() if weight > 0}
            signal = max(positive, key=positive.get, default=None)
        if signal not in motives:
            continue
        if choice['scope'] == 'anchor':
            anchors[signal] += 1
        elif choice['question_id'] in CROSS_QUESTIONS:
            cross[signal] += 1
        elif choice['question_id'] in supplemental_ids:
            supplements.add(signal)
    return {
        signal: 3 * cross[signal] + min(anchors[signal], 2) + (signal in supplements)
        for signal in cross.keys() | anchors.keys() | supplements
    }


@dataclass(frozen=True)
class Match:
    game_id: str
    work_id: str
    title: str
    platform: str
    reason: str
    motive: str
    strength: int
    secondary: int
    genres: frozenset
    nearby: bool
    pc: bool
    reviews: int

    def rank(self):
        return (-self.strength, -self.secondary, not self.nearby, not self.pc,
                -self.reviews, self.game_id)

    def display(self):
        return {'game_id': self.game_id, 'title': self.title,
                'platform': self.platform, 'reason': self.reason}


def _matches(report, weights):
    catalogue = v04.catalog()
    genres = {c['id'] for c in catalogue['categories'] if c['kind'] == 'genre'} - BROAD_GENRES
    favorite = v04.find_game(report['game']['id'])
    favorite_genres = genres.intersection(favorite['category_ids'])
    favorite_work = favorite.get('work_id') or favorite['id']
    public = v04.public_game_ids()
    curated = curated_games()
    for game in catalogue['games']:
        game_id = game['id']
        if game_id not in curated or game_id not in public or game['visibility'] != 'published':
            continue
        if game_id == favorite['id'] or game['work_id'] == favorite_work or game_id in catalogue.get('search_redirects', {}):
            continue
        entry = curated[game_id]
        reasons = entry['reasons']
        picks = sorted((motive for motive in reasons if weights.get(motive, 0)),
                       key=lambda motive: (-weights[motive], motive))
        if not picks:
            continue
        first, *rest = picks
        pc = 'PC' in game['platforms']
        platform = 'PC' if pc else entry.get('platform', ' / '.join(game['platforms']))
        if entry.get('requires'):
            platform += ' · ' + entry['requires']
        game_genres = frozenset(genres.intersection(game['category_ids']))
        yield Match(
            game_id=game_id,
            work_id=game['work_id'],
            title=game.get('display_title') or v04.current_game_identity(game)['title'],
            platform=platform,
            reason=reasons[first],
            motive=first,
            strength=weights[first],
            secondary=weights[rest[0]] if rest else 0,
            genres=game_genres,
            nearby=bool(favorite_genres & game_genres),
            pc=pc,
            reviews=(game.get('chinese_review_evidence') or {}).get('total_reviews', 0),
        )


def _choose(matches):
    pc_games = [match for match in matches if match.pc]
    chosen = []
    used = set()
    for match in pc_games:
        if match.work_id in used:
            continue
        chosen.append(match)
        used.add(match.work_id)
        if len(chosen) == 3:
            break
    if len(chosen) < 3:
        return []

    # Give a similarly strong title from the other category a place in the first three.
    weakest = chosen[-1].strength
    if all(match.nearby == chosen[0].nearby for match in chosen):
        alternate = next((match for match in pc_games
                          if match.genres and match.nearby != chosen[0].nearby
                          and match.strength >= max(3, weakest - 1) and match.work_id not in used), None)
        if alternate:
            used.remove(chosen[-1].work_id)
            chosen[-1] = alternate
            used.add(alternate.work_id)

    weakest = min(match.strength for match in chosen)
    covered_genres = set().union(*(match.genres for match in chosen))
    covered_motives = {match.motive for match in chosen}
    console_added = False
    # The fifth card needs more support than one cross-game choice on its own.
    for minimum_strength in (3, 4):
        eligible = (match for match in matches
                    if match.work_id not in used and match.strength >= minimum_strength
                    and (match.pc or (not console_added and match.strength >= weakest))
                    and (match.motive not in covered_motives or match.genres - covered_genres))
        # Prefer a second answer-backed interest over another game for the same interest.
        extra = min(eligible, key=lambda match: (match.motive in covered_motives, match.rank()), default=None)
        if extra is None:
            break
        chosen.append(extra)
        used.add(extra.work_id)
        covered_genres.update(extra.genres)
        covered_motives.add(extra.motive)
        console_added = console_added or not extra.pc
    return chosen


def for_report(report):
    matches = sorted(_matches(report, preferences(report)), key=Match.rank)
    return [match.display() for match in _choose(matches)]
