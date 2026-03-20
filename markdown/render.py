from __future__ import annotations

from analysis.model import FileModel
from documentation.doc_model import FileDocText
from markdown.templates import (
    CLASS_TEMPLATE,
    FILE_TEMPLATE,
    FUNCTION_TEMPLATE,
    METHOD_TEMPLATE,
)


def render_file_markdown(file_model: FileModel, doc_text: FileDocText) -> str:
    imports_md = _render_imports(file_model)
    classes_md = _render_classes(file_model, doc_text)
    functions_md = _render_functions(file_model, doc_text)

    return FILE_TEMPLATE.format(
        file_path=file_model.relative_path.as_posix(),
        overview=doc_text.overview.strip() or "<NO_OVERVIEW>",
        imports=imports_md,
        classes=classes_md,
        functions=functions_md,
    )


def _render_imports(file_model: FileModel) -> str:
    if not file_model.imports:
        return "(none)"
    return "\n".join(f"- `{imp}`" for imp in file_model.imports)


def _render_classes(file_model: FileModel, doc_text: FileDocText) -> str:
    if not file_model.classes:
        return "(none)"

    parts: list[str] = []
    for cls in file_model.classes:
        class_description = doc_text.class_descriptions.get(cls.name, "<NO_CLASS_DESCRIPTION>")

        methods_md = _render_methods(cls.name, cls.methods, doc_text)
        parts.append(
            CLASS_TEMPLATE.format(
                class_name=cls.name,
                class_description=class_description.strip() or "<NO_CLASS_DESCRIPTION>",
                methods=methods_md,
            )
        )
    return "\n\n".join(parts)


def _render_methods(class_name: str, methods, doc_text: FileDocText) -> str:
    if not methods:
        return "(none)"

    lines: list[str] = []
    for m in methods:
        sig = ", ".join(m.parameters)
        key = f"{class_name}.{m.name}"
        desc = doc_text.method_descriptions.get(key, "<NO_METHOD_DESCRIPTION>")
        lines.append(
            METHOD_TEMPLATE.format(
                method_name=m.name,
                signature=sig,
                description=desc.strip() or "<NO_METHOD_DESCRIPTION>",
            )
        )
    return "\n".join(lines)


def _render_functions(file_model: FileModel, doc_text: FileDocText) -> str:
    if not file_model.functions:
        return "(none)"

    parts: list[str] = []
    for fn in file_model.functions:
        sig = ", ".join(fn.parameters)
        desc = doc_text.function_descriptions.get(fn.name, "<NO_FUNCTION_DESCRIPTION>")
        parts.append(
            FUNCTION_TEMPLATE.format(
                function_name=fn.name,
                signature=sig,
                description=desc.strip() or "<NO_FUNCTION_DESCRIPTION>",
            )
        )
    return "\n\n".join(parts)
