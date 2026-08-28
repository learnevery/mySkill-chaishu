"""拆书报告骨架生成（chaishu new）。

骨架与 skills/chaishu/references/拆书报告模板.md 保持同构，
粗拆/深度细拆两种模式，生成到项目 拆书/ 目录。
"""
from __future__ import annotations

from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"
MODES = {"deep": ("深度细拆", "template-deep.md"), "rough": ("粗拆", "template-rough.md")}


def create_report(book: str, mode: str = "deep", out_dir: Path = Path("拆书"),
                  force: bool = False) -> Path:
    """生成报告骨架，返回文件路径。mode: deep | rough。"""
    if mode not in MODES:
        raise ValueError(f"未知模式：{mode}（可选 deep / rough）")
    mode_zh, template_name = MODES[mode]
    template = (_DATA_DIR / template_name).read_text(encoding="utf-8")
    content = template.replace("{书名}", book)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"拆书报告-{book}-{mode_zh}.md"
    if out_path.exists() and not force:
        raise FileExistsError(f"已存在 {out_path}（--force 覆盖）")
    out_path.write_text(content, encoding="utf-8")
    return out_path
