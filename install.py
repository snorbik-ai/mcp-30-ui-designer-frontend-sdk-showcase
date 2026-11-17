#!/usr/bin/env python3
"""Installateur multi-clients -- 30_ui_designer_frontend_sdk_mcp."""
import json, os, platform, sys
from pathlib import Path
from snorbik_bootstrap import get_guaranteed_python
PYTHON_BIN = get_guaranteed_python()
COMPONENT_NAME = "30_ui_designer_frontend_sdk_mcp"
ENTRYPOINT_REL = "canal_mcp/mcp_server.py"

def main():
    root = Path(__file__).resolve().parent
    entry = {
        "command": str(PYTHON_BIN),
        "args": [(root / ENTRYPOINT_REL).resolve().as_posix()],
        "cwd": root.as_posix(),
        "env": {"PYTHONIOENCODING": "utf-8"},
        "type": "stdio"
    }
    c_path = Path.home() / ".cursor" / "mcp.json"
    if c_path.exists():
        data = json.loads(c_path.read_text(encoding="utf-8"))
        data.setdefault("mcpServers", {})[COMPONENT_NAME] = entry
        c_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✅ {COMPONENT_NAME} installé avec succès")

if __name__ == "__main__":
    main()
