"""Contrat Doctrine V4.1 embarqué côté SDK pour 30_ui_designer_frontend_sdk_mcp (INV-18 / INV-19)."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


def _lp(p: Path) -> str:
    s = str(p.resolve())
    return "\\\\?\\" + s if os.name == "nt" and not s.startswith("\\\\?\\") else s


def _find_tool_root() -> Path:
    here = Path(__file__).resolve()
    for cand in [here.parent, here.parents[1], here.parents[2]]:
        if os.path.isfile(_lp(cand / "runtime_requirements.json")) or os.path.isdir(_lp(cand / "docs")):
            return cand
    return here.parent


def get_doctrine() -> Dict[str, Any]:
    """Retourne la doctrine autonome embarquée avec cet outil/SDK (zéro dépendance externe)."""
    root = _find_tool_root()
    doc_path = root / "docs" / "DOCTRINE_PIPELINES_SEQUENTIELLES.md"
    if not os.path.isfile(_lp(doc_path)):
        return {"status": "MISSING", "tool": "30_ui_designer_frontend_sdk_mcp", "tier": "PALIER_3_USINE_SKILLS", "content": ""}
    with open(_lp(doc_path), "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return {
        "status": "SUCCESS",
        "tool": "30_ui_designer_frontend_sdk_mcp",
        "tier": "PALIER_3_USINE_SKILLS",
        "doctrine_version": "4.1",
        "path": str(doc_path).replace("\\", "/"),
        "content": text,
    }


def get_runtime_requirements() -> Dict[str, Any]:
    """Retourne les exigences Python minimales embarquées (INV-19)."""
    root = _find_tool_root()
    req_path = root / "runtime_requirements.json"
    if not os.path.isfile(_lp(req_path)):
        return {"tool_name": "30_ui_designer_frontend_sdk_mcp", "min_python": "3.10", "docker_base_image": "python:3.12-slim"}
    with open(_lp(req_path), "r", encoding="utf-8") as f:
        return json.load(f)


def get_sdk_contract() -> Dict[str, Any]:
    """Expose le contrat combiné INV-18 + INV-19 pour les clients Python/SDK."""
    doc = get_doctrine()
    req = get_runtime_requirements()
    return {"tool": "30_ui_designer_frontend_sdk_mcp", "tier": "PALIER_3_USINE_SKILLS", "doctrine_status": doc["status"], "runtime": req}
