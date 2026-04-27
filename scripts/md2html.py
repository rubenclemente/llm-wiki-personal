#!/usr/bin/env python3
"""Generate HTML pages from markdown to a separate public/ folder."""

from pathlib import Path
import re
import json
from datetime import date

CSS = '''
<style>
:root { --bg-color: #0d1117; --text-color: #c9d1d9; --link-color: #58a6ff; --border-color: #30363d; --card-bg: #161b22; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: var(--bg-color); color: var(--text-color); line-height: 1.6; padding: 2rem; }
.container { max-width: 800px; margin: 0 auto; }
h1 { font-size: 1.8rem; margin-bottom: 0.5rem; color: #fff; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem; }
.meta { font-size: 0.85rem; color: #6e7681; margin-bottom: 1.5rem; }
.section { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem; }
.section h2 { font-size: 1.1rem; color: var(--link-color); margin-bottom: 0.75rem; }
ul { margin-left: 1.5rem; }
li { margin-bottom: 0.5rem; }
a { color: var(--link-color); text-decoration: none; }
a:hover { text-decoration: underline; }
.back-link { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border-color); }
.back-link a { color: #8b949e; }
</style>'''

INDEX_CSS = '''
<style>
:root { --bg-color: #0d1117; --text-color: #c9d1d9; --link-color: #58a6ff; --border-color: #30363d; --card-bg: #161b22; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: var(--bg-color); color: var(--text-color); line-height: 1.6; padding: 2rem; }
.container { max-width: 900px; margin: 0 auto; }
h1 { font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(90deg, #58a6ff, #a371f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { color: #8b949e; margin-bottom: 2rem; }
.section-title { font-size: 1.3rem; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border-color); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }
.card { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; transition: transform 0.2s, box-shadow 0.2s; }
.card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.card h2 { font-size: 1rem; margin-bottom: 0.5rem; color: #fff; }
.card a { color: var(--link-color); text-decoration: none; }
.card a:hover { text-decoration: underline; }
.card p { color: #8b949e; font-size: 0.9rem; }
footer { text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-color); color: #8b949e; font-size: 0.85rem; }
</style>'''

def parse_md(content):
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            content = content[end+3:]
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Untitled'
    
    sections = []
    current = {'title': '', 'items': []}
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('## '):
            if current['title']:
                sections.append(current)
            current = {'title': line[3:], 'items': []}
        elif line.startswith('- '):
            current['items'].append(line[2:])
    
    if current['title']:
        sections.append(current)
    
    return title, sections

def make_html(title, sections, source_path, today, back_depth):
    html_sections = []
    for sec in sections:
        items = ''.join(f'<li>{item}</li>' for item in sec['items'])
        html_sections.append(f'<div class="section"><h2>{sec["title"]}</h2><ul>{items}</ul></div>')
    
    back_link = "../" * back_depth + "index.html"
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | LLM Wiki</title>
{CSS}
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p class="meta">Source: {source_path} · Date: {today}</p>
        {''.join(html_sections)}
        <div class="back-link"><a href="{back_link}">← Back to Index</a></div>
    </div>
</body>
</html>'''

def make_index(summaries, concepts, today):
    summary_cards = ''
    for s in summaries:
        summary_cards += f'''<div class="card">
            <h2><a href="summaries/{s['file']}">{s['name']}</a></h2>
            <p>{s['desc']}</p>
        </div>'''
    
    concept_cards = ''
    for c in concepts:
        concept_cards += f'''<div class="card">
            <h2><a href="concepts/{c['file']}">{c['name']}</a></h2>
            <p>{c['desc']}</p>
        </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Wiki Personal</title>
{INDEX_CSS}
</head>
<body>
    <div class="container">
        <h1>LLM Wiki Personal</h1>
        <p class="subtitle">A personal knowledge base built with Karpathy's LLM Wiki pattern</p>

        <h2 class="section-title">Summaries</h2>
        <div class="grid">
            {summary_cards}
        </div>

        <h2 class="section-title">Concepts</h2>
        <div class="grid">
            {concept_cards}
        </div>

        <h2 class="section-title">Index & Log</h2>
        <div class="grid">
            <div class="card">
                <h2><a href="log.html">log</a></h2>
                <p>Activity log</p>
            </div>
        </div>

        <footer>
            <p>Built with Karpathy's LLM Wiki pattern</p>
        </footer>
    </div>
