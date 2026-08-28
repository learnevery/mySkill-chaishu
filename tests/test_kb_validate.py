"""kb：知识库规则入库 / validate：报告校验。"""
from pathlib import Path

from chaishu.kb import extract_kb_entries, kb_add, kb_stats, split_units
from chaishu.validate import validate_report

FIXTURE = Path(__file__).parent / "fixtures" / "sample-deep.md"
MD = FIXTURE.read_text(encoding="utf-8")


def test_split_units():
    units = split_units(MD)
    titles = [t for t, _ in units]
    assert any("主角" in t for t in titles)
    assert any("金手指" in t for t in titles)


def test_extract_entries_cover_five_kb():
    entries = extract_kb_entries(MD, "拆书报告-示例之书-深度细拆.md")
    assert set(entries) >= {"人设", "金手指", "节奏", "剧情", "范式"}
    assert "来源：拆书报告-示例之书-深度细拆.md" in entries["人设"]
    assert "《示例之书》" in entries["人设"]


def test_kb_add_and_dedup(tmp_path):
    report = kb_add(MD, FIXTURE, tmp_path)
    assert any("人设.md" in r for r in report)
    for name in ("人设", "金手指", "节奏", "剧情"):
        assert (tmp_path / f"{name}.md").exists()

    # 重复入库默认跳过
    report2 = kb_add(MD, FIXTURE, tmp_path)
    assert all("跳过" in r for r in report2)

    # --force 追加
    report3 = kb_add(MD, FIXTURE, tmp_path, force=True)
    assert any("追加" in r for r in report3)

    stats = kb_stats(tmp_path)
    assert any("人设.md：2 条" in s for s in stats)


def test_validate_ok():
    passed, results = validate_report(MD)
    fails = [msg for level, msg in results if level == "FAIL"]
    assert passed, fails


def test_validate_missing_sections():
    bad = "# 深度细拆报告：缺章\n\n## 一、书籍信息\n\n- x\n"
    passed, results = validate_report(bad)
    assert not passed
    assert any("缺少章节" in msg for _, msg in results)


def test_validate_missing_purpose_column():
    bad = """# 深度细拆报告：缺列

## 一、书籍信息与选书理由
- x

## 二、核心卖点与开篇拆解
- x

## 三、人设体系拆解
- x

## 四、节奏与情绪曲线拆解
| 章 | 冲突 |
|---|---|
| 1 | x |

## 五、大纲与故事结构拆解
- x

## 六、赛道读者偏好分析
- x

## 七、可复用范式清单
- x

## 八、仿写训练
- 这里是一段足够长的仿写内容，用来通过长度检查，虽然本章没有作者目的列表格，但其他必填章节都在，校验应因缺少该表格而失败，此处补足三百字以上的仿写文本以满足长度要求，重复一遍：此处补足三百字以上的仿写文本以满足长度要求，再来一遍此处补足三百字以上的仿写文本以满足长度要求。

## 九、内化行动清单
1. 每章末留钩子。
2. 金手指带代价。
3. 开篇三件事。
"""
    passed, results = validate_report(bad)
    assert not passed
    assert any("作者目的" in msg for level, msg in results if level == "FAIL")
