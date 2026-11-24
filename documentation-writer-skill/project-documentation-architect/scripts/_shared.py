"""Shared pure-stdlib utilities for project-documentation-architect scripts."""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "out",
    ".nuxt",
    ".svelte-kit",
    ".astro",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "target",
    "coverage",
}

MANIFEST_FILES = (
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "go.mod",
    "Cargo.toml",
)

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


@dataclass
class ProjectUnit:
    """Detected application, service, or package inside a repository."""

    name: str
    location: str
    kind: str
    languages: List[str]
    frameworks: List[str]
    package_manager: Optional[str]
    scripts: Dict[str, str]
    entry_points: List[str]
    databases: List[str]
    env_vars: List[str]
    has_readme: bool
    doc_paths: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def read_text_safe(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_repo_files(root: Path, extensions: Optional[Iterable[str]] = None) -> List[Path]:
    ext_set = {e.lower() for e in extensions} if extensions else None
    results: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        for fname in sorted(filenames):
            p = Path(dirpath) / fname
            if ext_set is None or p.suffix.lower() in ext_set:
                results.append(p)
    return results


def _detect_pkg_manager(proj_dir: Path, root: Path, has_py: bool, has_go: bool, has_rust: bool) -> Optional[str]:
    for check_dir in (proj_dir, root):
        if (check_dir / "pnpm-lock.yaml").is_file():
            return "pnpm"
        if (check_dir / "yarn.lock").is_file():
            return "yarn"
        if (check_dir / "bun.lockb").is_file() or (check_dir / "bun.lock").is_file():
            return "bun"
        if (check_dir / "package-lock.json").is_file():
            return "npm"
        if (check_dir / "uv.lock").is_file():
            return "uv"
        if (check_dir / "poetry.lock").is_file():
            return "poetry"
    if (proj_dir / "package.json").is_file():
        return "npm"
    if has_py:
        return "pip"
    if has_go:
        return "go"
    if has_rust:
        return "cargo"
    return None


def _parse_env_example_vars(directory: Path) -> List[str]:
    vars_found: List[str] = []
    for fname in (".env.example", ".env.template", ".env.sample"):
        p = directory / fname
        if p.is_file():
            for line in read_text_safe(p).splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key = stripped.split("=", 1)[0].strip()
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key) and key not in vars_found:
                    vars_found.append(key)
    return vars_found


