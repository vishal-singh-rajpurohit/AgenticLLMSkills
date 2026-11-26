# Controlled SEO Ranking Experiment

*(Record real baseline measurements before shipping changes; mark missing metrics `unavailable`, never invent data.)*

```yaml
experiment:
  id: "<page-slug-001>"
  url: "</target/path>"
  target_keywords:
    - "<primary target keyword>"
    - "<secondary target keyword>"

  measurement_context:
    country: "<Country>"
    language: "<Language>"
    device: "<mobile | desktop | all>"
    gsc_source: "<Connected | CSV Export | Unavailable>"
    rank_tracker_provider: "<Provider name or Unavailable>"

  baseline:
    date: "<YYYY-MM-DD>"
    observation_window_days: 28
    gsc_avg_position: unavailable
    tracker_position: unavailable
    clicks: unavailable
    impressions: unavailable
    ctr: unavailable
    conversions: unavailable
    indexed_status: "<Indexed | Not Indexed | Unavailable>"

  changes:
    deploy_date: "<YYYY-MM-DD>"
    summary:
      - "<Exact edit 1, e.g., Updated title & H1 alignment>"
      - "<Exact edit 2, e.g., Added pricing drivers & internal links>"

  post_change:
    evaluation_date: "<YYYY-MM-DD>"
    observation_window_days: 0
    gsc_avg_position: unavailable
    tracker_position: unavailable
    clicks: unavailable
    impressions: unavailable
    ctr: unavailable
    conversions: unavailable

  evaluation:
    status: awaiting-data # awaiting-data | improved | declined | inconclusive
    confounding_factors:
      - "<SERP layout change, seasonality, algorithm update, or none observed>"
    conclusion: "<Evidence-based evaluation; report inconclusive if window < 14 days or baseline missing>"
    next_action: "<continue-observing | iterate | keep | revert>"
```
