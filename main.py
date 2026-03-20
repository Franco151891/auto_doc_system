from __future__ import annotations
import argparse
import sys
from pathlib import Path
from analysis import analyze_file
from file_discovery import discover_python_files
from documentation.llm_adapter import LLMAdapter
from documentation.openai_client import OpenAIClient
from documentation.generate_texts import generate_file_doc_text
from documentation.index import build_global_readme, write_global_readme
from markdown.render import render_file_markdown
from update.write_docs import write_markdown_file
from update.state_store import DocState, load_state, save_state
from update.change_detection import detect_changes
from update.cleanup import delete_docs_for_removed


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auto_doc_system",
        description="Auto documentation system (incremental documentation generation).",
    )
    parser.add_argument(
        "--project-path",
        required=True,
        help="Path to the root of the Python repository to analyze.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    project_root = Path(args.project_path)

    try:
        py_files = discover_python_files(project_root)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    project_root = project_root.resolve()

    prev_state = load_state(project_root)
    changes, new_hashes = detect_changes(project_root, py_files, prev_state)

    if changes.removed:
        delete_docs_for_removed(project_root, changes.removed)
        for removed in changes.removed:
            print(f"Removed docs for: {removed.as_posix()}")

    llm = LLMAdapter(OpenAIClient(model="gpt-4.1-mini"))

    for rel_path in changes.changed:
        file_model = analyze_file(project_root, rel_path)

        doc_text = generate_file_doc_text(file_model, llm)
        md = render_file_markdown(file_model, doc_text)

        out_path = write_markdown_file(project_root, rel_path, md)
        print(f"Wrote: {out_path.relative_to(project_root).as_posix()}")

    readme = build_global_readme(py_files)
    write_global_readme(project_root, readme)
    print("Wrote: docs/README.md")

    save_state(project_root, DocState(file_hashes=new_hashes))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
