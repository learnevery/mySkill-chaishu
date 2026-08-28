"""拆书报告 Markdown → 精排版 HTML 渲染。

读取 src/chaishu/data/report-template.html（与技能内
assets/report-template.html 同源），保留其全部 CSS、导航结构与折叠脚本，
只替换正文内容：封面、目录导航、九大 section、页脚红线声明。
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Tuple

from .mdrender import (
    BLOCK_HEADING,
    BLOCK_QUOTE,
    parse_blocks,
    render_inline,
)

_TEMPLATE_PATH = Path(__file__).parent / "data" / "report-template.html"

_ZH_DIGITS = "零一二三四五六七八九"


def zh_num(n: int) -> str:
    """1-99 的中文数字（用于章节序号）。"""
    if n <= 0:
        return _ZH_DIGITS[0]
    if n < 10:
        return _ZH_DIGITS[n]
    if n < 20:
        return "十" + (_ZH_DIGITS[n % 10] if n % 10 else "")
    tens, ones = divmod(n, 10)
    return _ZH_DIGITS[tens] + "十" + (_ZH_DIGITS[ones] if ones else "")


def load_template(path: Optional[str] = None) -> str:
    p = Path(path) if path else _TEMPLATE_PATH
    return p.read_text(encoding="utf-8")


def _strip_title_suffix(title: str) -> str:
    """导航用短标题：去掉"一、"前缀与"（维度一）"后缀。"""
    t = re.sub(r"^[一二三四五六七八九十]+、\s*", "", title)
    t = re.sub(r"（[^（）]*）$", "", t).strip()
    return t


def extract_meta(md_text: str) -> dict:
    """从报告头部（h1 + 引用块 + 基本信息）尽力提取封面元数据。"""
    meta = {
        "h1": "",
        "mode": "深度细拆",
        "book": "",
        "author": "—",
        "category": "—",
        "words": "—",
        "chapters": "—",
        "reading": "—",
        "rating": "—",
        "scope": "—",
        "goal": "",
    }
    blocks = parse_blocks(md_text)
    for b in blocks:
        if b.type == BLOCK_HEADING and b.level == 1 and not meta["h1"]:
            meta["h1"] = b.text
            m = re.match(r"(粗拆|深度细拆)报告[：:]\s*(.+)$", b.text)
            if m:
                meta["mode"], meta["book"] = m.group(1), m.group(2).strip()
            else:
                meta["book"] = b.text
        if b.type == BLOCK_HEADING and b.level == 2:
            # “基本信息”在第一节内，元数据扫描不在此截断
            pass
        if b.type == BLOCK_QUOTE:
            for line in b.lines:
                if "拆解对象" in line:
                    m = re.search(r"拆解对象[：:]\s*([^《\n]+)《", line)
                    if m:
                        meta["author"] = m.group(1).strip()
                    m = re.search(r"(\d+(?:\.\d+)?)\s*万字", line)
                    if m:
                        meta["words"] = m.group(1) + "万字"
                    m = re.search(r"(\d+)\s*章", line)
                    if m:
                        meta["chapters"] = m.group(1) + "章"
                    m = re.search(r"在读\s*([\d.]+\s*万?)", line)
                    if m:
                        meta["reading"] = "在读" + m.group(1).strip()
                    m = re.search(r"评分\s*([\d.]+)", line)
                    if m:
                        meta["rating"] = m.group(1)
                elif "拆解范围" in line:
                    m = re.search(r"拆解范围[：:]\s*(.+)$", line)
                    if m:
                        meta["scope"] = m.group(1).strip()
                elif "拆解目标" in line:
                    m = re.search(r"拆解目标[：:]\s*(.+)$", line)
                    if m:
                        meta["goal"] = m.group(1).strip()
        if b.type == "para" and "**基本信息**" in b.text:
            m = re.search(r"分类\s*([^\s/／、,，]+)", b.text)
            if m:
                meta["category"] = m.group(1)
        if b.type == "list":
            for _, _, item_text in b.items:
                if "**基本信息**" in item_text:
                    m = re.search(r"分类\s*([^\s/／、,，]+)", item_text)
                    if m:
                        meta["category"] = m.group(1)
    return meta


def split_sections(blocks) -> List[Tuple[str, list]]:
    """按 h2 切分为 (标题, 内部块列表)。h2 之前的前言块丢弃（已进封面）。"""
    sections: List[Tuple[str, list]] = []
    current: Optional[Tuple[str, list]] = None
    for b in blocks:
        if b.type == BLOCK_HEADING and b.level == 2:
            if current:
                sections.append(current)
            current = (b.text, [])
        elif current is not None:
            current[1].append(b)
    if current:
        sections.append(current)
    return sections


def _build_cover(meta: dict) -> str:
    sub = meta["goal"] or meta["category"]
    meta_spans = (
        f'<span><b>作者</b>　{render_inline(meta["author"])}</span>'
        f'<span><b>分类</b>　{render_inline(meta["category"])}</span>'
        f'<span><b>字数</b>　{render_inline(meta["words"])}</span>'
        f'<span><b>章节</b>　{render_inline(meta["chapters"])}</span>'
        f'<span><b>在读</b>　{render_inline(meta["reading"])}</span>'
        f'<span><b>评分</b>　{render_inline(meta["rating"])}</span>'
        f'<span><b>拆解范围</b>　{render_inline(meta["scope"])}</span>'
    )
    return (
        '<div class="cover">'
        f'<span class="tag">拆书 · {meta["mode"]}报告</span>'
        f'<h1>{render_inline(meta["h1"] or meta["book"])}</h1>'
        f'<div class="sub">{render_inline(sub)}</div>'
        f'<div class="meta">{meta_spans}</div>'
        "</div>"
    )


def _build_nav(section_titles: List[str]) -> str:
    links = []
    for i, title in enumerate(section_titles, 1):
        links.append(
            f'<a href="#s{i}"><span class="n">{zh_num(i)}</span>'
            f"{_strip_title_suffix(title)}</a>"
        )
    return (
        '<nav id="nav">'
        '<div class="nav-head"><h4>目录</h4>'
        '<button class="nav-toggle" id="navToggle" type="button" '
        'aria-label="折叠/展开导航" title="折叠导航">‹</button></div>'
        f'<div class="nav-body">{"".join(links)}</div>'
        "</nav>"
    )


def _build_footer(meta: dict, template_html: str) -> str:
    m = re.search(r"<footer>(.*?)</footer>", template_html, re.S)
    if not m:
        return ""
    footer = m.group(1)
    footer = footer.replace("【作者】", meta["author"])
    footer = footer.replace("【书名】", meta["book"])
    footer = footer.replace("【拆解范围】", meta["scope"])
    return f"<footer>{footer}</footer>"


def render_report_html(md_text: str, template_html: Optional[str] = None) -> Tuple[str, dict]:
    """返回 (完整 HTML 字符串, 封面元数据)。"""
    from .mdrender import render_inner

    if template_html is None:
        template_html = load_template()

    meta = extract_meta(md_text)
    sections = split_sections(parse_blocks(md_text))

    section_htmls = []
    for i, (title, inner_blocks) in enumerate(sections, 1):
        check_lists = "内化" in title
        body = render_inner(inner_blocks, check_lists=check_lists)
        section_htmls.append(
            f'<section id="s{i}">'
            f'<h2><span class="idx">{zh_num(i)}</span>{render_inline(title)}</h2>'
            f"{body}</section>"
        )

    head_end = template_html.index("<body>") + len("<body>")
    head = template_html[:head_end].replace("【书名】", meta["book"])
    tail = template_html[template_html.index("<script>"):]

    body = (
        '<div class="wrap"><main>'
        + _build_cover(meta)
        + _build_nav([t for t, _ in sections])
        + "\n".join(section_htmls)
        + _build_footer(meta, template_html)
        + "</main></div>"
    )
    return head + body + tail, meta
