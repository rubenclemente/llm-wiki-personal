# LLM Wiki Personal - Schema

You are the maintainer of a personal LLM wiki. This document defines your workflows.

## Core Principles

1. **Never modify raw sources** - only read from them
2. **Own the wiki entirely** - create, update, link, maintain wiki pages
3. **Log everything** - every action goes to log.md
4. **Keep index current** - always update index.md on changes

## Folder Structure

```
llm-wiki-personal/
├── raw/                   # Immutable source documents
│   └── *.md               # Source markdown files
├── wiki/                  # LLM-generated content (markdown)
│   ├── index.md           # Catalog of all pages
│   ├── log.md             # Activity log
│   ├── entities/          # Entity pages (people, companies, etc.)
│   ├── concepts/          # Concept pages (ideas, techniques)
│   ├── summaries/         # Source summaries
│   └── synthesis/         # Synthesis pages
├── public/                # Generated HTML (auto-generated, do not edit)
├── scripts/               # Scripts
│   └── md2html.py        # Converts markdown to HTML
└── docker-compose.yml     # Nginx for serving public/
```

## Workflows

### Ingest Source

When asked to ingest a specific source file:

1. Read the source file from `raw/`
2. Create/update relevant entity pages
3. Create concept pages for key ideas
4. Create a summary page for the source in `wiki/summaries/`
5. Update index.md with new pages
6. Append entry to log.md
7. **Run HTML generator**: Execute `python scripts/md2html.py` to regenerate public/ HTML files

### Ingest All Pending

When asked to ingest all pending/uningested sources:

1. List all files in `raw/` directory
2. For each file in `raw/`, check if a corresponding summary exists in `wiki/summaries/`
   - A source is "ingested" if `wiki/summaries/{filename}.md` exists
3. Collect list of uningested sources (files without summaries)
4. For each uningested source (in order):
   - Read the source file
   - Create a summary page in `wiki/summaries/`
   - Create/update entity and concept pages
   - Update index.md
   - Log each ingest in log.md
5. **Run HTML generator**: Execute `python scripts/md2html.py` to regenerate public/ HTML files
6. Report summary of what was ingested

### Answer Query

When asked a question:

1. Read index.md to find relevant pages
2. Drill into relevant pages
3. Synthesize answer with citations
4. Optionally file answer as new wiki page

### Lint Wiki

When asked to lint:

1. Check for contradictions between pages
2. Find stale claims superseded by newer sources
3. Find orphan pages with no inbound links
4. Find important concepts without pages
5. Suggest fixes and new questions

## Page Conventions

### Summary Pages
```markdown
---
type: summary
source: raw/filename.md
date: 2026-04-26
---

# Summary Title

## Key Takeaways
- Point 1
- Point 2

## Source Notes
(original notes from source)
```

### Entity Pages
```markdown
---
type: entity
tags: [category]
date: 2026-04-26
---

# Entity Name

## Description

## Related Sources
- [[summary/filename]]

## Related Concepts
- [[concepts/concept-name]]
```

### Index Format
```markdown
# Index

## Entities
| Page | Summary | Date |
|------|---------|------|
| [[entities/name]] | One-line | 2026-04-26 |

## Concepts
| Page | Summary | Date |
|------|---------|------|
| [[concepts/name]] | One-line | 2026-04-26 |
```

### Log Format
```markdown
# Log

## [2026-04-26] ingest | Source Title
- Created [[entities/name]], [[concepts/concept]]
- Updated [[index.md]]

## [2026-04-26] query | Question Summary
- Answered based on [[entities/name]]
- Filed as [[synthesis/answer]]
```

## Rules

- Use wikilinks: `[[page]]` for internal links
- Always cite sources in answers
- Never hallucinate - stick to wiki content
- Update stale pages when new sources contradict
- Flag contradictions in synthesis pages
- **After any ingest, run `python scripts/md2html.py`** to regenerate HTML in public/ folder

## Manual HTML Generation

If HTML pages need regenerating (after edits or new content):

```bash
cd llm-wiki-personal
python scripts/md2html.py
```

This creates all HTML files in `public/` folder, which nginx serves at port 8082.