"""Utilitaires de chemins sécurisés anti-MAX_PATH Windows pour MCP #30."""
from __future__ import annotations

import os
from pathlib import Path


def safe_path(path: Path) -> Path:
    """Retourne un Path étendu \\\\?\\ sous Windows pour contourner MAX_PATH (260 chars)."""
    resolved = str(path.resolve())
    if os.name == "nt" and not resolved.startswith("\\\\?\\"):
        return Path("\\\\?\\" + resolved)
    return path
