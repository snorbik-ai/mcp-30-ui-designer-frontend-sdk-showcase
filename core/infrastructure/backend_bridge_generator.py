"""Générateur du Pont Backend FastAPI DDD (ACP, Google ADK, OpenAI ChatKit) — MCP #30 V2.0."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any, List


def _safe_path(p: Path) -> Path:
    resolved = str(p.resolve())
    if os.name == "nt" and not resolved.startswith("\\\\?\\"):
        return Path("\\\\?\\" + resolved)
    return p


class BackendBridgeGenerator:
    """Matérialise les routeurs FastAPI Clean DDD pour connecter le SDK Frontend aux agents IA."""

    def __init__(self, tool_root: Path | None = None):
        self.tool_root = tool_root or Path(__file__).resolve().parents[2]
        self.sessions_dir = self.tool_root / "output" / "sessions"

    def generate_backend_bridge(self, params: Dict[str, Any]) -> Dict[str, Any]:
        session_id = params.get("session_id", "ui-sess-default")
        raw_root = (
            Path(params["target_dir"])
            if params.get("target_dir")
            else (self.sessions_dir / session_id / "backend_bridge")
        )
        target_root = _safe_path(raw_root)
        target_root.mkdir(parents=True, exist_ok=True)

        files_created: List[str] = []

        def _w(rel: str, code: str) -> None:
            f = target_root / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(code.strip() + "\n", encoding="utf-8")
            files_created.append(rel)

        # 1. Routeur ACP (Agent Communication Protocol)
        _w(
            "interfaces/acp_router.py",
            '''"""FastAPI Router — Protocole Standard ACP (Agent Communication Protocol)."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AcpRunInputDto(BaseModel):
    agentName: str = Field("snorbik-orchestrator")
    sessionId: str
    input: str
    attachments: Optional[List[str]] = None
    context: Dict[str, Any] = Field(default_factory=dict)

class AcpMessageOutputDto(BaseModel):
    id: str
    role: str = "assistant"
    content: str
    timestamp: str
    toolCalls: List[Dict[str, Any]] = Field(default_factory=list)

def handle_acp_run(dto: AcpRunInputDto) -> AcpMessageOutputDto:
    return AcpMessageOutputDto(
        id=f"acp-{dto.sessionId}",
        role="assistant",
        content=f"[{dto.agentName}] Exécution ACP certifiée pour : {dto.input}",
        timestamp=datetime.now(timezone.utc).isoformat(),
        toolCalls=[],
    )''',
        )

        # 2. Routeur Google ADK (Agent Development Kit Bridge)
        _w(
            "interfaces/adk_router.py",
            '''"""FastAPI Router — Passerelle Directe Google ADK (Agent Development Kit)."""
from __future__ import annotations
from typing import Dict, Any, List
from pydantic import BaseModel

class AdkRunRequestDto(BaseModel):
    app_name: str
    user_id: str
    session_id: str
    new_message: Dict[str, Any]

def handle_adk_run(dto: AdkRunRequestDto) -> List[Dict[str, Any]]:
    parts = dto.new_message.get("parts", [{}])
    text = parts[0].get("text", "") if parts else ""
    return [{
        "author": dto.app_name,
        "content": {"parts": [{"text": f"[Google ADK Runner] Réponse structurée pour : {text}"}]},
        "partial": False,
    }]''',
        )

        # 3. Routeur OpenAI ChatKit & assistant-ui Session Stream
        _w(
            "interfaces/chatkit_router.py",
            '''"""FastAPI Router — Endpoint de Session pour @openai/chatkit-react & @assistant-ui/react."""
from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel

class ChatKitSessionDto(BaseModel):
    session_id: str
    ui_provider: str = "openai-chatkit"

def create_chatkit_session(dto: ChatKitSessionDto) -> Dict[str, Any]:
    return {
        "session_id": dto.session_id,
        "ui_provider": dto.ui_provider,
        "streaming_enabled": True,
        "supported_protocols": ["ACP", "GOOGLE_ADK", "AG_UI"],
        "status": "READY",
    }''',
        )

        _w(
            "interfaces/__init__.py",
            "from .acp_router import handle_acp_run\nfrom .adk_router import handle_adk_run\nfrom .chatkit_router import create_chatkit_session",
        )

        return {
            "session_id": session_id,
            "backend_bridge_dir": str(raw_root),
            "generated_files_count": len(files_created),
            "generated_files": files_created,
            "supported_protocols": ["ACP", "GOOGLE_ADK", "OPENAI_CHATKIT", "ASSISTANT_UI"],
        }
