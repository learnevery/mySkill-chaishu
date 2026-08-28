"""CLI 端到端：new → build → kb add → stats → validate → pack。"""
import shutil
import zipfile
from pathlib import Path


from chaishu.cli import main


def run(capsys, *argv):
    code = main(list(argv))
    out = capsys.readouterr().out
    return code, out


def test_new_build_roundtrip(tmp_path, capsys):
    code, out = run(capsys, "new", "测试书", "--mode", "deep", "--out-dir", str(tmp_path))
    assert code == 0
    md = tmp_path / "拆书报告-测试书-深度细拆.md"
    assert md.exists() and "{书名}" not in md.read_text(encoding="utf-8")

    code, out = run(capsys, "build", str(md))
    assert code == 0
    html = md.with_suffix(".html")
    text = html.read_text(encoding="utf-8")
    assert "<style>" in text and "navToggle" in text
    assert "测试书" in text

    # 骨架未填写时校验应失败并提示缺什么
    code, out = run(capsys, "validate", str(md))
    assert code == 1
    assert "FAIL" in out or "✗" in out


def test_kb_commands(tmp_path, capsys):
    src = Path(__file__).parent / "fixtures" / "sample-deep.md"
    code, out = run(capsys, "kb", "add", str(src), "--kb-dir", str(tmp_path))
    assert code == 0
    assert (tmp_path / "人设.md").exists()

    code, out = run(capsys, "kb", "stats", "--kb-dir", str(tmp_path))
    assert code == 0
    assert "人设.md：1 条" in out


def test_new_refuses_overwrite(tmp_path, capsys):
    run(capsys, "new", "重复书", "--out-dir", str(tmp_path))
    code, out = run(capsys, "new", "重复书", "--out-dir", str(tmp_path))
    assert code == 1
    code, out = run(capsys, "new", "重复书", "--out-dir", str(tmp_path), "--force")
    assert code == 0


def test_pack(tmp_path):
    skills = tmp_path / "skills"
    src = Path(__file__).parent.parent / "skills" / "chaishu"
    shutil.copytree(src, skills / "demo-skill")
    code = main(["pack", "--skills-dir", str(skills)])
    assert code == 0
    z = skills / "demo-skill.zip"
    assert z.exists()
    with zipfile.ZipFile(z) as zf:
        names = zf.namelist()
        assert "SKILL.md" in names
        assert any("五大维度拆解手册" in n for n in names)  # UTF-8 文件名
        info = zf.getinfo("references/五大维度拆解手册.md")
        assert info.flag_bits & 0x800  # UTF-8 标志位
