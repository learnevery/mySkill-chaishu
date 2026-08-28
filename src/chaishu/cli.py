"""chaishu 命令行入口。

子命令：
  new       生成拆书报告骨架（粗拆 / 深度细拆）
  build     拆书报告 Markdown → 精排版 HTML
  validate  校验报告完整性（范式/仿写/内化/作者目的列）
  kb add    报告五大维度精华入库（人设/剧情/爽点/节奏/金手指/范式）
  kb stats  知识库统计
  pack      把 skills/ 下技能目录打成可导入的 zip
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .kb import kb_add, kb_stats
from .pack import pack_skills
from .render import render_report_html
from .report import create_report
from .validate import validate_report


def _stdout_utf8():
    # Windows 控制台默认 GBK，中文输出可能报错
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def cmd_new(args) -> int:
    try:
        path = create_report(args.book, mode=args.mode, out_dir=Path(args.out_dir),
                             force=args.force)
    except FileExistsError as e:
        print(f"✗ {e}")
        return 1
    print(f"✓ 已生成报告骨架：{path}")
    print(f"  下一步：填写正文 → chaishu build \"{path}\"")
    return 0


def cmd_build(args) -> int:
    md_path = Path(args.report)
    if not md_path.exists():
        print(f"✗ 文件不存在：{md_path}")
        return 1
    md_text = md_path.read_text(encoding="utf-8")
    html_text, meta = render_report_html(md_text, template_html=args.template)
    out = Path(args.out) if args.out else md_path.with_suffix(".html")
    out.write_text(html_text, encoding="utf-8")
    print(f"✓ HTML 已生成：{out}")
    print(f"  书名：{meta['book']} · 模式：{meta['mode']} · 章节：{html_text.count('<section id=')}")
    return 0


def cmd_validate(args) -> int:
    md_path = Path(args.report)
    if not md_path.exists():
        print(f"✗ 文件不存在：{md_path}")
        return 1
    passed, results = validate_report(md_path.read_text(encoding="utf-8"))
    mark = {"OK": "✓", "WARN": "!", "FAIL": "✗"}
    for level, msg in results:
        print(f" [{mark[level]}] {msg}")
    print("校验通过" if passed else "校验未通过：报告缺少必要章节/表格，补齐后再入库")
    return 0 if passed else 1


def cmd_kb(args) -> int:
    if args.kb_cmd == "stats":
        kb_dir = Path(args.kb_dir)
        if not kb_dir.is_dir():
            print(f"知识库目录不存在：{kb_dir}")
            return 1
        for line in kb_stats(kb_dir):
            print(f" {line}")
        return 0

    md_path = Path(args.report)
    if not md_path.exists():
        print(f"✗ 文件不存在：{md_path}")
        return 1
    report = kb_add(md_path.read_text(encoding="utf-8"), md_path,
                    Path(args.kb_dir), force=args.force)
    if not report:
        print("未提取到可入库内容：请确认报告包含人设/节奏/大纲/范式等章节")
        return 1
    print("📚 拆书经验入库完成：")
    for line in report:
        print(f"  ├── {line}")
    return 0


def cmd_pack(args) -> int:
    zips = pack_skills(Path(args.skills_dir))
    if not zips:
        print(f"✗ {args.skills_dir} 下未发现含 SKILL.md 的技能目录")
        return 1
    for z in zips:
        print(f"✓ {z}")
    print("技能包已更新（UTF-8 文件名，跨平台解压不乱码）")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chaishu",
        description="网文拆书工具箱：报告骨架生成 / MD→HTML 精排版 / 知识库入库 / 技能打包",
    )
    parser.add_argument("--version", action="version", version=f"chaishu {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="生成拆书报告骨架")
    p_new.add_argument("book", help="书名")
    p_new.add_argument("--mode", choices=["deep", "rough"], default="deep",
                       help="deep=深度细拆（默认） rough=粗拆")
    p_new.add_argument("--out-dir", default="拆书", help="输出目录（默认 ./拆书）")
    p_new.add_argument("--force", action="store_true", help="覆盖已有文件")
    p_new.set_defaults(func=cmd_new)

    p_build = sub.add_parser("build", help="拆书报告 Markdown → 精排版 HTML")
    p_build.add_argument("report", help="报告 .md 路径")
    p_build.add_argument("-o", "--out", help="输出 .html 路径（默认同名）")
    p_build.add_argument("--template", help="自定义 HTML 模板路径")
    p_build.set_defaults(func=cmd_build)

    p_val = sub.add_parser("validate", help="校验报告完整性")
    p_val.add_argument("report", help="报告 .md 路径")
    p_val.set_defaults(func=cmd_validate)

    p_kb = sub.add_parser("kb", help="知识库入库/统计")
    kb_sub = p_kb.add_subparsers(dest="kb_cmd", required=True)
    p_add = kb_sub.add_parser("add", help="把报告五大维度精华追加到知识库")
    p_add.add_argument("report", help="报告 .md 路径")
    p_add.add_argument("--kb-dir", default=".", help="知识库目录（默认当前目录）")
    p_add.add_argument("--force", action="store_true", help="已入库也追加")
    p_add.set_defaults(func=cmd_kb)
    p_stats = kb_sub.add_parser("stats", help="知识库条目统计")
    p_stats.add_argument("--kb-dir", default=".", help="知识库目录（默认当前目录）")
    p_stats.set_defaults(func=cmd_kb)

    p_pack = sub.add_parser("pack", help="打包 skills/ 下技能为 zip")
    p_pack.add_argument("--skills-dir", default="skills", help="技能目录（默认 ./skills）")
    p_pack.set_defaults(func=cmd_pack)

    return parser


def main(argv=None) -> int:
    _stdout_utf8()
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
