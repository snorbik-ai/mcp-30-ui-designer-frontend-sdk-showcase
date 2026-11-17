"""Entités de domaine pures et contrats DTO Pydantic V2 — MCP #30 UI Designer & Frontend SDK."""
from __future__ import annotations

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class OperationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class MaterializationCategory(str, Enum):
    EXISTING_IN_BANK = "EXISTING_IN_BANK"
    EXTERNAL_MCP_REGISTRY = "EXTERNAL_MCP_REGISTRY"
    CUSTOM_AI_TO_BUILD = "CUSTOM_AI_TO_BUILD"


class UiSessionInitInputDto(BaseModel):
    session_id: Optional[str] = Field(None, description="ID de session (auto-généré si omis).")
    project_name: str = Field(..., description="Nom du projet ou de l'interface cible.")
    vision_brief: str = Field(..., description="Idée, vision métier et besoins fonctionnels.")
    mockup_image_path: Optional[str] = Field(None, description="Chemin optionnel vers la maquette image.")
    agent_protocols: List[str] = Field(
        default_factory=lambda: ["ACP", "GOOGLE_ADK", "OPENAI_CHATKIT", "ASSISTANT_UI"],
        description="Protocoles et Chat Panels IA à intégrer dans le SDK Frontend."
    )


class MaterializationItemDto(BaseModel):
    item_id: str
    name: str
    dpn_level: str
    target_path: str
    category: MaterializationCategory
    source_provider: str
    estimated_lines: int
    has_controller_hook: bool = False
    notes: str = ""


class MaterializationBlueprintDto(BaseModel):
    session_id: str
    project_name: str
    existing_in_bank_count: int
    external_mcp_count: int
    custom_to_build_count: int
    reuse_ratio_percent: float
    items: List[MaterializationItemDto] = Field(default_factory=list)
    markdown_report_path: str = ""
    json_plan_path: str = ""


class ToolRequestDto(BaseModel):
    action: str = Field("execute", description="Nom de l'action à opérer.")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Paramètres d'entrée.")


class ToolResponseDto(BaseModel):
    operation_id: str
    action: str
    status: OperationStatus
    payload: Dict[str, Any] = Field(default_factory=dict)
    execution_duration_ms: float
    error_message: Optional[str] = None
