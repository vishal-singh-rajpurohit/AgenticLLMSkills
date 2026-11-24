# Internal & External Linking Strategy

Connect each new or updated page into the site's actual topology and ground external claims in verified primary sources.

## Internal Linking Protocol

1. **Inspect existing routes, content, or database records first.** Check `app/`, `pages/`, `content/`, `sitemap.xml`, or existing CMS posts/categories before proposing any link.
2. **Never invent internal URLs.** Every recommended internal link must match a verified existing URL or an explicitly approved new page in the same release plan.
3. **Target high-value destinations:**
   - Related commercial service or product pages.
   - Core category and pillar hubs.
   - Deeply relevant supporting articles or tutorials.
   - High-intent conversion pages (pricing, quote, booking, documentation).

### Link Plan Specification
For each proposed internal link (both **outbound** from the new piece and **inbound** added to existing pages pointing to the new piece), record:
`| Direction | Source URL | Target URL | Proposed Anchor Text | Placement Context | Rationale |`

- **Anchor text rule:** Use natural, descriptive phrases telling readers what sits behind the click (`"commercial CCTV installation specifications"`—never `"click here"` or forced exact-match repetition).
- **Crawlability:** Render internal navigation and inline links via standard `<a href="...">` / framework `<Link href="...">` elements, never JS-only click handlers.

---

## External Linking Protocol

- Link out selectively to **primary, trustworthy sources** that directly substantiate statistics, standards, official APIs, or regulations.
- **Verify every URL** resolves cleanly (`200 OK`, no broken 4xx/5xx or spammy redirect hijacks) and confirm the destination page actually supports the linked sentence.
- Write meaningful anchor text naming the source or concept (`"Google's Indexing API eligibility documentation"`, not raw naked URLs in body prose).
- Do not link to low-quality link farms, thin affiliate clones, or untrusted scraper sites.
- Keep outbound links purposeful—do not dump unrelated filler links just to hit a quota.
