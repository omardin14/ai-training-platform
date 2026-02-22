"""LangChain Agents course - module registry."""

from learn.content.langchain_agents.module_01 import MODULE as MODULE_01
from learn.content.langchain_agents.module_02 import MODULE as MODULE_02
from learn.content.langchain_agents.module_03 import MODULE as MODULE_03
from learn.content.langchain_agents.module_04 import MODULE as MODULE_04
from learn.content.langchain_agents.module_05 import MODULE as MODULE_05

_COURSE_DIR = "courses/langchain-agents"

# All modules in order, with directory paths prefixed for the new layout.
AGENTS_MODULES = [
    MODULE_01,
    MODULE_02,
    MODULE_03,
    MODULE_04,
    MODULE_05,
]

# Prefix each module's directory with the course path.
for _m in AGENTS_MODULES:
    _orig = _m["directory"]
    if not _orig.startswith(_COURSE_DIR):
        _m["directory"] = f"{_COURSE_DIR}/{_orig}"
    if "setup" in _m and "module_dir" in _m["setup"]:
        _setup_dir = _m["setup"]["module_dir"]
        if not _setup_dir.startswith(_COURSE_DIR):
            _m["setup"]["module_dir"] = f"{_COURSE_DIR}/{_setup_dir}"
