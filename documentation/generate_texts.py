from __future__ import annotations
from analysis.model import FileModel
from documentation.doc_model import FileDocText
from documentation.llm_adapter import LLMAdapter
from documentation.prompts import (
    class_prompt,
    file_overview_prompt,
    function_prompt,
    method_prompt,
)

def generate_file_doc_text(file_model: FileModel, llm: LLMAdapter) -> FileDocText:
    overview = llm.generate_text(
        file_overview_prompt(
            file_path=file_model.relative_path.as_posix(),
            imports=file_model.imports,
        )
    )

    class_desc: dict[str, str] = {}
    method_desc: dict[str, str] = {}
    func_desc: dict[str, str] = {}

    for cls in file_model.classes:
        class_desc[cls.name] = llm.generate_text(
            class_prompt(
                class_name=cls.name,
                bases=cls.bases,
            )
        )

        for m in cls.methods:
            sig = ", ".join(m.parameters)
            key = f"{cls.name}.{m.name}"
            method_desc[key] = llm.generate_text(
                method_prompt(method_name=m.name, signature=sig)
            )

    for fn in file_model.functions:
        sig = ", ".join(fn.parameters)
        func_desc[fn.name] = llm.generate_text(
            function_prompt(function_name=fn.name, signature=sig)
        )

    return FileDocText(
        overview=overview,
        class_descriptions=class_desc,
        method_descriptions=method_desc,
        function_descriptions=func_desc,
    )