</body>
</html>'''

def make_log(entries, today):
    entries_html = ''
    for e in entries:
        items = ''.join(f'<li>{i}</li>' for i in e['items'])
        entries_html += f'''<div class="entry">
            <h2>{e['title']}</h2>
            <ul>{items}</ul>
        </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>log | LLM Wiki</title>
    <style>
    :root {{ --bg-color: #0d1117; --text-color: #c9d1d9; --link-color: #58a6ff; --border-color: #30363d; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg-color); color: var(--text-color); line-height: 1.6; padding: 2rem; }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    h1 {{ font-size: 1.8rem; color: #fff; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem; margin-bottom: 1.5rem; }}
    .entry {{ margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); }}
    .entry h2 {{ font-size: 1rem; color: var(--link-color); margin-bottom: 0.5rem; }}
    ul {{ margin-left: 1.25rem; }}
    a {{ color: var(--link-color); text-decoration: none; }}
    .back {{ margin-top: 2rem; }}
    .back a {{ color: #8b949e; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Activity Log</h1>
        {entries_html}
        <div class="back">
            <a href="index.html">← Back to Index</a>
        </div>
    </div>
</body>
</html>'''

def main():
    script_dir = Path(__file__).parent
    wiki_dir = script_dir.parent / 'wiki'
    public_dir = script_dir.parent / 'public'
    
    public_dir.mkdir(exist_ok=True)
    
    today = date.today().isoformat()
    
    summaries = []
    concepts = []
    entries = []
    
    # Process markdown files (in subdirectories)
    for md in wiki_dir.rglob('*.md'):
        if md.name in ('index.md', 'log.md') or md.parent == wiki_dir:
            continue  # Skip root files - handled separately
        
        content = md.read_text()
        title, sections = parse_md(content)
        
        # Determine output path and back depth
        rel_path = md.relative_to(wiki_dir)
        output_dir = public_dir / rel_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Calculate back depth: how many levels deep from root
        # Files in subdirectories need at least one level up
        if rel_path.parent == wiki_dir:
            back_depth = 0  # Root files
        else:
            back_depth = max(1, len(rel_path.parent.parts) - 1)
        
        source_path = str(rel_path).replace('.md', '.md')
        html_path = output_dir / f"{md.stem}.html"
        
        html = make_html(title, sections, source_path, today, back_depth)
        html_path.write_text(html)
        
        # Collect for index
        first_item = sections[0]['items'][0] if sections and sections[0]['items'] else ''
        
        if 'summaries' in str(md):
            summaries.append({'name': md.stem, 'file': f"{md.stem}.html", 'desc': first_item[:50] + '...' if len(first_item) > 50 else first_item})
        elif 'concepts' in str(md):
            concepts.append({'name': md.stem, 'file': f"{md.stem}.html", 'desc': first_item[:50] + '...' if len(first_item) > 50 else first_item})
        elif md.name == 'log.md':
            for sec in sections:
                title = sec['title']
                entries.append({'title': title, 'items': sec['items']})
        elif md.name == 'index.md':
            pass  # Skip - index is generated separately
        else:
            pass  # Other root files skipped
        
        print(f'Created: {html_path.name}')
    
    # Generate index.html
    index_html = make_index(summaries, concepts, today)
    (public_dir / 'index.html').write_text(index_html)
    print('Created: index.html')
    
    # Generate log.html
    log_html = make_log(entries, today)
    (public_dir / 'log.html').write_text(log_html)
    print('Created: log.html')

if __name__ == '__main__':
    main()