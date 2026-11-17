"""Interfaces abstraites (ports Clean Architecture)."""
from __future__ import annotations

from typing import Protocol, Dict, Any


class IOperationalAdapter(Protocol):
    def execute_operation(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        ...
