from __future__ import annotations

from pathlib import Path
from typing import List


def build_global_readme(py_files: List[Path]) -> str:
    """
    Deterministic global index. Always regenerated.
    """
    lines: list[str] = []
    lines.append("# Project Documentation Index")
    lines.append("")
    lines.append("This documentation was generated automatically.")
    lines.append("")
    lines.append("## Files")
    lines.append("")

    for rel_path in sorted(py_files, key=lambda p: p.as_posix()):
        md_path = Path("docs") / Path(str(rel_path) + ".md")
        lines.append(f"- `{rel_path.as_posix()}` → `{md_path.as_posix()}`")

    lines.append("")
    return "\n".join(lines)


def write_global_readme(project_root: Path, content: str) -> None:
    (project_root / "docs").mkdir(parents=True, exist_ok=True)
    (project_root / "docs" / "README.md").write_text(content, encoding="utf-8")
