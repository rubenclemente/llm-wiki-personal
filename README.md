# LLM Wiki Personal

A personal knowledge base powered by LLM agents, based on [Andrej Karpathy's](https://karpathy.ai/) LLM wiki proposal.

## Quick Start

```bash
cd labs/llm-wiki-personal && docker-compose up -d
```

Access wiki at: **http://localhost:8082**

## Architecture

**Three layers:**

1. **raw/** - Your immutable source documents (articles, papers, notes)
2. **wiki/** - LLM-generated markdown pages (summaries, entities, concepts)
3. **AGENTS.md** - Schema telling LLM how to maintain the wiki

## How It Works

This is NOT a script-based system. You interact directly with an LLM agent:

1. **Add sources**: Drop markdown/notes to `raw/` folder
2. **Ingest**: Ask LLM to process/ingest the source
   - LLM finds uningested files, processes them
   - Creates wiki/summaries/, wiki/concepts/ pages
   - Updates wiki/index.md and wiki/log.md
   - **Runs `python scripts/md2html.py`** to regenerate HTML
3. **Query**: Ask questions against the wiki
4. **Browse**: View wiki at http://localhost:8082

## Example LLM Conversations

**Ingest specific source:**
> "Please ingest the neural-networks.md file in raw/. Create/update relevant wiki pages, update index.md, log the ingest, then run the HTML generator."

**Ingest all pending sources:**
> "Please ingest all pending sources in raw/. Check wiki/summaries/ to find which files haven't been ingested yet, process each one, then regenerate HTML."

**Query:**
> "What's the difference between feedforward and recurrent neural networks? Check the wiki and cite sources."

**Lint:**
> "Please lint the wiki - check for contradictions, orphan pages, and missing cross-references."

## Folder Structure

| Directory | Purpose |
|----------|---------|
| `raw/` | Source documents (immutable) |
| `wiki/` | LLM-generated markdown (source of truth) |
| `wiki/summaries/` | Source summaries |
| `wiki/concepts/` | Concept pages |
| `wiki/index.md` | Catalog of all wiki pages |
| `wiki/log.md` | Activity log |
| `public/` | Generated HTML (served by nginx) |
| `scripts/md2html.py` | Converts wiki/ markdown to public/ HTML |

## Web Interface

The wiki is served via nginx at http://localhost:8082:

- **Main index**: Cards showing all summaries and concepts
- **Detail pages**: Generated HTML with Key Takeaways, Source Notes
- **Navigation**: "← Back to Index" links

### Manual HTML Regeneration

After any edits to wiki/ markdown files, regenerate HTML:

```bash
cd labs/llm-wiki-personal
python scripts/md2html.py
```

This creates HTML files in `public/` folder.

## Operations

**Ingest**: LLM reads source → creates/updates wiki pages → runs HTML generator → updates index

**Query**: Ask LLM to search wiki → synthesize answer → optionally file new pages

**Lint**: Check for contradictions, orphaned pages, missing links

## Key Insight

The wiki is a **persistent, compounding artifact**. Cross-references exist. Contradictions flagged. Knowledge compiled once, kept current.

- You curate sources and ask questions
- LLM does all the grunt work: summarizing, cross-referencing, maintenance, HTML generation

## Workflow Summary

1. Add source files to `raw/`
2. Ask LLM to ingest (specifies "after ingest, run python scripts/md2html.py")
3. LLM processes files → updates wiki/ → runs HTML generator
4. View results at http://localhost:8082

## Requirements

- AGENTS.md schema (included)
- LLM access (for natural language processing)