def _inspect_project_dir(proj_dir: Path, root: Path) -> ProjectUnit:
    rel_loc = "." if proj_dir == root else "./" + str(proj_dir.relative_to(root)).replace("\\", "/")
    name = root.name if proj_dir == root else proj_dir.name
    languages: List[str] = []
    frameworks: List[str] = []
    scripts: Dict[str, str] = {}
    databases: List[str] = []
    entry_points: List[str] = []

    pkg_file = proj_dir / "package.json"
    if pkg_file.is_file():
        languages.append("JavaScript/TypeScript" if (proj_dir / "tsconfig.json").is_file() else "JavaScript")
        try:
            pkg = json.loads(read_text_safe(pkg_file))
            if isinstance(pkg.get("name"), str) and pkg["name"].strip():
                name = pkg["name"].strip()
            if isinstance(pkg.get("scripts"), dict):
                scripts = {str(k): str(v) for k, v in pkg["scripts"].items()}
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            for dep, label in (
                ("next", "Next.js"),
                ("react", "React"),
                ("vue", "Vue"),
                ("nuxt", "Nuxt"),
                ("astro", "Astro"),
                ("@sveltejs/kit", "SvelteKit"),
                ("@nestjs/core", "NestJS"),
                ("express", "Express"),
                ("fastify", "Fastify"),
                ("hono", "Hono"),
                ("bullmq", "BullMQ"),
            ):
                if dep in deps and label not in frameworks:
                    frameworks.append(label)
            for dep, label in (
                ("@prisma/client", "Prisma"),
                ("prisma", "Prisma"),
                ("drizzle-orm", "Drizzle ORM"),
                ("mongoose", "Mongoose (MongoDB)"),
                ("pg", "PostgreSQL"),
                ("redis", "Redis"),
                ("ioredis", "Redis"),
            ):
                if dep in deps and label not in databases:
                    databases.append(label)
        except json.JSONDecodeError:
            pass

    has_py = (proj_dir / "pyproject.toml").is_file() or (proj_dir / "requirements.txt").is_file()
    if has_py:
        languages.append("Python")
        py_text = ""
        if (proj_dir / "pyproject.toml").is_file():
            py_text += read_text_safe(proj_dir / "pyproject.toml").lower()
        if (proj_dir / "requirements.txt").is_file():
            py_text += "\n" + read_text_safe(proj_dir / "requirements.txt").lower()
        for tok, label in (
            ("fastapi", "FastAPI"),
            ("django", "Django"),
            ("flask", "Flask"),
            ("celery", "Celery"),
            ("dramatiq", "Dramatiq"),
            ("sqlalchemy", "SQLAlchemy"),
            ("psycopg", "PostgreSQL"),
            ("pymongo", "MongoDB"),
            ("redis", "Redis"),
        ):
            if tok in py_text:
                target_list = databases if tok in {"sqlalchemy", "psycopg", "pymongo", "redis"} else frameworks
                if label not in target_list:
                    target_list.append(label)

    has_go = (proj_dir / "go.mod").is_file()
    if has_go:
        languages.append("Go")
        go_txt = read_text_safe(proj_dir / "go.mod").lower()
        for tok, label in (("gin-gonic", "Gin"), ("gofiber", "Fiber"), ("echo", "Echo")):
            if tok in go_txt:
                frameworks.append(label)

    has_rust = (proj_dir / "Cargo.toml").is_file()
    if has_rust:
        languages.append("Rust")
        cargo_txt = read_text_safe(proj_dir / "Cargo.toml").lower()
        for tok, label in (("axum", "Axum"), ("actix-web", "Actix Web"), ("sqlx", "SQLx")):
            if tok in cargo_txt:
                (databases if tok == "sqlx" else frameworks).append(label)

    if (proj_dir / "prisma" / "schema.prisma").is_file() and "Prisma" not in databases:
        databases.append("Prisma")

    for cand in (
        "src/index.ts",
        "src/index.js",
        "src/main.ts",
        "src/main.py",
        "app/layout.tsx",
        "src/app/layout.tsx",
        "app/main.py",
        "main.py",
        "main.go",
        "src/main.rs",
        "index.ts",
        "index.js",
    ):
        if (proj_dir / cand).is_file():
            entry_points.append(cand)

    folder_lower = proj_dir.name.lower()
    kind = "application"
    if "packages" in proj_dir.parts or folder_lower in {"shared", "common", "ui", "types"}:
        kind = "shared-package"
    elif any(k in folder_lower for k in ("worker", "jobs", "queue")) or any(f in frameworks for f in ("Celery", "BullMQ", "Dramatiq")):
        kind = "worker"
    elif any(k in folder_lower for k in ("backend", "api", "server")) or any(f in frameworks for f in ("Express", "NestJS", "FastAPI", "Django", "Flask", "Fastify", "Gin", "Axum")):
        kind = "backend"
    elif "admin" in folder_lower:
        kind = "admin-frontend"
    elif any(k in folder_lower for k in ("frontend", "web", "client")) or any(f in frameworks for f in ("Next.js", "React", "Vue", "Nuxt", "Astro", "SvelteKit")):
        kind = "frontend"

    doc_paths: List[str] = []
    if proj_dir != root and (proj_dir / "README.md").is_file():
        doc_paths.append(str((proj_dir / "README.md").relative_to(root)).replace("\\", "/"))
    elif proj_dir == root and (root / "README.md").is_file():
        doc_paths.append("README.md")

    docs_proj_dir = root / "docs" / "projects" / proj_dir.name
    if docs_proj_dir.is_dir():
        for md in sorted(docs_proj_dir.glob("*.md")):
            doc_paths.append(str(md.relative_to(root)).replace("\\", "/"))

    pkg_mgr = _detect_pkg_manager(proj_dir, root, has_py, has_go, has_rust)
    return ProjectUnit(
        name=name,
        location=rel_loc,
        kind=kind,
        languages=languages or ["Unknown"],
        frameworks=frameworks,
        package_manager=pkg_mgr,
        scripts=scripts,
        entry_points=entry_points,
        databases=databases,
        env_vars=_parse_env_example_vars(proj_dir),
        has_readme=bool(doc_paths),
        doc_paths=doc_paths,
    )


