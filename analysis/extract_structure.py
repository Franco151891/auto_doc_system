from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from tree_sitter import Node
from analysis.model import ClassModel, FileModel, FunctionModel, MethodModel
from analysis.ts_parser import build_python_parser
from analysis.extract_imports import extract_imports


def analyze_file(project_root: Path, relative_path: Path) -> FileModel:
    abs_path = (project_root / relative_path).resolve()
    source_bytes = abs_path.read_bytes()

    parser = build_python_parser()
    tree = parser.parse(source_bytes)
    root = tree.root_node
    imports = extract_imports(root, source_bytes)


    classes: List[ClassModel] = []
    functions: List[FunctionModel] = []

    for child in root.children:
        if child.type == "class_definition":
            classes.append(_extract_class(child, source_bytes))
        elif child.type == "function_definition":
            functions.append(_extract_function(child, source_bytes))

    return FileModel(
        relative_path=relative_path,
        imports=imports,
        classes=classes,
        functions=functions,
    )


def _extract_class(class_node: Node, src: bytes) -> ClassModel:
    name = _node_text(_child_by_field(class_node, "name"), src) or "UNKNOWN_CLASS"
    bases = _extract_bases(class_node, src)

    methods: List[MethodModel] = []
    body = _child_by_field(class_node, "body")
    if body:
        for item in body.children:
            if item.type == "function_definition":
                methods.append(_extract_method(item, src))

    return ClassModel(name=name, bases=bases, methods=methods)


def _extract_function(fn_node: Node, src: bytes) -> FunctionModel:
    name = _node_text(_child_by_field(fn_node, "name"), src) or "UNKNOWN_FUNCTION"
    params = _extract_parameters(fn_node, src)
    ret = _extract_return_annotation(fn_node, src)
    return FunctionModel(name=name, parameters=params, return_annotation=ret)


def _extract_method(fn_node: Node, src: bytes) -> MethodModel:
    name = _node_text(_child_by_field(fn_node, "name"), src) or "UNKNOWN_METHOD"
    params = _extract_parameters(fn_node, src)
    ret = _extract_return_annotation(fn_node, src)
    return MethodModel(name=name, parameters=params, return_annotation=ret)


def _extract_parameters(fn_node: Node, src: bytes) -> List[str]:
    params_node = _child_by_field(fn_node, "parameters")
    if not params_node:
        return []
    out: List[str] = []
    for ch in params_node.children:
        if ch.type in {"(", ")", ",", "comment"}:
            continue
        text = _node_text(ch, src)
        if text:
            out.append(text)
    return out


def _extract_return_annotation(fn_node: Node, src: bytes) -> Optional[str]:
    ret_node = _child_by_field(fn_node, "return_type")
    return _node_text(ret_node, src) if ret_node else None


def _extract_bases(class_node: Node, src: bytes) -> List[str]:
    super_node = _child_by_field(class_node, "superclasses")
    if not super_node:
        return []
    bases: List[str] = []
    for ch in super_node.children:
        if ch.type in {"(", ")", ",", "comment"}:
            continue
        text = _node_text(ch, src)
        if text:
            bases.append(text)
    return bases


def _child_by_field(node: Node, field_name: str) -> Optional[Node]:
    return node.child_by_field_name(field_name)


def _node_text(node: Optional[Node], src: bytes) -> Optional[str]:
    if node is None:
        return None
    return src[node.start_byte : node.end_byte].decode("utf-8", errors="replace").strip()
