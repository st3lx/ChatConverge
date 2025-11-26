# src/importer/adapters/base_adapter.py

class BaseAdapter:
    """
    Adapter interface for importers.

    Implement:
      - can_handle(path: str) -> bool
      - parse(path: str) -> dict
    """

    def can_handle(self, path: str) -> bool:
        raise NotImplementedError

    def parse(self, path: str) -> dict:
        raise NotImplementedError
