from __future__ import annotations

FILE_TEMPLATE = """# {file_path}

## Overview
{overview}

## Imports
{imports}

## Classes
{classes}

## Functions
{functions}
"""

CLASS_TEMPLATE = """### Class `{class_name}`

{class_description}

#### Methods
{methods}
"""

METHOD_TEMPLATE = """- **{method_name}({signature})**
  {description}
"""

FUNCTION_TEMPLATE = """### Function `{function_name}({signature})`

{description}
"""
