"""Moteur de Matérialisation, Analyse de Maquette & Plan Architectural N1-N5 — MCP #30 V3.0."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from core.domain.entities import (
    MaterializationCategory,
    MaterializationItemDto,
    MaterializationBlueprintDto,
)
from core.infrastructure.bank_repository import BankRepository
from core.infrastructure.path_utils import safe_path
from core.infrastructure.workflow_planner import WorkflowPlanner


class MaterializerEngine:
    """Analyse la maquette, exploite la Chasse 3 Cercles et construit le Document de Matérialisation N1-N5."""

    def __init__(self, tool_root: Path | None = None):
        self.tool_root = tool_root or Path(__file__).resolve().parents[2]
        self.sessions_dir = self.tool_root / "output" / "sessions"
        self.bank_repo = BankRepository(self.tool_root)
        self.planner = WorkflowPlanner(self.tool_root)

    def init_session(self, params: Dict[str, Any]) -> Dict[str, Any]:
        session_id = params.get("session_id") or f"ui-sess-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        project_name = params.get("project_name", "SnorbikAppSdk")
        vision_brief = params.get("vision_brief", "Interface graphique moderne avec Chat Panel IA ACP/ADK")
        mockup_image_path = params.get("mockup_image_path")
        agent_protocols = params.get("agent_protocols", ["ACP", "GOOGLE_ADK", "OPENAI_CHATKIT", "ASSISTANT_UI"])
        custom_features = params.get("custom_features", [])

        s_dir = safe_path(self.sessions_dir / session_id)
        s_dir.mkdir(parents=True, exist_ok=True)
        skills_info = self.bank_repo.load_architecture_skills()
        session_meta = {
            "session_id": session_id,
            "project_name": project_name,
            "vision_brief": vision_brief,
            "mockup_image_path": mockup_image_path,
            "agent_protocols": agent_protocols,
            "custom_features": custom_features,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "architecture_skills_loaded": skills_info["skills_loaded_count"],
            "status": "INITIALIZED_WITH_SKILLS",
        }
        (s_dir / "session_state.json").write_text(json.dumps(session_meta, indent=2, ensure_ascii=False), encoding="utf-8")
        return session_meta

    def analyze_mockup(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse la maquette image et la vision pour extraire le layout, les zones UI et les tokens."""
        session_id = params.get("session_id", "ui-sess-default")
        s_dir = safe_path(self.sessions_dir / session_id)
        if not (s_dir / "session_state.json").exists():
            self.init_session({**params, "session_id": session_id})

        state = json.loads((s_dir / "session_state.json").read_text(encoding="utf-8"))
        brief_lower = (state.get("vision_brief", "") + " " + str(params.get("vision_brief", ""))).lower()
        mockup_path = params.get("mockup_image_path") or state.get("mockup_image_path")

        if any(k in brief_lower for k in ("3d", "medical", "workbench", "studio", "console")):
            archetype = "WORKBENCH_3_COLUMNS_PRO"
            zones = ["LeftNavigationRail (320px)", "CenterFlexibleViewport (3D/Canvas)", "RightAcpPilotPanel (360px)"]
        elif any(k in brief_lower for k in ("ecommerce", "catalogue", "shop", "devis", "boutique")):
            archetype = "ECOMMERCE_SPLIT_SHOWCASE"
            zones = ["HeaderMegaMenu", "CommercialHeroSection", "FacetedCatalogGrid", "SlideOverAcpCopilotDrawer"]
        else:
            archetype = "SAAS_MODULAR_WORKSPACE"
            zones = ["TopStatusHeader", "MainSplitWorkspace", "RightAcpChatKitDock"]

        analysis = {
            "session_id": session_id,
            "mockup_image_path": mockup_path,
            "mockup_file_verified": bool(mockup_path and Path(mockup_path).exists()),
            "layout_archetype": archetype,
            "detected_ui_zones": zones,
            "design_tokens": {
                "surface_canvas": "#F8FAFC",
                "header_brand": "#0F172A",
                "accent_primary": "#059669",
                "accent_secondary": "#0284C7",
                "accent_ai_purple": "#7C3AED",
                "max_container_width": "1440px",
            },
            "recommended_dpn_mapping": {
                "04-shell": "WorkbenchLayout.tsx",
                "03-sections": "SplitWorkbenchSection.tsx",
                "02-features": ["acp-pilot-panel/", *(state.get("custom_features") or [])],
            },
        }
        state["mockup_analysis"] = analysis
        state["status"] = "MOCKUP_ANALYZED"
        (s_dir / "session_state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        return analysis

    def generate_materialization_doc(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Génère le Document de Matérialisation V3.0 en exploitant directement la Chasse en 3 Cercles."""
        session_id = params.get("session_id", "ui-sess-default")
        s_dir = safe_path(self.sessions_dir / session_id)
        if not (s_dir / "session_state.json").exists():
            self.init_session({**params, "session_id": session_id})

        state = json.loads((s_dir / "session_state.json").read_text(encoding="utf-8"))
        if "qualification" not in state:
            self.planner.qualify_and_plan_pages({"session_id": session_id})
        if "design_system" not in state:
            self.planner.extract_design_system({"session_id": session_id})
        if "parts_hunt_3_circles" not in state:
            self.planner.hunt_parts_3_circles({"session_id": session_id})
        if "mockup_analysis" not in state:
            self.analyze_mockup({"session_id": session_id})
        state = json.loads((s_dir / "session_state.json").read_text(encoding="utf-8"))

        items: List[MaterializationItemDto] = []
        seen_names: set[str] = set()
        circle_map = {
            "CIRCLE_1_INTERNAL_BANK": MaterializationCategory.EXISTING_IN_BANK,
            "CIRCLE_2_EXTERNAL_MCP_FREE": MaterializationCategory.EXTERNAL_MCP_REGISTRY,
            "CIRCLE_3_CUSTOM_LAST_RESORT": MaterializationCategory.CUSTOM_AI_TO_BUILD,
        }

        for idx, h in enumerate(state.get("parts_hunt_3_circles", {}).get("hunted_parts", []), start=1):
            lvl = h["dpn_level"]
            asset_name = h.get("matched_asset") or h["part_name"]
            cat = circle_map.get(h["circle"], MaterializationCategory.CUSTOM_AI_TO_BUILD)
            clean = "".join(w.capitalize() for w in str(asset_name).replace("-", " ").replace("_", " ").split()) or asset_name
            seen_names.add(h["part_name"].lower())
            items.append(
                MaterializationItemDto(
                    item_id=f"PART-{idx:02d}",
                    name=asset_name if cat != MaterializationCategory.CUSTOM_AI_TO_BUILD else clean,
                    dpn_level=lvl,
                    target_path=f"src/presentation/{lvl}/{asset_name}",
                    category=cat,
                    source_provider=h.get("source", "Banque SNORBIK"),
                    estimated_lines=145 if cat == MaterializationCategory.CUSTOM_AI_TO_BUILD else 95,
                    has_controller_hook=(lvl == "02-features"),
                    notes=f"{h['circle']} -> {h['action']}",
                )
            )

        if "openaichatkitstreampartial.tsx" not in seen_names:
            items.append(
                MaterializationItemDto(
                    item_id="EXT-CHATKIT-STREAM",
                    name="OpenAiChatKitStreamPartial.tsx",
                    dpn_level="02-features",
                    target_path="src/presentation/02-features/acp-pilot-panel/partials/OpenAiChatKitStreamPartial.tsx",
                    category=MaterializationCategory.EXTERNAL_MCP_REGISTRY,
                    source_provider="@openai/chatkit-react + @assistant-ui/react",
                    estimated_lines=115,
                    has_controller_hook=True,
                    notes="Chat Panel open-source configuré avec streaming ACP & Google ADK.",
                )
            )

        c_bank = sum(1 for i in items if i.category == MaterializationCategory.EXISTING_IN_BANK)
        c_ext = sum(1 for i in items if i.category == MaterializationCategory.EXTERNAL_MCP_REGISTRY)
        c_cust = sum(1 for i in items if i.category == MaterializationCategory.CUSTOM_AI_TO_BUILD)
        reuse_pct = round(((c_bank + c_ext) / max(len(items), 1)) * 100.0, 1)

        md_path = safe_path(s_dir / "MATERIALIZATION_BLUEPRINT.md")
        json_path = safe_path(s_dir / "materialization_plan.json")
        blueprint = MaterializationBlueprintDto(
            session_id=session_id,
            project_name=state["project_name"],
            existing_in_bank_count=c_bank,
            external_mcp_count=c_ext,
            custom_to_build_count=c_cust,
            reuse_ratio_percent=reuse_pct,
            items=items,
            markdown_report_path=str(s_dir / "MATERIALIZATION_BLUEPRINT.md"),
            json_plan_path=str(s_dir / "materialization_plan.json"),
        )

        arch_id = state.get("qualification", {}).get("archetype_id", "ai_agent_console")
        md_lines = [
            f"# 📐 DOCUMENT DE MATÉRIALISATION UI & SDK V3.0 — `{state['project_name']}`",
            f"- **Session ID :** `{session_id}` | **Archétype :** `{arch_id}`",
            f"- **Protocoles Agent SDK :** `{', '.join(state['agent_protocols'])}`",
            f"- **Taux de Réutilisation (3 Cercles) :** **{reuse_pct} %** ({c_bank} Cercle 1 Interne + {c_ext} Cercle 2 MCP Gratuits vs {c_cust} Cercle 3 Sur-Mesure IA)",
            "",
            "## Plan d'Assemblage Architectural (Puzzle DPN-IA `N1 ➔ N5` < 350L)",
            "| ID | Niveau | Composant / Dossier | Origine | Catégorie | Hook Contrôleur | Budget Lignes |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for it in items:
            hook_label = "Oui (`use*Controller.ts`)" if it.has_controller_hook else "Non (Stateless)"
            md_lines.append(f"| `{it.item_id}` | `{it.dpn_level}` | `{it.name}` | {it.source_provider} | `{it.category.value}` | {hook_label} | ~{it.estimated_lines}L |")

        md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        json_path.write_text(blueprint.model_dump_json(indent=2), encoding="utf-8")
        return blueprint.model_dump()
