"""Descriptive research metrics; intentionally not used by product reports.

No significance test is exposed: dyads are dependent and a formal study must
freeze a participant-level resampling/analysis plan before testing hypotheses.
"""

from collections import Counter
from math import log
from statistics import mean


def liked_work_set(response, *, experienced_only=True, collapse_series=False):
    works=set()
    for game in response["favorites"]:
        if experienced_only and game["experience"]!="yes":
            continue
        identity=("series:"+game["series_id"]) if collapse_series and game.get("series_id") else game["game_id"]
        works.add(identity)
    return works


def popularity_weights(responses, *, experienced_only=True, collapse_series=False):
    responses=list(responses)
    counts=Counter()
    for response in responses:
        counts.update(liked_work_set(response,experienced_only=experienced_only,collapse_series=collapse_series))
    n=len(responses)
    return {work:log((n+1)/(count+1))+1 for work,count in counts.items()}


def taste_overlap(left,right,weights=None,*,experienced_only=True,collapse_series=False):
    a=liked_work_set(left,experienced_only=experienced_only,collapse_series=collapse_series)
    b=liked_work_set(right,experienced_only=experienced_only,collapse_series=collapse_series)
    union=a|b
    if not union:
        return {"intersection_n":0,"left_n":0,"right_n":0,"jaccard":None,"weighted_jaccard":None}
    if weights is not None and any(work not in weights for work in union):
        raise ValueError("Weights must come from the declared research cohort, covering all included works")
    weighted=lambda work:weights[work] if weights is not None else 1
    return {"intersection_n":len(a&b),"left_n":len(a),"right_n":len(b),
            "jaccard":len(a&b)/len(union),
            "weighted_jaccard":sum(weighted(w) for w in a&b)/sum(weighted(w) for w in union)}


def profile_distances(left,right,*,require_complete=True):
    dimensions=[d for d in left["scores"] if d in right["scores"] and left["scores"][d]["score"] is not None and right["scores"][d]["score"] is not None]
    if not dimensions or (require_complete and len(dimensions)!=8):
        return {"dimensions":dimensions,"mean_absolute_difference":None,"centered_shape_difference":None}
    a=[left["scores"][d]["score"] for d in dimensions]
    b=[right["scores"][d]["score"] for d in dimensions]
    ma,mb=mean(a),mean(b)
    return {"dimensions":dimensions,"mean_absolute_difference":mean(abs(x-y) for x,y in zip(a,b)),
            "centered_shape_difference":mean(abs((x-ma)-(y-mb)) for x,y in zip(a,b))}
