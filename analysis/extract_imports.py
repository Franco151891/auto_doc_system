from __future__ import annotations
from typing import List, Optional
from tree_sitter import Node

def extract_imports(root: Node, src: bytes) -> List[str]:
    """
    Deterministically extracts import statements from a Python CST (Tree-Sitter).
    Returns a list of import lines as plain strings, in file order.
    """
    imports: List[str] = []

    for child in root.children:
        if child.type == "import_statement" or child.type == "import_from_statement":
            text = _node_text(child, src)
            if text:
                imports.append(_normalize_import_line(text))

    return imports


def _normalize_import_line(line: str) -> str:
    return " ".join(line.strip().split())


def _node_text(node: Optional[Node], src: bytes) -> Optional[str]:
    if node is None:
        return None
    return src[node.start_byte: node.end_byte].decode("utf-8", errors="replace").strip()
