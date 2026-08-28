"""技能打包（chaishu pack）。

把 skills/ 下每个含 SKILL.md 的目录打成同名 zip：
- 文件名 UTF-8 编码（跨平台解压不乱码）；
- 固定时间戳、按路径排序，产出确定性可复现的 zip。
"""
from __future__ import annotations

from pathlib import Path
from typing import List
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

_FIXED_DATE = (2026, 1, 1, 0, 0, 0)


def pack_skills(skills_dir: Path = Path("skills")) -> List[Path]:
    """打包所有技能目录，返回生成的 zip 路径列表。"""
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"技能目录不存在：{skills_dir}")

    zips: List[Path] = []
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        if not (skill_dir / "SKILL.md").exists():
            continue
        zip_path = skills_dir / f"{skill_dir.name}.zip"
        _zip_dir(skill_dir, zip_path)
        zips.append(zip_path)
    return zips


def _zip_dir(src_dir: Path, zip_path: Path) -> None:
    files = sorted(p for p in src_dir.rglob("*") if p.is_file())
    with ZipFile(zip_path, "w") as zf:
        for f in files:
            arcname = f.relative_to(src_dir).as_posix()
            info = ZipInfo(arcname, date_time=_FIXED_DATE)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, f.read_bytes())
