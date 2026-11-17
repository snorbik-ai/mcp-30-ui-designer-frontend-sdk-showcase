"""Porte 2 : CLI Terminal pour ui_designer_frontend_sdk_mcp."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from canal_sdk_cli.sdk import UiDesignerFrontendSdkMcpSdk


def main():
    parser = argparse.ArgumentParser(description="MCP UI Designer & Frontend SDK Builder : Banque de composants React (shadcn, Magic UI, 21st.dev), Chat Panels IA (OpenAI ChatKit, assistant-ui), protocoles ACP & Google ADK, et matérialisation architecture Puzzle N1-N5 (<350L).")
    parser.add_argument("--action", default="ping", help="Action à exécuter (ping, pipelines, execute)")
    parser.add_argument("--params", default="{}", help="Paramètres JSON de l'action")
    args = parser.parse_args()

    sdk = UiDesignerFrontendSdkMcpSdk()
    if args.action == "ping":
        print(json.dumps(sdk.ping(), indent=2, ensure_ascii=False))
    elif args.action == "pipelines":
        print(json.dumps(sdk.get_recommended_pipelines(), indent=2, ensure_ascii=False))
    else:
        try:
            params = json.loads(args.params)
        except Exception:
            params = {"raw": args.params}
        res = sdk.execute(args.action, params)
        print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
