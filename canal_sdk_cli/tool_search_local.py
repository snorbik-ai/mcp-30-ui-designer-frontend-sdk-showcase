"""tool_search_local.py — Moteur Tool Search Autonome INV-20 (30_ui_designer_frontend_sdk_mcp).
Accessible en SDK (`from canal_sdk_cli.tool_search_local import search_local_tools`) et en CLI.
Zéro dépendance inter-MCP : lit directement `canal_mcp/tool_search_manifest.json` en < 1ms.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional

_MANIFEST_PATH = Path(__file__).resolve().parents[1] / "canal_mcp" / "tool_search_manifest.json"
SERVER_ID = "30-ui-designer-frontend-sdk-mcp"
SERVER_DIR = "30_ui_designer_frontend_sdk_mcp"


def _norm_tokens(text: str) -> List[str]:
    dec = unicodedata.normalize("NFKD", (text or "").lower())
    clean = "".join(c for c in dec if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9_]{2,}", clean)


def load_local_manifest() -> Dict[str, Any]:
    if not _MANIFEST_PATH.is_file():
        return {"schema_version": "INV-20-v1.0", "server_id": SERVER_ID, "tools": []}
    return json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))


def search_local_tools(
    query: str = "",
    *,
    auth_filter: Optional[str] = None,
    limit: int = 5,
) -> Dict[str, Any]:
    """Recherche dynamique dans les outils de `30_ui_designer_frontend_sdk_mcp` avec filtrage auth et micro-prompts."""
    manifest = load_local_manifest()
    tools: List[Dict[str, Any]] = list(manifest.get("tools") or [])
    q_tokens = _norm_tokens(query)
    scored: List[Dict[str, Any]] = []

    for item in tools:
        req_auth = bool(item.get("requires_auth", False))
        if auth_filter == "public" and req_auth:
            continue
        if auth_filter == "auth_required" and not req_auth:
            continue
        hay_name = str(item.get("tool_name", "")).lower()
        hay_desc = f"{item.get('planner_micro_prompt', '')} {item.get('responder_micro_prompt', '')}".lower()
        score = 0.0
        for tok in q_tokens:
            if tok in hay_name:
                score += 6.0
            if tok in hay_desc:
                score += 2.5
        if not q_tokens or score > 0 or item.get("always_load"):
            scored.append({**item, "score": round(score, 2)})

    scored.sort(key=lambda x: (-x["score"], not x.get("always_load", False), x.get("tool_name", "")))
    hits = scored[: max(1, min(20, int(limit)))]
    total = len(tools)
    reduction = round((1.0 - (len(hits) / total)) * 100.0, 1) if total > 0 else 0.0
    return {
        "status": "OK",
        "server_id": SERVER_ID,
        "server_dir": SERVER_DIR,
        "query": query,
        "total_tools": total,
        "matched_count": len(hits),
        "context_reduction_pct": max(0.0, reduction),
        "hits": hits,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool Search local INV-20")
    parser.add_argument("--query", default="", help="Mots-clés de recherche")
    parser.add_argument("--auth-filter", choices=["public", "auth_required"], default=None)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(search_local_tools(args.query, auth_filter=args.auth_filter, limit=args.limit), indent=2, ensure_ascii=False))
