"""Module content registry."""

import os

from learn.content.module_01 import MODULE as MODULE_01
from learn.content.module_02 import MODULE as MODULE_02
from learn.content.module_03 import MODULE as MODULE_03
from learn.content.module_04 import MODULE as MODULE_04
from learn.content.module_05 import MODULE as MODULE_05
from learn.content.module_06 import MODULE as MODULE_06
from learn.content.module_07 import MODULE as MODULE_07
from learn.content.module_08 import MODULE as MODULE_08
from learn.content.module_09 import MODULE as MODULE_09
from learn.content.module_10 import MODULE as MODULE_10
from learn.content.module_11 import MODULE as MODULE_11
from learn.content.module_12 import MODULE as MODULE_12
from learn.content.module_13 import MODULE as MODULE_13
from learn.content.module_14 import MODULE as MODULE_14
from learn.content.module_15 import MODULE as MODULE_15
from learn.parser import parse_readme

# All available modules in order.
MODULES = [
    MODULE_01,
    MODULE_02,
    MODULE_03,
    MODULE_04,
    MODULE_05,
    MODULE_06,
    MODULE_07,
    MODULE_08,
    MODULE_09,
    MODULE_10,
    MODULE_11,
    MODULE_12,
    MODULE_13,
    MODULE_14,
    MODULE_15,
]

# Resolve the project root (parent of learn/ package)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_pages(module):
    """Load lesson pages from the module's README.md using markers.

    Returns a list of {"title": str, "content": str} dicts.
    Returns empty list if README has no lesson markers.
    """
    readme_path = os.path.join(_PROJECT_ROOT, module["directory"], "README.md")
    return parse_readme(readme_path)


def get_module(module_id):
    """Get a module by ID. Returns None if not found."""
    for m in MODULES:
        if m["id"] == module_id:
            return m
    return None
