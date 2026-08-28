"""render：报告 MD → 精排版 HTML 组装。"""
from pathlib import Path

from chaishu.render import extract_meta, render_report_html, zh_num

FIXTURE = Path(__file__).parent / "fixtures" / "sample-deep.md"
MD = FIXTURE.read_text(encoding="utf-8")


def test_zh_num():
    assert zh_num(1) == "一" and zh_num(9) == "九"
    assert zh_num(10) == "十" and zh_num(12) == "十二" and zh_num(20) == "二十"


def test_extract_meta():
    meta = extract_meta(MD)
    assert meta["book"] == "示例之书"
    assert meta["mode"] == "深度细拆"
    assert meta["author"] == "佚名"
    assert meta["words"] == "5.2万字"
    assert meta["chapters"] == "20章"
    assert meta["reading"] == "在读12万"
    assert meta["rating"] == "8.5"
    assert meta["category"] == "都市高武"
    assert "第1章—第20章" in meta["scope"]


def test_render_full_report():
    html, meta = render_report_html(MD)
    # 结构：9 个 section、导航锚点一一对应
    assert html.count('<section id="s') == 9
    assert '<a href="#s9">' in html and '<a href="#s1">' in html
    # 模板样式与折叠脚本保留
    assert "<style>" in html and "navToggle" in html
    # 占位符全部被替换
    assert "【书名】" not in html and "【作者】" not in html
    # 封面与页脚
    assert "示例之书" in html and "拆书红线自查" in html
    assert "<title>深度细拆报告：示例之书</title>" in html
    # 内化清单用 check 样式
    assert '<ul class="check">' in html


def test_render_rough_report_has_placeholder_meta():
    rough = "# 粗拆报告：测试书\n\n## 书籍信息\n\n- 内容\n"
    html, meta = render_report_html(rough)
    assert meta["mode"] == "粗拆"
    assert "—" in html  # 缺失字段兜底
