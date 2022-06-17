from typing import Dict

from tree_sitter import Language

"""
Supported languages for parsing
"""
LANGUAGES: Dict[str, Language] = {
    "python": Language("./build/languages.so", "python"),
    "java": Language("./build/languages.so", "java"),
    "javascript": Language("./build/languages.so", "javascript")
}

"""
Queries for tree-sitter to get classes', functions', variables' names
"""
QUERIES: Dict[str, Dict[str, str]] = {
    "python": {"classes": "(class_definition name: (identifier) @class.def)",
               "functions": "(function_definition name: (identifier) @function.def)",
               "variables": "(assignment left: (identifier) @var.def)"},
    "java": {"classes": "(class_declaration name: (identifier) @class.dec)",
             "functions": "(method_declaration name: (identifier) @method.dec)",
             "variables": "(variable_declarator name: (identifier) @variable.name)"},
    "javascript": {"classes": "(class_declaration name: (identifier) @class.dec)",
                   "functions": "(function_declaration name: (identifier) @function.dec)",
                   "variables": "(variable_declaration (variable_declarator (identifier) @var.dec))"}
}
