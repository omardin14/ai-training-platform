"""Auto-discovery loader for course modules."""

import importlib
import os


def discover_modules(package_name, course_dir):
    """Scan for module_*.py files in a package, import each, and return sorted list.

    This replaces the manual import + list pattern in each course's __init__.py.
    Adding a new module is now just creating the file — no registration needed.
    """
    package = importlib.import_module(package_name)
    package_dir = os.path.dirname(package.__file__)

    modules = []
    for filename in sorted(os.listdir(package_dir)):
        if not filename.startswith("module_") or not filename.endswith(".py"):
            continue
        module_name = filename[:-3]  # strip .py
        full_name = f"{package_name}.{module_name}"
        mod = importlib.import_module(full_name)
        module_dict = mod.MODULE

        # Prefix directory with course path
        if not module_dict["directory"].startswith(course_dir):
            module_dict["directory"] = f"{course_dir}/{module_dict['directory']}"

        # Also prefix setup.module_dir if present
        setup = module_dict.get("setup")
        if setup and "module_dir" in setup:
            if not setup["module_dir"].startswith(course_dir):
                setup["module_dir"] = f"{course_dir}/{setup['module_dir']}"

        modules.append(module_dict)

    modules.sort(key=lambda m: m["id"])
    return modules
