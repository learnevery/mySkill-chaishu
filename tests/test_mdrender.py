"""mdrender：Markdown 子集解析与渲染。"""
from chaishu.mdrender import parse_blocks, render_inline, render_inner


def test_heading_and_para():
    blocks = parse_blocks("## 二、标题（维度一）\n\n段落一\n\n段落二")
    assert blocks[0].type == "heading" and blocks[0].level == 2
    assert blocks[0].text == "二、标题（维度一）"
    assert [b.text for b in blocks[1:]] == ["段落一", "段落二"]


def test_inline():
    assert render_inline("**粗体**") == "<strong>粗体</strong>"
    assert render_inline("*斜*") == "<em>斜</em>"
    assert render_inline("`代码`") == "<code>代码</code>"
    assert "<script>" not in render_inline("<script>")


def test_table():
    blocks = parse_blocks("| 章节 | 钩子 |\n|---|---|\n| 1 | 危机钩 |\n| 2 |  |")
    assert blocks[0].type == "table"
    html = render_inner(blocks)
    assert '<div class="tbl-wrap">' in html
    assert "<th>章节</th>" in html
    assert html.count("<td>") == 4
    assert "—" in html  # 空单元格补 —


def test_callout_heuristic():
    blocks = parse_blocks("**作者为什么这么安排**：开篇三件事一次完成。")
    html = render_inner(blocks)
    assert '<div class="callout">' in html


def test_lists_nested_and_check():
    md = "- 甲\n- 乙\n  - 乙1\n1. 第一\n2. 第二"
    html = render_inner(parse_blocks(md))
    assert "<ul>" in html and "<ol>" in html and "<li>" in html

    html2 = render_inner(parse_blocks("- 甲\n- 乙"), check_lists=True)
    assert '<ul class="check">' in html2
    assert '<span class="num">1.</span>' in html2


def test_quote_and_code():
    md = "> 拆解对象：某人《书》\n> 拆解范围：第1章\n\n```\n公式A → 公式B\n```"
    html = render_inner(parse_blocks(md))
    assert '<div class="lead">' in html
    assert '<div class="formula">' in html


def test_hr_skipped():
    html = render_inner(parse_blocks("---"))
    assert html == ""
