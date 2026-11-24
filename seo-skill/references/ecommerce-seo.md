# E-Commerce SEO Playbook

Activate this workflow for online stores, D2C brands, and B2B/B2C catalogs where searchers browse categories, compare SKUs, and purchase online.

## Core Architecture: Category vs. Product Intent

| Page Type | Primary Intent | Role in Site Architecture |
|---|---|---|
| **Category / Collection Pages** | Commercial / browse (`"4k wifi security cameras"`, `"gaming laptops under 70000"`) | Capture broader, multi-option shopping demand; link down to PDPs and sub-categories |
| **Sub-Category / Curated Filter Pages** | Refined commercial (`"outdoor solar cctv cameras"`, `"16gb ram laptops"`) | Index **only** curated, high-demand facets with clean static URLs, unique H1/title, and genuine demand |
| **Product Detail Pages (PDPs)** | Transactional SKU/model (`"hikvision 4mp ip bullet camera price"`) | Capture exact model/brand/SKU searches; optimize for specs, availability, trust, and conversion |
| **Buying Guides & Comparisons** | Commercial Investigation (`"how to choose a router for gaming"`, `"oled vs qled tv"`) | Educate unsure buyers and funnel internally to high-margin categories/PDPs |

---

## E-Commerce Technical Traps & Fixes

### 1. Faceted Navigation & Filter Parameters
Uncontrolled filter combinations (`?color=black&brand=x&sort=price_asc&rating=4`) create millions of thin, duplicate URLs that waste crawl budget and dilute index signals.
- **Never** let arbitrary combinations (`sort=`, `page=`, multi-select filters) become indexable URLs.
- Use consistent governance:
  - Block crawlable parameter traps cleanly OR handle non-SEO interactive filters via JS state / disallowed query params / `noindex, follow` on low-value filter pages, while exposing **curated SEO sub-categories** as clean static URLs (`/cameras/outdoor-solar/`).
  - Do **not** include non-canonical filter URLs in XML sitemaps.
  - Ensure canonicalized filter URLs do not create conflicting signals (canonicalize minor sort/view params to the clean category URL).

### 2. Product Variants (Color, Size, Storage)
- **Single-concept variants** (e.g., shirt sizes S/M/L, same phone in Blue vs. Black when users search the model generically): host on one canonical PDP with selectable variant states (optional URL query `?variant=` canonicalizing to the parent SKU URL).
- **Distinct search-demand variants** (e.g., `"iPhone 16 128GB"` vs `"iPhone 16 Pro Max 1TB"`, or noticeably distinct models): separate indexable URLs only when copy, specs, images, and buyer intent truly differ.

### 3. Pagination & Crawl Depth
- Paginated category pages (`/laptops?page=2`) should carry self-referencing `rel="canonical"` to `?page=2`, NOT back to page 1, so products on deeper pages remain discoverable and indexable.
- Ensure top-selling and high-margin categories and products sit within 2–3 clicks of the homepage via clean category menus and contextual links.

### 4. Out-of-Stock & Discontinued Product Lifecycle
- **Temporarily out of stock:** Keep `200 OK` indexed, clearly show `"Out of stock"` (and accurate restock date or back-in-stock notify form if real), update `Offer.availability` to `https://schema.org/OutOfStock`, and suggest comparable in-stock alternatives.
- **Permanently discontinued with a direct successor:** `301` redirect to the replacement model/version and update internal links.
- **Permanently discontinued with no successor:** Return `404` or `410` (or `301` to parent category only if the category directly satisfies visitors—avoid mass redirecting thousands of dead SKUs to the homepage, which Google treats as soft 404s).

---

## On-Page E-Commerce Optimization

- **Avoid manufacturer boilerplate duplication.** Rewrite/augment supplier spec sheets with real use-case guidance, compatibility notes, box contents, warranty/return details, delivery timelines, and original photos/comparison tables.
- **Category copy placement:** Put a concise, helpful 1–2 sentence intro above the product grid (without pushing products off mobile screens!) and deeper buying guidance/FAQs cleanly below the product grid.
- **Internal cross-linking:** Related categories, `"compatible accessories"`, curated guides linked to categories, and breadcrumbs (`Home > Electronics > Monitors > 4K Monitors`).
- **Checkout & Conversion UX:** Clear pricing (including GST/taxes/shipping transparency), trust badges (warranty, return window, COD/payment security), fast mobile product gallery, clear stock indicators.

---

## Product & Merchant Listing Structured Data

Verify alignment with Google's **Product Snippets** and **Merchant Listings** documentation:
- Implement `Product` JSON-LD on PDPs containing real, visible `name`, `image`, `description`, `sku`/`mpn`/`gtin` (when accurate), `brand`, and `offers` (`price`, `priceCurrency`, `availability`, `url`, plus `shippingDetails` and `hasMerchantReturnPolicy` when supported).
- Include `aggregateRating` / `review` **only** if genuine, visible customer reviews exist on that exact product page—never fabricate scores or paste sitewide store reviews onto individual SKUs.
- On category pages, focus on `BreadcrumbList` and clean `ItemList` (do not mark up a category listing page as a single `Product` with an aggregate price unless following Google's multi-offer product documentation properly).
