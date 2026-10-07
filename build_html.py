#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert ai-learning-notes.md -> self-contained dark-theme HTML with live Mermaid + interactive TOC."""
import re, html, sys

SRC = "/Users/vinces/WorkBuddy/2026-10-07-00-05-01/ai-learning-notes/ai-learning-notes.md"
OUT = "/Users/vinces/WorkBuddy/2026-10-07-00-05-01/ai-learning-notes/ai-learning-notes.html"

def slug(s):
    s = re.sub(r'[^\w\u4e00-\u9fff\- ]', '', s).strip().lower()
    s = re.sub(r'\s+', '-', s)
    return s or "sec"

def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t

lines = open(SRC, encoding='utf-8').read().split('\n')
out = []
toc = []
i = 0
n = len(lines)
in_code = False
code_buf = []
code_lang = ''
in_table = False
table_buf = []

def flush_table():
    global table_buf, in_table
    if not table_buf:
        in_table = False
        return
    rows = [r for r in table_buf if set(r.strip()) - {'|', '-', ':', ' '} or '|' in r]
    # parse
    html_rows = []
    data_rows = [r for r in table_buf if not re.match(r'^\s*\|?[\s:\-|]+\|?\s*$', r)]
    for idx, r in enumerate(data_rows):
        cells = [c.strip() for c in r.strip().strip('|').split('|')]
        tag = 'th' if idx == 0 else 'td'
        html_rows.append('<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells) + '</tr>')
    out.append('<table class="tbl"><thead>' + html_rows[0] + '</thead><tbody>' + ''.join(html_rows[1:]) + '</tbody></table>')
    table_buf = []
    in_table = False

while i < n:
    line = lines[i]
    if line.strip().startswith('```'):
        if not in_code:
            in_code = True
            code_lang = line.strip()[3:].strip()
            code_buf = []
        else:
            in_code = False
            block = '\n'.join(code_buf)
            if code_lang == 'mermaid':
                out.append('<div class="mermaid">\n' + block + '\n</div>')
            else:
                out.append('<pre class="code"><code>' + html.escape(block) + '</code></pre>')
            code_lang = ''
            code_buf = []
        i += 1
        continue
    if in_code:
        code_buf.append(line)
        i += 1
        continue
    # table
    if line.strip().startswith('|') and ('|' in line.strip()[1:]):
        if not in_table:
            in_table = True
            table_buf = []
        table_buf.append(line)
        i += 1
        continue
    else:
        if in_table:
            flush_table()
    # headings
    m = re.match(r'^(#{1,4})\s+(.*)$', line)
    if m:
        lvl = len(m.group(1))
        txt = m.group(2).strip()
        sid = slug(txt)
        # strip any trailing html-ish; keep text
        out.append(f'<h{lvl} id="{sid}">{inline(txt)}</h{lvl}>')
        if lvl <= 3:
            toc.append((lvl, sid, txt))
        i += 1
        continue
    # blockquote
    if line.startswith('>'):
        buf = []
        while i < n and lines[i].startswith('>'):
            buf.append(re.sub(r'^>\s?', '', lines[i]))
            i += 1
        out.append('<blockquote>' + ' '.join(inline(b) for b in buf) + '</blockquote>')
        continue
    # lists
    if re.match(r'^\s*[-*]\s+', line):
        buf = []
        while i < n and re.match(r'^\s*[-*]\s+', lines[i]):
            item = re.sub(r'^\s*[-*]\s+', '', lines[i])
            buf.append('<li>' + inline(item) + '</li>')
            i += 1
        out.append('<ul>' + ''.join(buf) + '</ul>')
        continue
    # blank
    if not line.strip():
        i += 1
        continue
    # paragraph
    out.append('<p>' + inline(line) + '</p>')
    i += 1
if in_table:
    flush_table()

body = '\n'.join(out)
toc_html = ''
for lvl, sid, txt in toc:
    cls = 'lvl' + str(lvl)
    toc_html += f'<li class="{cls}"><a href="#{sid}">{html.escape(txt)}</a></li>\n'

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 学习笔记 全流程体系化完整版</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
:root {{
  --bg:#0d1117; --bg2:#161b22; --fg:#e6edf3; --muted:#8b949e; --accent:#58a6ff;
  --green:#3fb950; --border:#30363d; --code:#1f2937;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; line-height:1.7; }}
header {{ padding:28px 32px; background:linear-gradient(135deg,#161b22,#0d1117); border-bottom:1px solid var(--border); }}
header h1 {{ margin:0 0 6px; font-size:26px; color:#fff; }}
header p {{ margin:0; color:var(--muted); font-size:14px; }}
.layout {{ display:flex; min-height:calc(100vh - 110px); }}
nav {{ width:280px; flex:none; border-right:1px solid var(--border); background:var(--bg2); padding:18px 14px; position:sticky; top:0; align-self:flex-start; max-height:100vh; overflow:auto; }}
nav h3 {{ font-size:13px; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; margin:4px 8px 10px; }}
nav ul {{ list-style:none; margin:0; padding:0; }}
nav li a {{ display:block; padding:5px 10px; color:var(--fg); text-decoration:none; border-radius:6px; font-size:13.5px; }}
nav li.lvl2 a {{ padding-left:10px; font-weight:600; }}
nav li.lvl3 a {{ padding-left:22px; font-size:12.5px; color:var(--muted); }}
nav li a:hover {{ background:#21323f; color:var(--accent); }}
main {{ flex:1; padding:28px 40px 80px; max-width:980px; }}
h1,h2,h3,h4 {{ color:#fff; line-height:1.35; scroll-margin-top:16px; }}
h2 {{ font-size:22px; margin-top:38px; padding-bottom:8px; border-bottom:2px solid var(--accent); }}
h3 {{ font-size:18px; margin-top:26px; color:#cdd9e5; }}
h4 {{ font-size:15px; color:var(--accent); }}
p {{ margin:12px 0; }}
a {{ color:var(--accent); }}
code {{ background:var(--code); padding:2px 6px; border-radius:4px; font-family:"SFMono-Regular",Consolas,monospace; font-size:13px; color:#ffa657; }}
pre.code {{ background:var(--code); padding:14px 16px; border-radius:8px; overflow:auto; border:1px solid var(--border); }}
pre.code code {{ color:#e6edf3; padding:0; background:none; }}
.tbl {{ border-collapse:collapse; width:100%; margin:16px 0; font-size:14px; }}
.tbl th,.tbl td {{ border:1px solid var(--border); padding:8px 11px; text-align:left; vertical-align:top; }}
.tbl th {{ background:#1c2530; color:#fff; }}
.tbl tbody tr:nth-child(even) {{ background:#11161d; }}
blockquote {{ border-left:4px solid var(--accent); background:#11161d; margin:14px 0; padding:10px 16px; color:var(--muted); border-radius:0 8px 8px 0; }}
.mermaid {{ background:var(--bg2); border:1px solid var(--border); border-radius:10px; padding:18px; margin:18px 0; text-align:center; overflow:auto; }}
.mermaid svg {{ max-width:100%; height:auto; }}
.foot {{ margin-top:50px; padding-top:18px; border-top:1px solid var(--border); color:var(--muted); font-size:13px; }}
@media (max-width:820px) {{ nav {{ display:none; }} main {{ padding:20px; }} }}
</style>
</head>
<body>
<header>
  <h1>AI 学习笔记 全流程体系化完整版</h1>
  <p>思维导图与流程图可视化版 · 由 4 份真实聊天导出提炼 · 109 个用户回合逐项可追溯</p>
</header>
<div class="layout">
<nav>
  <h3>目录导航</h3>
  <ul>{toc_html}</ul>
</nav>
<main>
{body}
<div class="foot">本页为 HTML 可视化版；同名 <code>.md</code> 与 <code>.docx</code> 为等效交付物。Mermaid 图表需联网加载（jsDelivr CDN）；若离线则显示源码。</div>
</main>
</div>
<script>
  if (window.mermaid) {{
    mermaid.initialize({{ startOnLoad:true, theme:'dark', securityLevel:'loose', flowchart:{{ curve:'basis' }} }});
  }}
</script>
</body>
</html>"""

open(OUT, 'w', encoding='utf-8').write(HTML)
print("WROTE", OUT, len(HTML), "bytes")
