"""Deterministic SEO research, intent classification, clustering, and ranking experiment helpers.

Pure Python 3.9+ standard library utilities supporting:
  - Configurable weighted keyword opportunity scoring (transparently separated from provider metrics)
  - Semrush numeric search-intent decoding
  - SERP-overlap anti-cannibalization clustering & page-format recommendation
  - Evidence-based ranking experiment evaluation (enforcing observation windows and baseline integrity)
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

SEMRUSH_INTENT_CODES: Dict[str, str] = {
    "0": "Commercial",
    "1": "Informational",
    "2": "Navigational",
    "3": "Transactional",
}

DEFAULT_OPPORTUNITY_WEIGHTS: Dict[str, float] = {
    "business_relevance": 0.25,
    "intent_conversion_fit": 0.25,
    "ranking_feasibility": 0.20,
    "search_demand": 0.15,
    "content_gap_geo_fit": 0.15,
}


def decode_semrush_intent(raw_code: Any) -> str:
    """Decode Semrush integer or comma-separated intent codes without guessing unknown values."""
    if raw_code is None:
        return "Unavailable"
    raw_str = str(raw_code).strip()
    if not raw_str:
        return "Unavailable"
    tokens = [tok.strip() for tok in raw_str.split(",") if tok.strip()]
    decoded: List[str] = []
    for tok in tokens:
        if tok not in SEMRUSH_INTENT_CODES:
            return f"Unresolved ({raw_str})"
        label = SEMRUSH_INTENT_CODES[tok]
        if label not in decoded:
            decoded.append(label)
    if len(decoded) > 1:
        return f"Mixed ({', '.join(decoded)})"
    return decoded[0]


def recommend_page_format(
    query: str,
    serp_types: Optional[Iterable[str]] = None,
    serp_features: Optional[Iterable[str]] = None,
) -> Dict[str, str]:
    """Recommend primary search intent and content format from query + observed SERP signals."""
    q = query.lower().strip()
    types_set = {t.strip().lower() for t in (serp_types or []) if t.strip()}
    features_set = {f.strip().lower() for f in (serp_features or []) if f.strip()}

    if "shopping" in features_set or "product_page" in types_set or "category_page" in types_set:
        fmt = "Product Page" if "product_page" in types_set and "category_page" not in types_set else "Category / Product Page"
        return {"intent": "Transactional / Commercial", "format": fmt}

    if "local_pack" in features_set or any(tok in q for tok in ("near me", "in bangalore", "in pune", "in delhi", "in mumbai", "agency in", "services in")):
        return {"intent": "Local / Commercial", "format": "Service or Location Page"}

    if any(tok in q for tok in (" vs ", "versus", "alternative", "alternatives", "best ", "top ", "comparison", "compare ")):
        return {"intent": "Commercial Investigation", "format": "Comparison Article or Buying Guide"}

    if any(tok in q for tok in ("hire ", "buy ", "pricing", "quote", "book demo", "free trial", "cost of", "services")):
        if "service_page" in types_set or "landing_page" in types_set or not types_set:
            return {"intent": "Transactional / Commercial", "format": "Service or Commercial Landing Page"}

    if any(q.startswith(prefix) for prefix in ("how to ", "what is ", "why ", "guide ", "tutorial ")) or "featured_snippet" in features_set:
        if types_set & {"service_page", "landing_page", "product_page"}:
            return {"intent": "Mixed (Informational + Commercial)", "format": "Hybrid Guide + Solution Landing Page"}
        return {"intent": "Informational", "format": "Tutorial, Guide, or Documentation"}

    if types_set & {"service_page", "saas_landing"}:
        return {"intent": "Commercial", "format": "Dedicated Landing / Service Page"}

    return {"intent": "Informational", "format": "Blog Guide or Resource Page"}


def compute_opportunity_score(
    business_relevance: float,
    intent_conversion_fit: float,
    ranking_feasibility: float,
    search_demand: Optional[float] = None,
    content_gap_geo_fit: float = 0.5,
    weights: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Compute a transparent weighted opportunity score in [0, 100].

    Inputs are normalized 0.0-1.0. When `search_demand` is None (volume Unavailable),
    demand weight is redistributed cleanly or marked qualitative so missing data is never invented.
    """
    active_weights = dict(DEFAULT_OPPORTUNITY_WEIGHTS)
    if weights:
        active_weights.update(weights)

    components = {
        "business_relevance": max(0.0, min(1.0, business_relevance)),
        "intent_conversion_fit": max(0.0, min(1.0, intent_conversion_fit)),
        "ranking_feasibility": max(0.0, min(1.0, ranking_feasibility)),
        "content_gap_geo_fit": max(0.0, min(1.0, content_gap_geo_fit)),
    }

    demand_status = "measured"
    if search_demand is None:
        demand_status = "Unavailable (redistributed across qualitative weights)"
        active_weights.pop("search_demand", None)
    else:
        components["search_demand"] = max(0.0, min(1.0, search_demand))

    total_weight = sum(active_weights.values())
    if total_weight <= 0 or not math.isfinite(total_weight):
        raise ValueError("Opportunity weights must sum to a positive finite number.")

    weighted_sum = sum(components[k] * active_weights[k] for k in components if k in active_weights)
    score = round((weighted_sum / total_weight) * 100.0, 1)

    return {
        "opportunity_score": score,
        "is_google_metric": False,
        "demand_input_status": demand_status,
        "weights_used": {k: round(v / total_weight, 4) for k, v in active_weights.items() if k in components},
    }


