"""Porte 3 : SDK Python in-process (< 2ms) V3.0 pour 30_ui_designer_frontend_sdk_mcp."""
from __future__ import annotations

import time
from typing import Dict, Any, List, Optional
from core.domain.entities import ToolRequestDto, ToolResponseDto
from core.application.usecases import ExecuteActionUseCase
from core.infrastructure.adapter import ConcreteOperationalAdapter

RECOMMENDED_PIPELINES: Dict[str, Dict[str, Any]] = {
    "pipeline_zero_maquette_visual_prototyping": {
        "title": "Pipeline 0 — Méthode SNORBIK « Zéro Maquette » (AI Visual Prototyping : Concevoir ➔ Valider ➔ Animer ➔ Reconstruire)",
        "intention": (
            "Quand l'utilisateur n'a aucune maquette : 1. Générer le Prompt Maître Phase 1 (Planche 6 écrans 2x3) pour image-generator -> "
            "2. Validation humaine -> 3. Générer le Prompt Storyboard Vidéo 12s (Phase 2) -> 4. Extraire et reconstruire en React N1->N5."
        ),
        "sequence_exact_tools": [
            "1. ui_designer_init_session",
            "2. ui_designer_qualify_and_plan_pages",
            "3. ui_designer_generate_phase1_design_prompt",
            "4. ui_designer_generate_phase2_video_prompt",
            "5. ui_designer_extract_design_system",
            "6. ui_designer_decompose_n1_to_n5",
            "7. ui_designer_hunt_parts_3_circles",
            "8. ui_designer_materialize_frontend_sdk",
        ],
    },
    "pipeline_usine_montage_voiture_e2e": {
        "title": "Pipeline 1 — Chaîne Complète d'Usine de Montage UI V3.0 (11 Étapes Ordonnées)",
        "intention": (
            "Guide l'IA pas-à-pas comme une chaîne de montage voiture : 1. Qualification (E-commerce simple/complexe, Hôtel, SaaS, Console IA) & Séquences de Pages -> "
            "2. Design System Stitch -> 3. Décomposition N1->N5 -> 4. Chasse aux pièces en 3 Cercles (Banque Interne 200+ -> MCP Gratuits -> Dernier recours IA) -> "
            "5. Blueprint -> 6. Montage SDK React + ACP/ADK + Bridge FastAPI -> 7. Audit L4."
        ),
        "sequence_exact_tools": [
            "1. ui_designer_frontend_sdk_mcp_get_pipelines",
            "2. ui_designer_init_session",
            "3. ui_designer_qualify_and_plan_pages",
            "4. ui_designer_extract_design_system",
            "5. ui_designer_load_architecture_skills",
            "6. ui_designer_decompose_n1_to_n5",
            "7. ui_designer_hunt_parts_3_circles",
            "8. ui_designer_generate_materialization_doc",
            "9. ui_designer_materialize_frontend_sdk",
            "10. ui_designer_generate_backend_bridge",
            "11. ui_designer_audit_architecture",
        ],
    },
    "pipeline_chasse_pieces_banque_express": {
        "title": "Pipeline 2 — Chasse Rapide aux Pièces Détachées (3 Cercles)",
        "intention": "Vérifier en 3 appels quelles pièces existent déjà dans nos 200+ composants BatiHome ou shadcn/Magic UI/ChatKit.",
        "sequence_exact_tools": [
            "1. ui_designer_list_bank_inventory",
            "2. ui_designer_decompose_n1_to_n5",
            "3. ui_designer_hunt_parts_3_circles",
        ],
    },
    "pipeline_backend_bridge_acp_adk": {
        "title": "Pipeline 3 — Génération Ciblée du Pont Backend FastAPI (ACP · Google ADK · ChatKit)",
        "intention": "Générer les routeurs FastAPI Clean DDD (/acp/v1/runs, /adk/run_sse, /chatkit/session) pour connecter l'UI React.",
        "sequence_exact_tools": [
            "1. ui_designer_init_session",
            "2. ui_designer_generate_backend_bridge",
        ],
    },
    "pipeline_rapide_direct": {
        "title": "Pipeline 4 — Exécution Directe One-Shot",
        "intention": "Exécution immédiate sans précurseur pour une action unitaire ou un audit N1-N5.",
        "sequence_exact_tools": [
            "1. ui_designer_frontend_sdk_mcp_run",
        ],
    },
}


