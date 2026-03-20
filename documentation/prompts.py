from __future__ import annotations

BASE_PROMPT = (
    "You are generating technical documentation text for a Python project.\n"
    "You will receive structured information extracted from source code.\n"
    "STRICT OUTPUT RULES:\n"
    "- Output PLAIN TEXT ONLY.\n"
    "- Do NOT use Markdown (no headings, no bullet lists, no code fences).\n"
    "- Do NOT include function/class signatures as code blocks.\n"
    "- Do NOT repeat file paths or titles.\n"
    "- Do NOT document methods/functions unless explicitly asked for that single entity.\n"
    "- Keep it concise (2-5 sentences).\n"
    "- Do NOT invent APIs.\n"
)



def file_overview_prompt(file_path: str, imports: list[str]) -> str:
    return (
        BASE_PROMPT
        + f"\nTask: Write a high-level overview for the file '{file_path}'.\n"
        + f"Imports: {imports}\n"
    )


def class_prompt(class_name: str, bases: list[str]) -> str:
    return (
        BASE_PROMPT
        + f"\nTask: Describe the purpose and responsibility of the class '{class_name}'.\n"
        + f"Base classes: {bases}\n"
        + "Do NOT list or describe methods.\n"
    )



def method_prompt(method_name: str, signature: str) -> str:
    return (
        BASE_PROMPT
        + f"\nTask: Document the method '{method_name}'.\n"
        + f"Signature: {signature}\n"
        + "Write 1-3 sentences. No lists.\n"
    )


def function_prompt(function_name: str, signature: str) -> str:
    return (
        BASE_PROMPT
        + f"\nTask: Document the function '{function_name}'.\n"
        + f"Signature: {signature}\n"
        + "Write 1-3 sentences. No lists.\n"
    )
