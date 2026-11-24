"""Image asset, alt text, filename, licensing, and storage validation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from _shared import (  # noqa: E402
    Issue,
    format_report,
    is_http_url,
    iter_repo_files,
    parse_frontmatter_and_body,
    parse_html,
    read_text_safe,
)

MD_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
GENERIC_NAME_RE = re.compile(r"^(?:img[_-]?\d+|image\d*|screenshot.*|untitled.*|photo\d*)\.", re.IGNORECASE)
HEAVY_FORMATS = {".bmp", ".tiff", ".tif"}
NEXT_IMAGE_RE = re.compile(r"<Image\b([^>]+)>")


def _check_image_entry(
    rel: str,
    src: str,
    alt: Optional[str],
    repo_path: Optional[Path],
    file_parent: Path,
    width: Optional[str] = None,
    height: Optional[str] = None,
) -> List[Issue]:
    issues: List[Issue] = []
    if not src:
        issues.append(Issue("Image missing src", "High", rel, "Empty image path", "Provide valid local asset path or licensed media URL."))
        return issues

    if alt is None or alt.strip() == "":
        issues.append(
            Issue(
                "Content image missing descriptive alt text",
                "Medium",
                rel,
                f'Image "{src}" has empty or missing alt text',
                "Describe what the visual shows clearly for accessibility and image search.",
            )
        )

    if is_http_url(src):
        issues.append(
            Issue(
                "External image hotlink detected",
                "High",
                rel,
                f'Image points to external URL "{src}"',
                "Download/store approved licensed media locally in public/assets or CMS media storage instead of hotlinking.",
            )
        )
    elif repo_path is not None:
        clean_src = src.split("?", 1)[0].split("#", 1)[0]
        if clean_src.startswith("/"):
            candidates = [repo_path / "public" / clean_src.lstrip("/"), repo_path / clean_src.lstrip("/")]
        else:
            candidates = [file_parent / clean_src, repo_path / "public" / clean_src]
        if not any(c.is_file() for c in candidates):
            issues.append(
                Issue(
                    "Referenced local image asset does not exist",
                    "Critical",
                    rel,
                    f'Asset "{src}" not found in repository public/assets paths',
                    "Save the approved image file to the repository's image folder before publishing.",
                )
            )

    filename = Path(src.split("?", 1)[0]).name
    if GENERIC_NAME_RE.match(filename):
        issues.append(
            Issue(
                "Non-descriptive image filename",
                "Low",
                rel,
                f'Filename "{filename}" is generic',
                "Rename using descriptive lowercase hyphenated words (e.g., warehouse-nvr-setup.webp).",
            )
        )
    if Path(filename).suffix.lower() in HEAVY_FORMATS:
        issues.append(
            Issue(
                "Unoptimized image format",
                "Medium",
                rel,
                f'Image "{filename}" uses uncompressed format',
                "Convert to WebP or AVIF for fast web delivery.",
            )
        )
    if width is not None and height is not None and (not width or not height):
        issues.append(
            Issue(
                "HTML <img> missing explicit width/height",
                "Low",
                rel,
                f'Image "{src}" lacks width or height attributes',
                "Specify width and height (or aspect ratio) to prevent Cumulative Layout Shift.",
            )
        )
    return issues


def run_image_validation(target: str, repo_root: Optional[str] = None, manifest: Optional[str] = None) -> Tuple[List[Issue], Dict[str, str]]:
    issues: List[Issue] = []
    path = Path(target).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    repo_path = Path(repo_root).resolve() if repo_root else (path if path.is_dir() else path.parent)
    files = [path] if path.is_file() else iter_repo_files(path, {".md", ".mdx", ".html", ".htm"})

    img_count = 0
    for f in files:
        rel = f.name if path.is_file() else str(f.relative_to(path))
        txt = read_text_safe(f)
        if f.suffix.lower() in {".html", ".htm"}:
            parsed = parse_html(txt)
            for img in parsed.images:
                img_count += 1
                issues.extend(
                    _check_image_entry(
                        rel,
                        img.get("src") or "",
                        img.get("alt"),
                        repo_path,
                        f.parent,
                        img.get("width") or "",
                        img.get("height") or "",
                    )
                )
        else:
            fm, body = parse_frontmatter_and_body(txt)
            og_img = fm.get("ogImage")
            if og_img:
                img_count += 1
                issues.extend(_check_image_entry(rel, og_img, "Open Graph image", repo_path, f.parent))
            for m in MD_IMG_RE.finditer(body):
                img_count += 1
                issues.extend(_check_image_entry(rel, m.group(2), m.group(1), repo_path, f.parent))
            for jm in NEXT_IMAGE_RE.finditer(body):
                attrs = jm.group(1)
                src_m = re.search(r'src=["\']([^"\']+)["\']', attrs)
                alt_m = re.search(r'alt=["\']([^"\']*)["\']', attrs)
                if src_m:
                    img_count += 1
                    issues.extend(_check_image_entry(rel, src_m.group(1), alt_m.group(1) if alt_m else None, repo_path, f.parent))

    if manifest:
        mpath = Path(manifest).resolve()
        if not mpath.is_file():
            raise FileNotFoundError(f"Image manifest does not exist: {manifest}")
        entries = json.loads(read_text_safe(mpath))
        for idx, item in enumerate(entries if isinstance(entries, list) else []):
            if not item.get("license") or not item.get("source_url"):
                issues.append(
                    Issue(
                        "Image manifest entry missing license or source_url",
                        "High",
                        f"{mpath.name}[{idx}]",
                        f"Missing license/source_url for asset {item.get('filename')}",
                        "Verify exact license, source URL, and attribution before publishing.",
                    )
                )

    return issues, {"Mode": "Image & License Audit", "Files Scanned": str(len(files)), "Images Checked": str(img_count)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate image existence, alt text, formats, and licensing manifests.")
    parser.add_argument("target", help="Content file or directory")
    parser.add_argument("--repo", help="Repository root for resolving public/ image paths")
    parser.add_argument("--manifest", help="Optional JSON image licensing manifest path")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        issues, summary = run_image_validation(args.target, repo_root=args.repo, manifest=args.manifest)
    except Exception as exc:
        print(f"Error validating images: {exc}", file=sys.stderr)
        return 1

    print(format_report("Image & Licensing Validation", args.target, issues, summary, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
