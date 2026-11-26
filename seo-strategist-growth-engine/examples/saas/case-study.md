# Scenario 3 — B2B SaaS Growth Engine (Worked Example)

> *Illustrative demonstration scenario covering problem-based keywords, competitor comparisons, use-case & feature pages, educational hubs, and pipeline-first CRO.*

## 1. Confirmed Business Context
- **Model:** B2B SaaS (`Automated Cloud Spend & Kubernetes Cost Optimization`)
- **Audience:** DevOps leads & FinOps engineers (high technical fluency; skeptical of inflated ROI calculators and black-box agents)
- **Primary Conversion:** Booked architecture demo + self-serve sandbox trial

## 2. Funnel-First Keyword & Page Strategy

| Buyer Stage | Keyword Cluster | Dominant Intent | Recommended Format & URL | Primary CTA |
|---|---|---|---|---|
| **Bottom (High Intent)** | `<competitor> alternatives for kubernetes` | Commercial Investigation | Honest Comparison Page (`/compare/competitor-alternatives`) | Launch read-only cost audit |
| **Bottom (Use Case)** | `reduce aws eks idle node costs` | Commercial / Problem | Use-Case Landing Page (`/use-cases/eks-cost-optimization`) | Start 14-day FinOps sandbox |
| **Middle (Feature / Integration)** | `kubernetes namespace cost allocation tool` | Commercial | Feature Page (`/features/namespace-cost-allocation`) | Interactive sandbox preview |
| **Top / Middle (Educational)** | `how to rightsize kubernetes requests vs limits` | Informational | Deep Engineering Tutorial (`/guides/k8s-rightsizing`) | Contextual link to `/features/autoscaling` |

## 3. Differentiation & Writing Guardrails
- **Comparison Integrity:** Include verified pricing model differences, deployment footprint (read-only IAM vs. DaemonSet agent), and honest cases where the competitor fits better—dated clearly (`Last verified: YYYY-MM-DD`).
- **Proof & CRO:** Embed real CLI/Helm install snippets, architecture diagrams with verified alt text, and transparent security docs right above demo/trial CTAs—never invent G2 ratings or fake customer savings percentages.
- **Measurement:** Pair GSC non-branded clicks per landing page with GA4 `trial_started` and `demo_booked` key events before scaling further topic clusters.