class UiDesignerFrontendSdkMcpSdk:
    """Façade programmatique V3.0 pour exécution en mémoire vive haute vitesse (< 2ms)."""

    def __init__(self):
        self.adapter = ConcreteOperationalAdapter()
        self.usecase = ExecuteActionUseCase(adapter=self.adapter)

    def ping(self) -> Dict[str, Any]:
        return {"status": "HEALTHY", "reply": "pong", "version": "3.0.0", "time": time.time()}

    def get_recommended_pipelines(self) -> Dict[str, Any]:
        return {"status": "SUCCESS", "pipelines_count": len(RECOMMENDED_PIPELINES), "pipelines": RECOMMENDED_PIPELINES}

    def execute(self, action: str = "execute", parameters: Optional[Dict[str, Any]] = None) -> ToolResponseDto:
        return self.usecase.execute(ToolRequestDto(action=action, parameters=parameters or {}))

    def init_session(
        self,
        project_name: str,
        vision_brief: str,
        mockup_image_path: Optional[str] = None,
        agent_protocols: Optional[List[str]] = None,
        custom_features: Optional[List[str]] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.execute(
            "init_session",
            {
                "session_id": session_id,
                "project_name": project_name,
                "vision_brief": vision_brief,
                "mockup_image_path": mockup_image_path,
                "agent_protocols": agent_protocols or ["ACP", "GOOGLE_ADK", "OPENAI_CHATKIT", "ASSISTANT_UI"],
                "custom_features": custom_features or [],
            },
        ).payload

    def qualify_and_plan_pages(self, session_id: str, project_type: Optional[str] = None, vision_brief: Optional[str] = None) -> Dict[str, Any]:
        return self.execute("qualify_and_plan_pages", {"session_id": session_id, "project_type": project_type, "vision_brief": vision_brief}).payload

    def extract_design_system(self, session_id: str) -> Dict[str, Any]:
        return self.execute("extract_design_system", {"session_id": session_id}).payload

    def decompose_n1_to_n5(self, session_id: str, custom_features: Optional[List[str]] = None) -> Dict[str, Any]:
        return self.execute("decompose_n1_to_n5", {"session_id": session_id, "custom_features": custom_features or []}).payload

    def hunt_parts_3_circles(self, session_id: str) -> Dict[str, Any]:
        return self.execute("hunt_parts_3_circles", {"session_id": session_id}).payload

    def generate_phase1_design_prompt(self, session_id: str, project_name: Optional[str] = None, vision_brief: Optional[str] = None) -> Dict[str, Any]:
        return self.execute("generate_phase1_design_prompt", {"session_id": session_id, "project_name": project_name, "vision_brief": vision_brief}).payload

    def generate_phase2_video_prompt(self, session_id: str, duration_seconds: int = 12) -> Dict[str, Any]:
        return self.execute("generate_phase2_video_prompt", {"session_id": session_id, "duration_seconds": duration_seconds}).payload

    def analyze_mockup(self, session_id: str, mockup_image_path: Optional[str] = None, vision_brief: Optional[str] = None) -> Dict[str, Any]:
        return self.execute("analyze_mockup", {"session_id": session_id, "mockup_image_path": mockup_image_path, "vision_brief": vision_brief}).payload

    def load_architecture_skills(self) -> Dict[str, Any]:
        return self.execute("load_architecture_skills", {}).payload

    def list_bank_inventory(self) -> Dict[str, Any]:
        return self.execute("list_bank_inventory", {}).payload

    def search_bank(self, query: str = "", required_features: Optional[List[str]] = None, protocols: Optional[List[str]] = None) -> Dict[str, Any]:
        return self.execute("search_bank", {"query": query, "required_features": required_features or [], "protocols": protocols or []}).payload

    def generate_materialization_doc(self, session_id: str, **kwargs: Any) -> Dict[str, Any]:
        return self.execute("generate_materialization_doc", {"session_id": session_id, **kwargs}).payload

    def materialize_frontend_sdk(self, session_id: str, target_dir: Optional[str] = None) -> Dict[str, Any]:
        return self.execute("materialize_frontend_sdk", {"session_id": session_id, "target_dir": target_dir}).payload

    def generate_backend_bridge(self, session_id: str, target_dir: Optional[str] = None) -> Dict[str, Any]:
        return self.execute("generate_backend_bridge", {"session_id": session_id, "target_dir": target_dir}).payload

    def audit_architecture(self, session_id: str = "ui-sess-default", target_dir: Optional[str] = None) -> Dict[str, Any]:
        return self.execute("audit_architecture", {"session_id": session_id, "target_dir": target_dir}).payload
