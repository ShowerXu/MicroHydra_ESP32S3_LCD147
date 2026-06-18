"""Helpers for running built-in launcher handlers without rebooting."""

import gc
import sys


class ExitToLauncher(Exception):
    """Raised by a built-in handler when it wants to return to launcher."""


def module_name(path):
    """Convert a MicroHydra app path to a Python module name."""
    path = path.strip()
    if path.startswith("/"):
        path = path[1:]
    if path.endswith(".py") or path.endswith(".mpy"):
        path = path.rsplit(".", 1)[0]
    return path.replace("/", ".")


def import_fresh(path):
    """Import a module path, removing any cached copy first."""
    name = module_name(path)
    for mod_name in tuple(sys.modules):
        if mod_name == name or mod_name.startswith(name + "."):
            del sys.modules[mod_name]
    module = __import__(name)
    for part in name.split(".")[1:]:
        module = getattr(module, part)
    return module


def run_handler(path, *args):
    """Run a built-in handler module's run() function."""
    gc.collect()
    module = import_fresh(path)
    try:
        if hasattr(module, "run"):
            return module.run(*args)
    except ExitToLauncher:
        return None
    finally:
        gc.collect()
    return None


def exit_to_launcher():
    """Return to the launcher from a nested built-in handler."""
    raise ExitToLauncher()
