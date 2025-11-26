# src/importer/engine.py

import importlib
import pkgutil
from pathlib import Path
from src.importer import adapters


class ImportEngine:
    """
    Loads all adapters inside src/importer/adapters
    Each adapter must implement:
       - can_handle(path: str) -> bool
       - parse(path: str) -> list[dict]
    """

    def __init__(self):
        self._adapters = []
        self._load_adapters()

    def _load_adapters(self):
        package = adapters
        package_path = package.__path__

        for _, module_name, _ in pkgutil.iter_modules(package_path):
            module_full = f"{package.__name__}.{module_name}"
            module = importlib.import_module(module_full)

            if hasattr(module, "Adapter"):
                self._adapters.append(module.Adapter())

    def import_file(self, file_path: str):
        file_path = str(Path(file_path).expanduser().resolve())

        for adapter in self._adapters:
            try:
                if adapter.can_handle(file_path):
                    return adapter.parse(file_path)
            except Exception as e:
                print(f"[WARN] Adapter {adapter} threw error: {e}")

        raise ValueError(f"No adapter can handle file: {file_path}")
