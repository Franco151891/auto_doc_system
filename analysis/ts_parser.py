from __future__ import annotations
from tree_sitter import Language, Parser
import tree_sitter_python

def build_python_parser() -> Parser:
    parser = Parser()
    parser.language = Language(tree_sitter_python.language())
    return parser
