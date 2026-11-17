"""Serveur MCP JSON-RPC 2.0 / stdio V3.0 -- 30_ui_designer_frontend_sdk_mcp.
Porte 1 : Connexion universelle IDE IA (Antigravity, Cursor, Claude Desktop, Google ADK).
Usine Snorbik MCP Factory Launcher (Standard INV-07 Bipartite).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from canal_sdk_cli.sdk import UiDesignerFrontendSdkMcpSdk
from canal_mcp.tools_metadata import TOOLS_METADATA

sdk = UiDesignerFrontendSdkMcpSdk()

_DIRECT_ACTIONS = {
    "ui_designer_init_session",
    "ui_designer_qualify_and_plan_pages",
    "ui_designer_extract_design_system",
    "ui_designer_analyze_mockup",
    "ui_designer_load_architecture_skills",
    "ui_designer_decompose_n1_to_n5",
    "ui_designer_hunt_parts_3_circles",
    "ui_designer_generate_phase1_design_prompt",
    "ui_designer_generate_phase2_video_prompt",
    "ui_designer_list_bank_inventory",
    "ui_designer_search_bank",
    "ui_designer_generate_materialization_doc",
    "ui_designer_materialize_frontend_sdk",
    "ui_designer_generate_backend_bridge",
    "ui_designer_audit_architecture",
}


def handle_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Any:
    if tool_name == "ui_designer_frontend_sdk_mcp_ping":
        return {"status": "HEALTHY", "tool": "ui_designer_frontend_sdk_mcp", "version": "3.0.0"}
    if tool_name == "ui_designer_frontend_sdk_mcp_get_pipelines":
        return sdk.get_recommended_pipelines()
    if tool_name == "ui_designer_frontend_sdk_mcp_run":
        return sdk.execute(arguments.get("action", "execute"), arguments.get("parameters", {})).model_dump()
    if tool_name in _DIRECT_ACTIONS:
        return sdk.execute(tool_name, arguments).model_dump()
    raise ValueError(f"Outil MCP inconnu: {tool_name}")


def run_stdio_server() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            if req_id is None:
                continue
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "30_ui_designer_frontend_sdk_mcp", "version": "3.0.0"},
                        "instructions": "Standard Tri-Canal Snorbik AI V3.0 — Usine de Montage UI (Qualification, Stitch, Chasse 3 Cercles, ACP, Google ADK, ChatKit).",
                    },
                }
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS_METADATA}}
            elif method == "tools/call":
                params = req.get("params", {})
                res = handle_tool_call(params.get("name", ""), params.get("arguments", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False)}]},
                }
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(resp, ensure_ascii=False), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
            print(json.dumps(err, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    run_stdio_server()
