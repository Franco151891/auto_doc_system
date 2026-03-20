from __future__ import annotations
from pathlib import Path


def write_markdown_file(project_root: Path, relative_source_path: Path, markdown_text: str) -> Path:

    docs_root = project_root / "docs"

    out_rel = Path(str(relative_source_path) + ".md")
    out_path = docs_root / out_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown_text, encoding="utf-8")
    return out_path
