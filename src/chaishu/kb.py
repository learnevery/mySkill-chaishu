"""拆书知识库入库：把报告中的五大维度精华追加到知识库文件。

确定性规则入库（不依赖 AI），映射关系与
skills/chaishu-builder 的五大知识库一致，并扩展"范式"一库：

- 人设.md   ← "人设体系拆解"（其中"金手指"小节单独入金手指库）
- 金手指.md ← "金手指"小节
- 节奏.md   ← "节奏与情绪曲线拆解"（其中"爽点/铺垫释放"小节入爽点库）
- 爽点.md   ← "爽点 / 铺垫·释放"小节
- 剧情.md   ← "大纲与故事结构拆解"
- 范式.md   ← "可复用范式清单"
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .mdrender import BLOCK_HEADING, parse_blocks
from .render import extract_meta

KB_FILES = ("人设", "剧情", "爽点", "节奏", "金手指", "范式")


def split_units(md_text: str) -> List[Tuple[str, str]]:
    """切分为 (标题, 正文) 单元：h2 为大单元，其下 h3 为子单元。"""
    units: List[Tuple[str, str]] = []
    cur_title: Optional[str] = None
    cur_lines: List[str] = []
    sub_title: Optional[str] = None
    sub_lines: List[str] = []

    def flush_sub():
        nonlocal sub_title, sub_lines
        if sub_title is not None and any(l.strip() for l in sub_lines):
            units.append((sub_title, "\n".join(sub_lines).strip()))
        sub_title, sub_lines = None, []

    def flush_all():
        flush_sub()
        nonlocal cur_title, cur_lines
        if cur_title is not None and any(l.strip() for l in cur_lines):
            units.append((cur_title, "\n".join(cur_lines).strip()))
        cur_title, cur_lines = None, []

    for b in parse_blocks(md_text):
        if b.type == BLOCK_HEADING and b.level == 2:
            flush_all()
            cur_title = re.sub(r"^[一二三四五六七八九十]+、\s*", "", b.text).strip()
        elif b.type == BLOCK_HEADING and b.level == 3:
            flush_sub()
            sub_title = b.text.strip()
        else:
            if cur_title is None:
                continue  # 报告前言（已进封面/元数据）
            if b.type == "hr":
                continue
            text = _block_markdown(b)
            if text:
                if sub_title is not None:
                    sub_lines.append(text)
                else:
                    cur_lines.append(text)
    flush_all()
    return units


def _block_markdown(b) -> str:
    """把块元素还原回 markdown 文本（入库保留可读源码）。"""
    if b.type == "para":
        return b.text
    if b.type == "heading":
        return f"#### {b.text}"
    if b.type == "list":
        lines = []
        for ordered, depth, text in b.items:
            prefix = "  " * depth + ("1. " if ordered else "- ")
            lines.append(prefix + text)
        return "\n".join(lines)
    if b.type == "table":
        rows = [b.head] + b.rows
        return "\n".join("| " + " | ".join(r) + " |" for r in rows)
    if b.type == "quote":
        return "\n".join("> " + l for l in b.lines)
    if b.type == "code":
        return "\n".join(b.lines)
    return ""


def classify(unit_title: str) -> Optional[str]:
    t = unit_title
    if "金手指" in t:
        return "金手指"
    if "爽点" in t or ("铺垫" in t and "释放" in t) or "高潮分布" in t:
        return "爽点"
    if "人设" in t or "主角" in t or "反派" in t or "配角" in t or "冲突来源" in t:
        return "人设"
    if "节奏" in t or "情绪" in t or "钩子" in t:
        return "节奏"
    if "大纲" in t or "故事结构" in t or "主线" in t or "危机递进" in t or "桥段" in t or "转折" in t:
        return "剧情"
    if "范式" in t or "公式" in t or "模块" in t:
        return "范式"
    return None


def extract_kb_entries(md_text: str, source_name: str) -> Dict[str, str]:
    """从报告提取各知识库条目，返回 {知识库名: 追加文本}。"""
    meta = extract_meta(md_text)
    book = meta.get("book") or source_name
    buckets: Dict[str, List[str]] = {}
    for title, body in split_units(md_text):
        target = classify(title)
        if not target or not body.strip():
            continue
        buckets.setdefault(target, []).append(f"### {title}\n\n{body}")
    entries = {}
    for name, chunks in buckets.items():
        entries[name] = (
            f"\n## 《{book}》 - 拆书积累\n\n"
            f"> 来源：{source_name}\n\n" + "\n\n".join(chunks) + "\n\n---\n"
        )
    return entries


def kb_add(md_text: str, md_path: Path, kb_dir: Path, force: bool = False) -> List[str]:
    """入库：返回写入摘要行。重复入库（知识库已有该书条目）默认跳过。"""
    meta = extract_meta(md_text)
    book = meta.get("book") or md_path.stem
    entries = extract_kb_entries(md_text, md_path.name)
    kb_dir.mkdir(parents=True, exist_ok=True)

    report = []
    for name in KB_FILES:
        if name not in entries:
            continue
        kb_file = kb_dir / f"{name}.md"
        existing = kb_file.read_text(encoding="utf-8") if kb_file.exists() else ""
        if f"《{book}》" in existing and not force:
            report.append(f"跳过 {name}.md：已有《{book}》条目（--force 可覆盖追加）")
            continue
        with kb_file.open("a", encoding="utf-8") as f:
            f.write(entries[name])
        report.append(f"{name}.md ← 追加《{book}》条目")
    return report


def kb_stats(kb_dir: Path) -> List[str]:
    """统计知识库各文件的条目数。"""
    lines = []
    for name in KB_FILES:
        kb_file = kb_dir / f"{name}.md"
        if not kb_file.exists():
            lines.append(f"{name}.md：0 条（未创建）")
            continue
        text = kb_file.read_text(encoding="utf-8")
        count = len(re.findall(r"^## 《.+?》", text, re.M))
        lines.append(f"{name}.md：{count} 条 · {len(text.splitlines())} 行")
    return lines
