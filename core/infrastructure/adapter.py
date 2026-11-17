"""Adaptateur d'infrastructure concret V3.0 — MCP #30 UI Designer & Usine de Montage Voiture."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from core.domain.ports import IOperationalAdapter
from core.infrastructure.bank_repository import BankRepository
from core.infrastructure.workflow_planner import WorkflowPlanner
from core.infrastructure.visual_prototyping_guide import VisualPrototypingGuide
from core.infrastructure.materializer_engine import MaterializerEngine
from core.infrastructure.sdk_builder_auditor import SdkBuilderAndAuditor
from core.infrastructure.backend_bridge_generator import BackendBridgeGenerator


class ConcreteOperationalAdapter(IOperationalAdapter):
    """Adaptateur déterministe V3.0 : Qualification, Stitch, N1-N5, Chasse 3 Cercles, SDK & Bridge FastAPI."""

    def __init__(self):
        self.bank_repo = BankRepository()
        self.planner = WorkflowPlanner()
        self.visual_guide = VisualPrototypingGuide()
        self.materializer = MaterializerEngine()
        self.sdk_builder = SdkBuilderAndAuditor()
        self.backend_bridge = BackendBridgeGenerator()

    def execute_operation(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.process_action(action, params)

    def process_action(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        act = (action or "execute").strip().lower()

        if act in ("ping", "health"):
            return {"status": "HEALTHY", "service": "30_ui_designer_frontend_sdk_mcp", "version": "3.0.0"}

        if act in ("init_session", "ui_designer_init_session"):
            return self.materializer.init_session(parameters)

        if act in ("qualify_and_plan_pages", "ui_designer_qualify_and_plan_pages"):
            return self.planner.qualify_and_plan_pages(parameters)

        if act in ("extract_design_system", "ui_designer_extract_design_system"):
            return self.planner.extract_design_system(parameters)

        if act in ("decompose_n1_to_n5", "ui_designer_decompose_n1_to_n5"):
            return self.planner.decompose_n1_to_n5(parameters)

        if act in ("hunt_parts_3_circles", "ui_designer_hunt_parts_3_circles"):
            return self.planner.hunt_parts_3_circles(parameters)

        if act in ("generate_phase1_design_prompt", "ui_designer_generate_phase1_design_prompt"):
            return self.visual_guide.generate_phase1_design_prompt(parameters)

        if act in ("generate_phase2_video_prompt", "ui_designer_generate_phase2_video_prompt"):
            return self.visual_guide.generate_phase2_video_prompt(parameters)

        if act in ("analyze_mockup", "ui_designer_analyze_mockup"):
            return self.materializer.analyze_mockup(parameters)

        if act in ("load_skills", "load_architecture_skills", "ui_designer_load_architecture_skills"):
            return self.bank_repo.load_architecture_skills()

        if act in ("list_bank", "list_bank_inventory", "ui_designer_list_bank_inventory"):
            return self.bank_repo.get_full_bank_inventory()

        if act in ("search_bank", "ui_designer_search_bank"):
            return self.bank_repo.search_bank(
                query=parameters.get("query", ""),
                required_features=parameters.get("required_features", []),
                protocols=parameters.get("protocols", []),
            )

        if act in ("generate_materialization_doc", "ui_designer_generate_materialization_doc"):
            return self.materializer.generate_materialization_doc(parameters)

        if act in ("materialize_sdk", "materialize_frontend_sdk", "ui_designer_materialize_frontend_sdk"):
            return self.sdk_builder.materialize_frontend_sdk(parameters)

        if act in ("generate_backend_bridge", "ui_designer_generate_backend_bridge"):
            return self.backend_bridge.generate_backend_bridge(parameters)

        if act in ("audit_architecture", "ui_designer_audit_architecture"):
            return self.sdk_builder.audit_architecture(parameters)

        return {
            "processed_action": action,
            "version": "3.0.0",
            "received_keys": list(parameters.keys()),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "trace_token": uuid.uuid4().hex[:12],
            "bank_summary": self.bank_repo.get_full_bank_inventory()["summary_counts"],
            "skills_loaded": self.bank_repo.load_architecture_skills()["skills_loaded_count"],
        }
