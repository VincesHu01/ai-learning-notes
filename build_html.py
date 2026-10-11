#!/usr/bin/env python3
"""Build the two static, navigable HTML editions in this repository."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent

DOCUMENTS = (
    {
        "source": ROOT / "ai-learning-notes.md",
        "outputs": (ROOT / "index.html", ROOT / "ai-learning-notes.html"),
        "title": "AI 学习笔记：全流程体系化完整版",
        "subtitle": "从大模型基础到智能体工程 · 思维导图与流程图可视化版",
        "description": "系统理解人工智能底层原理、训练、智能体、推理服务与产品工程。",
        "active_section": "principles",
    },
    {
        "source": ROOT / "ai-product-manager-playbook.md",
        "outputs": (ROOT / "ai-product-manager-playbook.html",),
        "title": "AI 产品经理系统化知识与求职实战手册",
        "subtitle": "从技术原理到产品指标、评测、优化、商业化与面试表达",
        "description": "把人工智能底层知识翻译为产品决策、指标体系、优化动作和求职证据。",
        "active_section": "product",
    },
)


def slugify(value: str, used: dict[str, int]) -> str:
    base = re.sub(r"[^\w\u4e00-\u9fff\- ]", "", value).strip().lower()
    base = re.sub(r"\s+", "-", base) or "section"
    used[base] = used.get(base, 0) + 1
    return base if used[base] == 1 else f"{base}-{used[base]}"


def render_inline(value: str) -> str:
    placeholders: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00CODE{len(placeholders) - 1}\x00"

    value = re.sub(r"`([^`]+)`", stash_code, value)
    value = html.escape(value, quote=False)
    value = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}">'
            f"{match.group(1)}</a>"
        ),
        value,
    )
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", value)
    value = re.sub(
        r"\[\^([^\]]+)\]",
        lambda match: (
            f'<sup id="ref-{match.group(1)}"><a href="#note-{match.group(1)}">'
            f"[{match.group(1)}]</a></sup>"
        ),
        value,
    )
    for index, placeholder in enumerate(placeholders):
        value = value.replace(f"\x00CODE{index}\x00", placeholder)
    return value


def extract_footnotes(lines: list[str]) -> tuple[list[str], list[tuple[str, str]]]:
    body: list[str] = []
    notes: list[tuple[str, str]] = []
    for line in lines:
        match = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", line)
        if match:
            notes.append((match.group(1), match.group(2)))
        else:
            body.append(line)
    return body, notes


def markdown_to_html(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines, footnotes = extract_footnotes(markdown.splitlines())
    output: list[str] = []
    toc: list[tuple[int, str, str]] = []
    used_slugs: dict[str, int] = {}
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            code: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            index += 1
            block = "\n".join(code)
            if language == "mermaid":
                output.append(f'<div class="mermaid">\n{block}\n</div>')
            else:
                lang_class = f' class="language-{html.escape(language)}"' if language else ""
                output.append(f"<pre><code{lang_class}>{html.escape(block)}</code></pre>")
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            rows: list[str] = []
            while index < len(lines):
                candidate = lines[index].strip()
                if not (candidate.startswith("|") and "|" in candidate[1:]):
                    break
                rows.append(candidate)
                index += 1
            data_rows = [row for row in rows if not re.match(r"^\|?[\s:\-|]+\|?$", row)]
            if data_rows:
                rendered_rows: list[str] = []
                for row_index, row in enumerate(data_rows):
                    tag = "th" if row_index == 0 else "td"
                    cells = [cell.strip() for cell in row.strip("|").split("|")]
                    rendered_rows.append(
                        "<tr>"
                        + "".join(f"<{tag}>{render_inline(cell)}</{tag}>" for cell in cells)
                        + "</tr>"
                    )
                output.append(
                    '<div class="table-wrap"><table><thead>'
                    + rendered_rows[0]
                    + "</thead><tbody>"
                    + "".join(rendered_rows[1:])
                    + "</tbody></table></div>"
                )
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            section_id = slugify(text, used_slugs)
            output.append(f'<h{level} id="{section_id}">{render_inline(text)}</h{level}>')
            if level <= 3:
                toc.append((level, section_id, text))
            index += 1
            continue

        if re.match(r"^\s*[-*]\s+", line):
            items: list[str] = []
            while index < len(lines) and re.match(r"^\s*[-*]\s+", lines[index]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[index])
                items.append(f"<li>{render_inline(item)}</li>")
                index += 1
            output.append("<ul>" + "".join(items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items: list[str] = []
            while index < len(lines) and re.match(r"^\s*\d+\.\s+", lines[index]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[index])
                items.append(f"<li>{render_inline(item)}</li>")
                index += 1
            output.append("<ol>" + "".join(items) + "</ol>")
            continue

        if line.startswith(">"):
            quotes: list[str] = []
            while index < len(lines) and lines[index].startswith(">"):
                quotes.append(re.sub(r"^>\s?", "", lines[index]))
                index += 1
            output.append("<blockquote>" + "<br>".join(render_inline(q) for q in quotes) + "</blockquote>")
            continue

        if stripped in {"<details>", "</details>"}:
            output.append(stripped)
            index += 1
            continue

        if re.match(r'^<a id="[^"]+"></a>$', stripped):
            output.append(stripped)
            index += 1
            continue

        summary = re.match(r"^<summary>(.*)</summary>$", stripped)
        if summary:
            summary_text = re.sub(r"</?strong>", "**", summary.group(1))
            output.append(f"<summary>{render_inline(summary_text)}</summary>")
            index += 1
            continue

        if re.match(r"^---+$", stripped):
            output.append("<hr>")
            index += 1
            continue

        if not stripped:
            index += 1
            continue

        output.append(f"<p>{render_inline(line)}</p>")
        index += 1

    if footnotes:
        output.append('<section class="footnotes" aria-labelledby="footnotes-title">')
        output.append('<h2 id="footnotes-title">参考注释</h2><ol>')
        for note_id, note in footnotes:
            escaped_id = html.escape(note_id, quote=True)
            output.append(
                f'<li id="note-{escaped_id}">{render_inline(note)} '
                f'<a class="footnote-back" href="#ref-{escaped_id}" aria-label="返回引用位置">↩</a></li>'
            )
        output.append("</ol></section>")

    return "\n".join(output), toc


def build_document(config: dict[str, object]) -> str:
    source = Path(config["source"])
    body, toc = markdown_to_html(source.read_text(encoding="utf-8"))
    toc_html = "\n".join(
        f'<li class="level-{level}"><a href="#{section_id}">{html.escape(text)}</a></li>'
        for level, section_id, text in toc
    )
    active_section = str(config["active_section"])
    section_links = (
        ("principles", "AI 原理", "index.html"),
        ("product", "AI 产品", "ai-product-manager-playbook.html"),
    )
    section_switcher_parts: list[str] = []
    for key, label, href in section_links:
        active_class = " is-active" if key == active_section else ""
        current_page = ' aria-current="page"' if key == active_section else ""
        section_switcher_parts.append(
            f'<a class="section-tab{active_class}" href="{href}"{current_page}>'
            f'{html.escape(label)}</a>'
        )
    section_switcher = "\n".join(section_switcher_parts)
    title = html.escape(str(config["title"]))
    subtitle = html.escape(str(config["subtitle"]))
    description = html.escape(str(config["description"]), quote=True)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{description}">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
:root {{ color-scheme:dark; --bg:#091019; --panel:#101923; --panel-soft:#141f2c; --text:#e8eef5; --muted:#9eacbb; --accent:#67adff; --accent-strong:#3f93f3; --border:#27384b; --code:#1a2736; --max:1160px; --sidebar:316px; }}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0; background:linear-gradient(180deg,#0b121b 0,#091019 340px); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; line-height:1.75; }}
.skip-link {{ position:absolute; left:-9999px; top:8px; }}
.skip-link:focus {{ left:12px; z-index:20; padding:8px 12px; background:#fff; color:#000; border-radius:6px; }}
header {{ padding:24px clamp(22px,4vw,56px); background:radial-gradient(circle at 84% -20%,#1d4875 0,transparent 36%),linear-gradient(135deg,#142131,#0c141f); border-bottom:1px solid var(--border); }}
.hero {{ width:100%; max-width:1480px; margin:auto; display:grid; grid-template-columns:minmax(0,1fr) minmax(260px,320px); align-items:center; gap:28px; }}
.hero-copy {{ min-width:0; }}
header h1 {{ margin:0 0 6px; color:#fff; font-size:clamp(25px,3.2vw,38px); letter-spacing:-.025em; }}
header p {{ margin:0; color:var(--muted); font-size:14px; }}
.author {{ margin-top:6px; color:#c9d1d9; font-weight:600; }}
.section-switcher {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; padding:6px; border:1px solid #31465e; border-radius:14px; background:rgba(8,15,24,.72); box-shadow:0 12px 30px rgba(0,0,0,.18); }}
.section-tab {{ display:flex; align-items:center; justify-content:center; min-height:46px; padding:9px 18px; border:1px solid transparent; border-radius:9px; color:#c5d0dc; font-weight:750; letter-spacing:.02em; text-decoration:none; transition:background .18s ease,color .18s ease,transform .18s ease; }}
.section-tab:hover {{ color:#fff; background:#1b2b3d; transform:translateY(-1px); }}
.section-tab.is-active {{ color:#07111f; background:linear-gradient(135deg,#79bcff,#4c9cf5); box-shadow:0 5px 16px rgba(63,147,243,.28); }}
.section-tab:focus-visible {{ outline:3px solid rgba(121,192,255,.55); outline-offset:3px; }}
.layout {{ display:grid; grid-template-columns:var(--sidebar) minmax(0,1fr); min-height:calc(100vh - 136px); }}
nav {{ position:sticky; top:0; align-self:start; max-height:100vh; overflow:auto; padding:24px 18px 48px; background:linear-gradient(180deg,#111b27,#0e1721); border-right:1px solid var(--border); scrollbar-width:thin; scrollbar-color:#536274 transparent; }}
nav h2 {{ margin:0 10px 12px; font-size:13px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; border:0; padding:0; }}
nav ul {{ margin:0; padding:0; list-style:none; }}
nav a {{ display:block; padding:6px 10px; color:var(--text); border-radius:7px; text-decoration:none; font-size:13px; line-height:1.5; }}
nav a:hover {{ color:var(--accent); background:#1b2a3a; }}
nav .level-1 a {{ font-weight:800; }}
nav .level-2 a {{ font-weight:650; }}
nav .level-3 a {{ padding-left:23px; color:var(--muted); font-size:12px; }}
main {{ width:100%; max-width:var(--max); padding:42px clamp(30px,5vw,72px) 96px; overflow:hidden; }}
h1,h2,h3,h4 {{ color:#fff; line-height:1.35; scroll-margin-top:18px; }}
main h1 {{ font-size:30px; margin-top:0; }}
main h2 {{ margin-top:44px; padding-bottom:9px; border-bottom:2px solid var(--accent); font-size:23px; }}
main h3 {{ margin-top:30px; color:#d5e4f3; font-size:19px; }}
main h4 {{ margin-top:24px; color:var(--accent); font-size:16px; }}
p {{ margin:12px 0; }}
a {{ color:var(--accent); }}
strong {{ color:#fff; }}
code {{ padding:2px 6px; border-radius:5px; background:var(--code); color:#ffad66; font-family:"SFMono-Regular",Consolas,monospace; font-size:.9em; }}
pre {{ overflow:auto; padding:16px; border:1px solid var(--border); border-radius:10px; background:var(--code); }}
pre code {{ padding:0; color:var(--text); background:none; }}
.table-wrap {{ width:100%; overflow-x:auto; margin:18px 0; }}
table {{ width:100%; border-collapse:collapse; min-width:620px; font-size:14px; }}
th,td {{ padding:9px 11px; border:1px solid var(--border); text-align:left; vertical-align:top; }}
th {{ color:#fff; background:#1c2938; }}
tbody tr:nth-child(even) {{ background:#101720; }}
blockquote {{ margin:16px 0; padding:11px 17px; border-left:4px solid var(--accent); border-radius:0 9px 9px 0; color:#c1cad5; background:#111a24; }}
hr {{ margin:32px 0; border:0; border-top:1px solid var(--border); }}
li {{ margin:5px 0; }}
.mermaid {{ margin:20px 0; padding:20px; overflow:auto; border:1px solid var(--border); border-radius:12px; background:var(--panel); text-align:center; }}
.mermaid svg {{ max-width:100%; height:auto; }}
details {{ margin:16px 0 22px; padding:12px 16px; border:1px solid #284967; border-radius:10px; background:#101820; }}
summary {{ cursor:pointer; color:#79c0ff; font-weight:700; }}
.footnotes {{ margin-top:60px; color:#bac5d1; font-size:14px; }}
.footnotes h2 {{ font-size:21px; }}
.footnote-back {{ text-decoration:none; }}
.page-foot {{ margin-top:60px; padding-top:18px; border-top:1px solid var(--border); color:var(--muted); font-size:13px; }}
@media (min-width:1760px) {{ :root {{ --sidebar:336px; --max:1240px; }} }}
@media (max-width:900px) {{
  header {{ padding:22px 20px; }}
  .hero {{ grid-template-columns:1fr; gap:18px; }}
  .section-switcher {{ width:100%; max-width:380px; }}
  .layout {{ display:block; }}
  nav {{ position:relative; max-height:300px; padding:18px 14px 28px; border-right:0; border-bottom:1px solid var(--border); }}
  main {{ margin:auto; padding:30px 20px 72px; }}
  main h1 {{ font-size:26px; }}
}}
@media (max-width:420px) {{ .section-tab {{ min-height:44px; padding-inline:10px; }} }}
</style>
</head>
<body>
<a class="skip-link" href="#content">跳到正文</a>
<header><div class="hero">
  <div class="hero-copy">
    <h1>{title}</h1>
    <p>{subtitle}</p>
    <p class="author">本笔记由 VincesHu 胡中岳整理</p>
  </div>
  <div class="section-switcher" role="navigation" aria-label="知识库内容切换">{section_switcher}</div>
</div></header>
<div class="layout">
  <nav aria-label="文章目录"><h2>目录导航</h2><ul>{toc_html}</ul></nav>
  <main id="content">{body}<div class="page-foot">本页由仓库内构建脚本自动生成，流程图由 Mermaid 在浏览器中渲染。</div></main>
</div>
<script>
if (window.mermaid) {{ mermaid.initialize({{ startOnLoad:true, theme:"dark", securityLevel:"loose", flowchart:{{ curve:"basis" }} }}); }}
</script>
</body>
</html>
"""


def main() -> None:
    for config in DOCUMENTS:
        rendered = build_document(config)
        for output in config["outputs"]:
            Path(output).write_text(rendered, encoding="utf-8")
            print(f"WROTE {Path(output).name}: {len(rendered):,} bytes")


if __name__ == "__main__":
    main()
