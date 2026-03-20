from __future__ import annotations

from pathlib import Path


def delete_docs_for_removed(project_root: Path, removed_rel_paths: list[Path]) -> None:
  
    docs_root = project_root / "docs"

    for rel_src in removed_rel_paths:
        md_rel = Path(str(rel_src) + ".md")
        out_path = docs_root / md_rel
        if out_path.exists():
            out_path.unlink()
