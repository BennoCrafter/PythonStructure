import importlib.util
import sys
from types import ModuleType
from pathlib import Path

def import_from_path(module_name: str, file_path: Path) -> ModuleType:
    """Import a module given its name and file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    if spec is None or spec.loader is None:
        raise ValueError(f"Could not create module spec or loader for {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module
