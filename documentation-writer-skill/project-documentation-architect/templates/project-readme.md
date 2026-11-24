# Template: Per-Project `README.md`

Use this concise structure for each independent application, service, or shared package:

```markdown
# <Application / Service Name>

<1–2 sentence description of this project's purpose and boundaries.>

## Project Overview

- **Responsibilities:** `<What this app owns>`
- **Technologies:** `<Verified stack & runtime versions>`
- **Related Projects:** `<APIs, shared packages, or services it depends on>`

## Getting Started

### Prerequisites
- `<Verified runtime/tool versions from package.json / pyproject.toml / Dockerfile>`

### Commands (Verified)
~~~bash
# Install dependencies
<verified install command>

# Run local development server
<verified dev command>

# Build for production
<verified build command>

# Run tests
<verified test command>
~~~

## Directory Structure

~~~text
<app>/
├── src/               # <Responsibility>
├── tests/             # <Test suite>
└── ...
~~~

## Application Workflow

1. `<Entry point initialization>`
2. `<Routing / request or job processing>`
3. `<Persistence / downstream integration>`

## Important Modules & Further Docs

- [Environment Variables](<environment.md>)
- [API Reference](<api.md>) *(include only if applicable)*
- [Database Guide](<database.md>) *(include only if applicable)*
- [Development & Testing](<development.md>) *(include only if applicable)*
```
