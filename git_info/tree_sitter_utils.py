import platform
import urllib.request
from os.path import abspath, dirname, join
from typing import Dict

from tree_sitter import Language

URLS = {
    "Linux":
        "https://github.com/d-eremina/2022_similar_dev_search_eremina/releases/latest/download/languages-linux.so",
    "Darwin":
        "https://github.com/d-eremina/2022_similar_dev_search_eremina/releases/latest/download/languages-darwin.so"
}

FILENAMES = {
    "Linux": "languages-linux.so",
    "Darwin": "languages-darwin.so"
}


def _get_file_name() -> str | None:
    if platform.system() in FILENAMES:
        return FILENAMES[platform.system()]
    else:
        raise OSError(f"{platform.system()} is not supported in current version")


def _get_url() -> str | None:
    if platform.system() in URLS:
        return URLS[platform.system()]
    else:
        raise OSError(f"{platform.system()} is not supported in current version")


def download_languages() -> None:
    urllib.request.urlretrieve(
        _get_url(),
        abspath(join(abspath(join(dirname(__file__), "build")), _get_file_name())))


download_languages()

FILENAME = _get_file_name()

"""
Supported languages for parsing
"""
LANGUAGES: Dict[str, Language] = {
    "python": Language(f"./build/{FILENAME}", "python"),
    "java": Language(f"./build/{FILENAME}", "java"),
    "javascript": Language(f"./build/{FILENAME}", "javascript")
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