def discover_projects(root: Path) -> Tuple[List[ProjectUnit], Dict[str, Any]]:
    """Discover all applications/services/packages and repository-level metadata."""
    manifest_dirs: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        cur = Path(dirpath)
        rel_depth = len(cur.relative_to(root).parts)
        if rel_depth > 2:
            dirnames[:] = []
            continue
        if any(m in filenames for m in MANIFEST_FILES):
            manifest_dirs.append(cur)

    sub_projects = [d for d in manifest_dirs if d != root]
    has_workspace_cfg = any(
        (root / f).is_file() for f in ("pnpm-workspace.yaml", "turbo.json", "nx.json", "lerna.json")
    )
    root_has_workspaces = False
    if (root / "package.json").is_file():
        try:
            root_pkg = json.loads(read_text_safe(root / "package.json"))
            root_has_workspaces = "workspaces" in root_pkg
        except json.JSONDecodeError:
            pass

    if sub_projects and (has_workspace_cfg or root_has_workspaces or root not in manifest_dirs):
        project_dirs = sub_projects
    else:
        project_dirs = manifest_dirs

    units = [_inspect_project_dir(d, root) for d in sorted(set(project_dirs))]

    has_compose = (root / "docker-compose.yml").is_file() or (root / "docker-compose.yaml").is_file()
    compose_services: List[str] = []
    for cname in ("docker-compose.yml", "docker-compose.yaml"):
        cpath = root / cname
        if cpath.is_file():
            in_services = False
            for line in read_text_safe(cpath).splitlines():
                if re.match(r"^services:\s*$", line):
                    in_services = True
                    continue
                if in_services and re.match(r"^[A-Za-z0-9_-]+:", line):
                    in_services = False
                elif in_services:
                    sm = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
                    if sm:
                        compose_services.append(sm.group(1))

    has_shared = any(u.kind == "shared-package" for u in units) or (root / "packages").is_dir() or (root / "shared").is_dir()

    if len(units) <= 1 and not compose_services:
        topology = "Single Application"
    elif has_workspace_cfg or root_has_workspaces or has_compose or has_shared:
        topology = "Monorepo / Multi-Service"
    else:
        topology = "Multiple Independent Projects"

    infra = {
        "docker_compose": has_compose,
        "compose_services": compose_services,
        "dockerfile": (root / "Dockerfile").is_file() or any((d / "Dockerfile").is_file() for d in project_dirs),
        "ci_workflows": [str(p.relative_to(root)).replace("\\", "/") for p in (root / ".github" / "workflows").glob("*.yml")] if (root / ".github" / "workflows").is_dir() else [],
        "root_env_vars": _parse_env_example_vars(root),
        "root_readme": (root / "README.md").is_file(),
        "docs_files": [str(p.relative_to(root)).replace("\\", "/") for p in iter_repo_files(root, {".md"})],
        "topology": topology,
    }
    return units, infra


def strip_markdown_code(md_text: str) -> str:
    """Remove fenced code blocks and inline code spans so examples do not trigger false link checks."""
    no_fences = re.sub(r"```.*?```", "", md_text, flags=re.DOTALL)
    return re.sub(r"`[^`\n]+`", "", no_fences)


def extract_markdown_anchors(md_text: str) -> Set[str]:
    """Compute GitHub-style heading anchors from a Markdown document."""
    no_fences = re.sub(r"```.*?```", "", md_text, flags=re.DOTALL)
    anchors: Set[str] = set()
    for line in no_fences.splitlines():
        m = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if m:
            raw = m.group(1).strip().lower()
            slug = re.sub(r"[^\w\s-]", "", raw)
            slug = re.sub(r"\s+", "-", slug).strip("-")
            if slug:
                anchors.add(slug)
    return anchors