def cluster_by_serp_overlap(
    keyword_serps: Sequence[Dict[str, Any]],
    min_shared_urls: int = 3,
) -> List[Dict[str, Any]]:
    """Cluster keywords sharing intent and top-10 SERP URL overlap to prevent cannibalization.

    Each item in `keyword_serps` expects:
      {"keyword": str, "intent": str, "urls": list[str], "volume": int|None}
    """
    clusters: List[Dict[str, Any]] = []
    for entry in keyword_serps:
        kw = str(entry["keyword"]).strip()
        intent = str(entry.get("intent", "Unknown")).strip().lower()
        urls = {u.rstrip("/").lower() for u in entry.get("urls", []) if u}

        matched_cluster = None
        for cluster in clusters:
            if cluster["intent_norm"] != intent:
                continue
            overlap = len(urls & cluster["anchor_urls"])
            if overlap >= min_shared_urls:
                matched_cluster = cluster
                break

        if matched_cluster is None:
            clusters.append(
                {
                    "primary_keyword": kw,
                    "intent": entry.get("intent", "Unknown"),
                    "intent_norm": intent,
                    "anchor_urls": set(urls),
                    "keywords": [entry],
                }
            )
        else:
            matched_cluster["keywords"].append(entry)

    output: List[Dict[str, Any]] = []
    for cl in clusters:
        kw_list = cl["keywords"]
        # Pick primary keyword by highest known volume, falling back to shortest clear phrase
        best = max(
            kw_list,
            key=lambda item: (
                item.get("volume") if isinstance(item.get("volume"), (int, float)) else -1,
                -len(str(item["keyword"])),
            ),
        )
        supporting = [item["keyword"] for item in kw_list if item["keyword"] != best["keyword"]]
        slug_base = re.sub(r"[^a-z0-9]+", "-", best["keyword"].lower()).strip("-")
        output.append(
            {
                "primary_keyword": best["keyword"],
                "supporting_keywords": supporting,
                "intent": cl["intent"],
                "recommended_slug": f"/{slug_base}",
                "cluster_size": len(kw_list),
            }
        )
    return output


def evaluate_ranking_experiment(experiment: Dict[str, Any], min_window_days: int = 14) -> Dict[str, Any]:
    """Evaluate a ranking experiment honestly without over-claiming attribution.

    Requires:
      - Observation window >= `min_window_days`
      - Non-unavailable baseline metric (clicks, impressions, tracker_position, or conversions)
      - Keeps GSC average position strictly separate from geo/device-pinned tracker_position
    """
    baseline = experiment.get("baseline", {})
    post = experiment.get("post_change", {})
    window_days = int(post.get("observation_window_days") or 0)

    def _num(val: Any) -> Optional[float]:
        if isinstance(val, (int, float)) and math.isfinite(val):
            return float(val)
        return None

    base_clicks = _num(baseline.get("clicks"))
    post_clicks = _num(post.get("clicks"))
    base_impr = _num(baseline.get("impressions"))
    post_impr = _num(post.get("impressions"))
    base_pos = _num(baseline.get("tracker_position"))
    post_pos = _num(post.get("tracker_position"))
    base_conv = _num(baseline.get("conversions"))
    post_conv = _num(post.get("conversions"))

    if post_clicks is None and post_impr is None and post_pos is None and post_conv is None:
        return {
            "status": "awaiting-data",
            "reason": "No post-change measurements recorded yet.",
            "next_action": "continue-observing",
        }

    if window_days < min_window_days:
        return {
            "status": "inconclusive",
            "reason": f"Observation window ({window_days}d) is shorter than minimum {min_window_days}d recrawl threshold.",
            "next_action": "continue-observing",
        }

    has_comparable_baseline = any(
        b is not None and p is not None
        for b, p in ((base_clicks, post_clicks), (base_impr, post_impr), (base_pos, post_pos), (base_conv, post_conv))
    )
    if not has_comparable_baseline:
        return {
            "status": "inconclusive",
            "reason": "Baseline measurements are unavailable for comparable metrics.",
            "next_action": "record-current-as-new-baseline",
        }

    signals: List[str] = []
    score = 0

    if base_conv is not None and post_conv is not None and (base_conv > 0 or post_conv > 0):
        delta_conv = post_conv - base_conv
        signals.append(f"conversions: {base_conv:g} -> {post_conv:g}")
        if delta_conv > 0:
            score += 2
        elif delta_conv < 0:
            score -= 2

    if base_clicks is not None and post_clicks is not None and max(base_clicks, post_clicks) >= 5:
        pct = ((post_clicks - base_clicks) / max(base_clicks, 1.0)) * 100.0
        signals.append(f"clicks: {base_clicks:g} -> {post_clicks:g} ({pct:+.1f}%)")
        if pct >= 15.0:
            score += 1
        elif pct <= -15.0:
            score -= 1

    if base_pos is not None and post_pos is not None:
        # Lower numeric position is better (e.g., 12 -> 5 is +7 improvement)
        pos_gain = base_pos - post_pos
        signals.append(f"pinned tracker_position: {base_pos:g} -> {post_pos:g}")
        if pos_gain >= 2.0:
            score += 1
        elif pos_gain <= -2.0:
            score -= 1

    confounders = [c for c in experiment.get("evaluation", {}).get("confounding_factors", []) if c and "none" not in str(c).lower()]

    if not signals:
        return {
            "status": "inconclusive",
            "reason": "Sample volume is too small for reliable directional attribution.",
            "next_action": "continue-observing",
        }

    if score >= 1:
        status = "improved"
        next_action = "keep"
    elif score <= -1:
        status = "declined"
        next_action = "iterate"
    else:
        status = "inconclusive"
        next_action = "continue-observing"

    return {
        "status": status,
        "signals": signals,
        "confounding_factors_noted": confounders,
        "next_action": next_action,
    }
