from __future__ import annotations

import importlib.metadata
from pathlib import Path

project = "uv-init"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_autodoc_typehints",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"

# Add project root to sys.path so autodoc can find uv_init
import sys
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# Version info
try:
    release = importlib.metadata.version("uv-init")
except importlib.metadata.PackageNotFoundError:
    release = "0.0.0"
version = release

html_theme = "alabaster"
