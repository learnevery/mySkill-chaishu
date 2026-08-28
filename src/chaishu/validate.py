"""拆书报告完整性校验。

执行 skills/chaishu 的硬性规则：报告必须包含"可复用范式""仿写训练"
"内化行动清单"，否则等于白拆；深度细拆的逐章标记表必须含"作者目的"列。
"""
from __future__ import annotations

import re
from typing import List, Tuple

from .mdrender import BLOCK_HEADING, BLOCK_TABLE, parse_blocks
from .render import extract_meta

# (级别, 章节关键词, 说明)
_DEEP_REQUIREMENTS = [
    ("书籍信息", "选书理由"),
    ("卖点", "核心卖点与开篇（维度一）"),
    ("人设", "人设体系拆解（维度二）"),
    ("节奏", "节奏与情绪曲线拆解（维度三）"),
    ("大纲", "大纲与故事结构拆解（维度四）"),
    ("赛道", "赛道读者偏好分析（维度五）"),
    ("范式", "可复用范式清单"),
    ("仿写", "仿写训练"),
    ("内化", "内化行动清单"),
]
_ROUGH_REQUIREMENTS = [
    ("书籍信息", "书籍信息"),
    ("开篇任务", "开篇任务"),
    ("卖点", "核心卖点"),
    ("人设", "主要人设"),
    ("节奏", "开篇节奏"),
    ("范式", "可复用范式"),
    ("结论", "一句话结论"),
]


def validate_report(md_text: str) -> Tuple[bool, List[Tuple[str, str]]]:
    """返回 (是否通过, [(级别, 说明), ...])，级别为 OK/WARN/FAIL。"""
    meta = extract_meta(md_text)
    mode = "粗拆" if "粗拆" in meta.get("mode", "") else "深度细拆"
    blocks = parse_blocks(md_text)

    h2_titles = [b.text for b in blocks if b.type == BLOCK_HEADING and b.level == 2]
    joined = "\n".join(h2_titles)
    results: List[Tuple[str, str]] = []

    if not meta.get("h1"):
        results.append(("FAIL", "缺少一级标题（应为“# 深度细拆报告：书名”格式）"))

    if re.search(r"\{[^}\n]+\}", md_text):
        results.append(("FAIL", "仍含未填写的占位符 {…}（先补齐书籍信息与逐章标记）"))

    reqs = _ROUGH_REQUIREMENTS if mode == "粗拆" else _DEEP_REQUIREMENTS
    for keyword, desc in reqs:
        ok = keyword in joined
        if not ok and not any(keyword in t for t in h2_titles):
            results.append(("FAIL", f"缺少章节：{desc}"))
        else:
            results.append(("OK", f"章节齐全：{desc}"))

    tables = [b for b in blocks if b.type == BLOCK_TABLE]
    if mode == "深度细拆":
        has_purpose_col = any("作者目的" in cell for t in tables for cell in t.head)
        if has_purpose_col:
            results.append(("OK", "逐章标记表含“作者目的”列"))
        else:
            results.append(("FAIL", "深度细拆缺少含“作者目的”列的逐章标记表"))

    # 仿写与内化必须有实质内容
    for keyword in ("仿写", "内化"):
        section = _section_body(blocks, keyword)
        if section is None:
            continue
        plain = re.sub(r"[#*>|\-\s]", "", section)
        if keyword == "仿写" and len(plain) < 300:
            results.append(("WARN", f"“{keyword}”章节内容偏少（仿写片段建议 300-800 字）"))
        elif keyword == "内化" and len(plain) < 30:
            results.append(("WARN", f"“{keyword}”章节内容偏少"))
        else:
            results.append(("OK", f"“{keyword}”章节有实质内容"))

    passed = not any(level == "FAIL" for level, _ in results)
    return passed, results


def _section_body(blocks, keyword: str):
    idx = next((i for i, b in enumerate(blocks)
                if b.type == BLOCK_HEADING and b.level == 2 and keyword in b.text), None)
    if idx is None:
        return None
    parts = []
    for b in blocks[idx + 1:]:
        if b.type == BLOCK_HEADING and b.level == 2:
            break
        parts.append(getattr(b, "text", "") or "\n".join(getattr(b, "lines", []) or []))
    return "\n".join(parts)
