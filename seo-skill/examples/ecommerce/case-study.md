# Worked Example: E-Commerce Store (Pan-India Electronics Retail)

*(Illustrative worked scenario demonstrating category vs. PDP intent separation, faceted navigation control, out-of-stock handling, and honest Product JSON-LD.)*

---

## 1. Customer Segments & Intent Split

| Segment | Typical Search Pattern | Ideal Target Page |
|---|---|---|
| **Category Browsers** | `"4k ips monitor under 25000 india"`, `"gaming mechanical keyboard"` | Curated Category / Sub-Category Page |
| **Spec-Driven SKU Buyers** | `"lg 27gp850 price india"`, `"logitech mx master 3s specs"` | Product Detail Page (PDP) |
| **Unsure / Comparing Buyers** | `"ips vs va monitor for coding and gaming"`, `"thunderbolt dock vs usb c hub"` | Buying Guide / Comparison Article |
| **B2B / Bulk Office Procurement** | `"bulk laptops with gst invoice india"` | B2B Bulk Inquiry Landing Page |

---

## 2. Technical Architecture Rules Applied

1. **Faceted Navigation Governance:**
   - Arbitrary filter URLs (`/monitors?sort=price_asc&refresh=144hz&brand=lg&in_stock=1`) must **not** enter the XML sitemap or compete in Google's index.
   - Expose high-demand single-facet sub-categories as clean static URLs with unique titles, `<h1>`, and helpful intro copy (e.g., `/monitors/4k-usb-c-monitors`), while keeping multi-filter combinations `noindex, follow` (or client-side state).
2. **Product Variants:**
   - Color/cable-length variants on the same mouse/keyboard share one canonical PDP URL; distinct capacity/tier models with separate search demand (`256GB` vs `1TB` SSD) use distinct canonical URLs only if specs/reviews/pricing justify separate pages.
3. **Out-of-Stock Lifecycle:**
   - Temporary restock -> `200 OK`, clear `"Notify Me"` CTA, `https://schema.org/OutOfStock` in `Offer.availability`, comparable in-stock alternatives grid.
   - Discontinued SKU with newer generation -> `301` redirect to the replacement model (update internal links).
   - Discontinued SKU with zero replacement -> `404`/`410` (never bulk-redirect dead SKUs to `/`).
4. **Pagination:** `/monitors?page=2` uses a self-referencing canonical (`/monitors?page=2`), never canonicalizing back to page 1.

---

## 3. Product JSON-LD Verification Example (Compliant)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Acme 27-Inch 4K USB-C IPS Monitor",
  "image": ["https://store.example/images/acme-27-4k.webp"],
  "description": "27-inch UHD 3840x2160 IPS panel with 65W USB-C power delivery and 3-year India warranty.",
  "sku": "ACME-27UHD-IN",
  "brand": { "@type": "Brand", "name": "Acme" },
  "offers": {
    "@type": "Offer",
    "url": "https://store.example/monitors/acme-27-4k-usb-c",
    "priceCurrency": "INR",
    "price": "24999",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
```
*(Notice: `aggregateRating` is omitted when the page does not display real, verified customer reviews for that exact SKU.)*
