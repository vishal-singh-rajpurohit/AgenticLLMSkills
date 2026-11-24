# Image Research, Sourcing & Licensing

Select visuals that genuinely clarify steps, products, data, or real work—never generic decorative clutter or unlicensed web images.

## Sourcing Priority Ladder

1. **User-provided images & screenshots:** Always prefer genuine client photos, UI captures, hardware installations, and team media.
2. **Original business photography / authentic product media:** Verified official manufacturer/vendor product packs or original captures.
3. **Licensed stock & open repositories (verify every individual asset license!):**
   - **Unsplash** (Unsplash License — verify no recognizable trademarks/people issues in commercial context; credit photographer thoughtfully where appropriate).
   - **Pexels** (Pexels License — verify commercial terms and model/property release limitations).
   - **Wikimedia Commons** (check exact asset license: `CC0` vs `CC BY` requiring mandatory attribution vs `CC BY-SA` share-alike vs non-commercial `NC` licenses that **cannot** be used on commercial sites!).
   - **Official documentation / press kits** (subject to vendor brand guidelines).
4. **Commissioned diagrams or generated illustrations:** Use when bespoke process diagrams or conceptual visuals add clear understanding (never pass generated imagery off as real product photos or real client installations!).

### Mandatory Licensing Rules
- **Never** assume an image returned by Google Images or a competitor blog is free to use.
- **Never** hotlink directly to third-party domains without explicit permission and stable CDN hosting.
- **Never** skip attribution when required by Creative Commons (`CC BY`, `CC BY-SA`) or editorial licenses.

---

## Image Asset Manifest (Prepare for Every Visual)

Document these fields in every content package before approval:
- **Source URL** (exact asset page or local user source)
- **Local Asset Filename** (descriptive, lowercase hyphenated, e.g., `warehouse-poe-nvr-wiring-diagram.webp`)
- **License & Verification Date** (e.g., `User-supplied`, `CC BY 4.0`, `Unsplash License`, checked `YYYY-MM-DD`)
- **Attribution Required?** (`None` or exact required credit line + link)
- **Target Placement** (e.g., `Featured hero`, `Under H2: PoE vs Wi-Fi`)
- **Descriptive Alt Text** (accurately describes what the image depicts for screen readers and image search—zero keyword stuffing; use `alt=""` for purely decorative UI icons)
- **Caption** (optional contextual note when helpful)
- **Dimensions & Format** (prefer WebP or AVIF with explicit `width` and `height` / aspect ratio to prevent CLS)

---

## Implementation Rules by Architecture

- **Static / Source-Code Sites:** Save assets inside the project's existing `public/` or `assets/` folder; render through the codebase's established image component (`next/image`, `astro:assets`, `<NuxtImg>`); set explicit width/height; **do not** apply `loading="lazy"` to the critical above-the-fold hero/LCP image, and do apply lazy loading to below-the-fold images where appropriate.
- **Database / CMS Sites:** Inspect the existing media adapter (S3/R2/Cloudinary/Directus/Strapi/Sanity/WordPress Media) and upload via existing APIs, persisting alt text, caption, attribution, and relation IDs. Never invent a parallel storage bucket without checking existing media plumbing first.
