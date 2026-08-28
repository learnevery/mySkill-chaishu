"""Markdown 子集解析与 HTML 渲染。

只实现拆书报告实际用到的语法子集：标题、段落、粗体/斜体/行内代码、
链接、有序/无序列表（支持一级嵌套）、表格、引用块、围栏代码块、水平线。

与 skills/chaishu/references/html输出规范.md 保持一致：
- "作者为什么这么安排"等反推结论段落自动渲染为 callout 组件；
- 表格渲染为 .tbl-wrap 结构，空单元格补 "—"；
- 代码块渲染为 .formula 组件。
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from typing import List

BLOCK_HEADING = "heading"
BLOCK_PARA = "para"
BLOCK_LIST = "list"
BLOCK_TABLE = "table"
BLOCK_QUOTE = "quote"
BLOCK_CODE = "code"
BLOCK_HR = "hr"

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_HR_RE = re.compile(r"^ {0,3}(?:-{3,}|\*{3,}|_{3,})$")
_UL_RE = re.compile(r"^(\s*)[-*+]\s+(.+)$")
_OL_RE = re.compile(r"^(\s*)(\d+)[.、)]\s+(.+)$")
_TABLE_SEP_RE = re.compile(r"^[\s:|\-]+$")
_CALLOUT_RE = re.compile(r"^\*\*(?:作者为什么这么安排|为什么[^*]{0,16}|分布规律)\*\*")


@dataclass
class Block:
    """一个块级元素。"""

    type: str
    text: str = ""
    level: int = 0
    # list: [(ordered: bool, depth: int, text: str)]
    items: list = field(default_factory=list)
    head: list = field(default_factory=list)
    rows: list = field(default_factory=list)
    lines: list = field(default_factory=list)


def _split_table_row(line: str) -> List[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def parse_blocks(text: str) -> List[Block]:
    """把 Markdown 文本解析为块级元素列表。"""
    blocks: List[Block] = []
    para: List[str] = []
    in_code = False
    code_lines: List[str] = []
    quote_lines: List[str] = []
    list_items: List[tuple] = []
    table_lines: List[str] = []

    def flush_para():
        nonlocal para
        if para:
            blocks.append(Block(BLOCK_PARA, text="\n".join(para).strip()))
            para = []

    def flush_list():
        nonlocal list_items
        if list_items:
            blocks.append(Block(BLOCK_LIST, items=list(list_items)))
            list_items = []

    def flush_table():
        nonlocal table_lines
        if table_lines:
            rows = [_split_table_row(l) for l in table_lines if not _TABLE_SEP_RE.match(l)]
            blocks.append(Block(BLOCK_TABLE, head=rows[0], rows=rows[1:]))
            table_lines = []

    def flush_quote():
        nonlocal quote_lines
        if quote_lines:
            blocks.append(Block(BLOCK_QUOTE, lines=list(quote_lines)))
            quote_lines = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")

        if in_code:
            if line.strip().startswith("```"):
                blocks.append(Block(BLOCK_CODE, lines=code_lines))
                code_lines = []
                in_code = False
            else:
                code_lines.append(line)
            continue

        if line.strip().startswith("```"):
            flush_para(); flush_list(); flush_table(); flush_quote()
            in_code = True
            continue

        stripped = line.strip()

        # 表格行
        if stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 2:
            flush_para(); flush_list(); flush_quote()
            table_lines.append(line)
            continue
        elif table_lines:
            flush_table()

        if not stripped:
            flush_para(); flush_list(); flush_quote()
            continue

        m = _HEADING_RE.match(line)
        if m:
            flush_para(); flush_list(); flush_quote()
            blocks.append(Block(BLOCK_HEADING, text=m.group(2).strip(), level=len(m.group(1))))
            continue

        if _HR_RE.match(line):
            flush_para(); flush_list(); flush_quote()
            blocks.append(Block(BLOCK_HR))
            continue

        if stripped.startswith(">"):
            flush_para(); flush_list()
            quote_lines.append(re.sub(r"^\s*>\s?", "", line))
            continue
        elif quote_lines:
            flush_quote()

        m = _UL_RE.match(line)
        if m:
            flush_para()
            list_items.append((False, len(m.group(1)) // 2, m.group(2).strip()))
            continue
        m = _OL_RE.match(line)
        if m:
            flush_para()
            list_items.append((True, len(m.group(1)) // 2, m.group(3).strip()))
            continue

        if list_items:
            # 列表后的普通行视为列表延续段落（少见），合并进最后一项
            list_items[-1] = (list_items[-1][0], list_items[-1][1],
                              list_items[-1][2] + " " + stripped)
            continue

        para.append(line)

    if in_code and code_lines:
        blocks.append(Block(BLOCK_CODE, lines=code_lines))
    flush_para(); flush_list(); flush_table(); flush_quote()
    return blocks


def render_inline(text: str) -> str:
    """行内元素：转义 → 行内代码 → 链接 → 粗体 → 斜体。"""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def _render_list(items: List[tuple], check: bool = False) -> str:
    """渲染列表。check=True 时按内化行动清单样式渲染（.check + .num）。"""
    if check:
        parts = ['<ul class="check">']
        n = 0
        for _, depth, txt in items:
            if depth > 0:
                continue
            n += 1
            parts.append(f'<li><span class="num">{n}.</span>{render_inline(txt)}</li>')
        parts.append("</ul>")
        return "".join(parts)

    out = []
    i = 0

    def render_level(depth: int) -> str:
        nonlocal i
        ordered = items[i][0]
        tag = "ol" if ordered else "ul"
        parts = [f"<{tag}>"]
        while i < len(items) and items[i][1] == depth and items[i][0] == ordered:
            txt = items[i][2]
            i += 1
            inner = render_inline(txt)
            if i < len(items) and items[i][1] > depth:
                inner += render_level(items[i][1])
            parts.append(f"<li>{inner}</li>")
        parts.append(f"</{tag}>")
        return "".join(parts)

    while i < len(items):
        out.append(render_level(items[i][1]))
    return "".join(out)


def _render_table(head: List[str], rows: List[List[str]]) -> str:
    def cell(c: str) -> str:
        return render_inline(c) if c else "—"

    th = "".join(f"<th>{render_inline(h)}</th>" for h in head)
    trs = []
    for row in rows:
        tds = "".join(f"<td>{cell(c)}</td>" for c in row)
        trs.append(f"<tr>{tds}</tr>")
    return (
        '<div class="tbl-wrap"><table><thead>'
        f"<tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table></div>"
    )


def render_inner(blocks: List[Block], check_lists: bool = False) -> str:
    """渲染 section 内部内容（h3 及以下块级元素）。"""
    parts: List[str] = []
    for b in blocks:
        if b.type == BLOCK_HEADING:
            if b.level == 3:
                parts.append(f"<h3>{render_inline(b.text)}</h3>")
            elif b.level == 4:
                parts.append(f"<h4>{render_inline(b.text)}</h4>")
            else:
                parts.append(f"<p><strong>{render_inline(b.text)}</strong></p>")
        elif b.type == BLOCK_PARA:
            if _CALLOUT_RE.match(b.text):
                parts.append(f'<div class="callout">{render_inline(b.text)}</div>')
            else:
                for seg in b.text.split("\n"):
                    parts.append(f"<p>{render_inline(seg)}</p>")
        elif b.type == BLOCK_LIST:
            parts.append(_render_list(b.items, check=check_lists))
        elif b.type == BLOCK_TABLE:
            parts.append(_render_table(b.head, b.rows))
        elif b.type == BLOCK_QUOTE:
            inner = "<br>".join(render_inline(l) for l in b.lines if l.strip())
            parts.append(f'<div class="lead">{inner}</div>')
        elif b.type == BLOCK_CODE:
            code = html.escape("\n".join(b.lines), quote=False)
            parts.append(f'<div class="formula">{code}</div>')
        # BLOCK_HR：section 之间的分隔线，HTML 中由卡片布局承担，跳过
    return "\n".join(p for p in parts if p)
