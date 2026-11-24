# Worked Example: Multiple Unrelated Projects in One Workspace (Scenario 3)

Demonstrates isolating unrelated projects (`ecommerce/`, `portfolio/`, `chatbot/`) inside a shared workspace directory without inventing fake cross-service dependencies.

## Generated Documentation Tree

```text
workspace/
├── README.md                 # Minimal workspace directory index ONLY
├── ecommerce/
│   └── README.md             # Independent Next.js + Stripe store docs
├── portfolio/
│   └── README.md             # Independent Astro static site docs
└── chatbot/
    └── README.md             # Independent Python FastAPI bot docs
```

## Excerpt: Workspace Root `README.md`

```markdown
# Workspace Projects

Independent applications maintained inside this workspace. Each project uses its own runtime, dependencies, and setup guide.

| Project | Location | Stack | Documentation |
|---|---|---|---|
| E-Commerce Store | `ecommerce/` | Next.js + PostgreSQL | [ecommerce/README.md](ecommerce/README.md) |
| Developer Portfolio | `portfolio/` | Astro + Markdown | [portfolio/README.md](portfolio/README.md) |
| Support Chatbot | `chatbot/` | Python FastAPI | [chatbot/README.md](chatbot/README.md) |
```
