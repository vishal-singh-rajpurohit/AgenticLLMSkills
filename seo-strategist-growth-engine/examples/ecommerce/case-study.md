# Scenario 2 — E-Commerce Store (Worked Example)

> *Illustrative demonstration scenario covering product & category keyword architecture, faceted navigation controls, `Product` JSON-LD, internal linking, and GSC/GA4 monitoring.*

## 1. Confirmed Business Context
- **Model:** Direct-to-consumer & B2B hardware e-commerce (`4K USB-C Monitors, Docking Stations, Ergonomic Desk Gear`)
- **Platform:** Next.js App Router storefront (`SSR/ISR`) + headless inventory catalog
- **Primary Conversion:** Completed checkout purchases + B2B bulk quote inquiries

## 2. Category vs. Product Keyword Architecture

| Keyword | Intent | Volume | Difficulty | Business Relevance | Canonical Target & Format |
|---|---|---|---|---|---|
| `4k usb-c monitors for programming` | Commercial Investigation | Unavailable | Unavailable | High | Curated Category / Sub-Category Page (`/monitors/4k-usb-c`) |
| `27 inch 4k usb-c monitor 90w pd` | Transactional | Unavailable | Unavailable | High | Promoted Static Facet or High-Margin Category Hub |
| `<brand> prodisplay 27 4k review & specs` | Transactional / Product | Unavailable | Unavailable | High | Product Detail Page (`/products/prodisplay-27-4k`) |
| `thunderbolt 4 vs usb-c dock for dual 4k` | Commercial Investigation | Unavailable | Unavailable | Medium-High | Buying Guide (`/guides/thunderbolt-4-vs-usb-c-dock`) linking to PDPs |

## 3. Faceted Navigation & Technical Rules
- **Indexation Control:** Prevent multi-parameter combinations (`?sort=price&color=black&in_stock=1`) from inflating crawl waste via `rel="canonical"` to the base category, `<meta name="robots" content="noindex, follow">` on arbitrary combinations, and exclusion from `sitemap.xml`.
- **Promoted Facets:** Expose clean static URLs only for verified recurring buyer modifiers (e.g., `/monitors/4k-usb-c`) backed by unique buying criteria and distinct inventory copy.
- **Out-of-Stock Lifecycle:** Keep temporarily out-of-stock PDPs `200 OK` with `https://schema.org/OutOfStock` and alternative in-stock suggestions; use `301` redirects only when a SKU is permanently retired with an exact successor model.
- **Structured Data (`Product` + `BreadcrumbList`):** Populate `name`, `image`, `sku`, `brand`, and visible `offers` (`price`, `priceCurrency`, `availability`, `url`). Include `aggregateRating` strictly when real product reviews render on that exact PDP.

## 4. Internal Linking & Performance Monitoring
- **Internal Topology:** `BreadcrumbList` UI links (`Home -> Monitors -> 4K USB-C`), cross-linked compatible accessories on PDPs, and buying guides pointing contextually to curated categories.
- **Monitoring Loop:** Track GA4 `Organic Search` landing-page conversion rate and add-to-cart rate alongside GSC category vs. PDP query cannibalization.
