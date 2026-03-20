from __future__ import annotations
from analysis.model import FileModel


def assemble_file_skeleton(file_model: FileModel) -> dict:
    """
    Returns a documentation skeleton with placeholders
    (to be filled by the LLM later).
    """
    return {
        "file_path": file_model.relative_path.as_posix(),
        "overview": "<OVERVIEW_PENDING>",
        "imports": file_model.imports,
        "classes": file_model.classes,
        "functions": file_model.functions,
    }
