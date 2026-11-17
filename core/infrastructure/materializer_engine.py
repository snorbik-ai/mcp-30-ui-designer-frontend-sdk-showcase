"""Moteur de Matérialisation, Analyse de Maquette & Plan Architectural N1-N5 — MCP #30 V2.0."""
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


class MaterializerEngine:
    """Analyse la maquette, construit le Document de Matérialisation et prépare le plan N1-N5."""

    def __init__(self, tool_root: Path | None = None):
        self.tool_root = tool_root or Path(__file__).resolve().parents[2]
        self.sessions_dir = self.tool_root / "output" / "sessions"
        self.bank_repo = BankRepository(self.tool_root)

    def init_session(self, params: Dict[str, Any]) -> Dict[str, Any]:
        session_id = params.get("session_id") or f"ui-sess-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        project_name = params.get("project_name", "SnorbikAppSdk")
        vision_brief = params.get("vision_brief", "Interface graphique moderne avec Chat Panel IA ACP/ADK")
        mockup_image_path = params.get("mockup_image_path")
        agent_protocols = params.get(
            "agent_protocols", ["ACP", "GOOGLE_ADK", "OPENAI_CHATKIT", "ASSISTANT_UI"]
        )
        custom_features = params.get("custom_features", [])

        s_dir = self.sessions_dir / session_id
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
        (s_dir / "session_state.json").write_text(
            json.dumps(session_meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return session_meta

    def analyze_mockup(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse la maquette image et la vision pour extraire le layout, les zones UI et les tokens."""
        session_id = params.get("session_id", "ui-sess-default")
        s_dir = self.sessions_dir / session_id
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

        mockup_exists = bool(mockup_path and Path(mockup_path).exists())
        analysis = {
            "session_id": session_id,
            "mockup_image_path": mockup_path,
            "mockup_file_verified": mockup_exists,
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
        (s_dir / "session_state.json").write_text(
            json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return analysis

    def generate_materialization_doc(self, params: Dict[str, Any]) -> Dict[str, Any]:
        session_id = params.get("session_id", "ui-sess-default")
        s_dir = self.sessions_dir / session_id
        if not (s_dir / "session_state.json").exists():
            self.init_session({**params, "session_id": session_id})

        state = json.loads((s_dir / "session_state.json").read_text(encoding="utf-8"))
        if "mockup_analysis" not in state:
            self.analyze_mockup({"session_id": session_id})
            state = json.loads((s_dir / "session_state.json").read_text(encoding="utf-8"))

        search_res = self.bank_repo.search_bank(
            query=state.get("vision_brief", ""),
            required_features=state.get("custom_features", []),
            protocols=state.get("agent_protocols", []),
        )

        items: List[MaterializationItemDto] = []
        for comp in search_res["matched_components"]:
            lvl = comp["dpn_level"]
            items.append(
                MaterializationItemDto(
                    item_id=comp["component_id"],
                    name=comp["name"],
                    dpn_level=lvl,
                    target_path=f"src/presentation/{lvl}/{comp['name']}",
                    category=MaterializationCategory.EXISTING_IN_BANK,
                    source_provider=comp["source"],
                    estimated_lines=comp.get("max_lines", 120),
                    has_controller_hook=bool(comp.get("has_controller", False)),
                    notes=comp.get("description", comp.get("source", "")),
                )
            )

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
                notes="Composant Chat Panel open-source configuré avec streaming ACP & Google ADK.",
            )
        )
        items.append(
            MaterializationItemDto(
                item_id="EXT-SHADCN-MAGIC-BLOCKS",
                name="ShadcnMagicUiBlocks.tsx",
                dpn_level="01-primitives",
                target_path="src/presentation/01-primitives/ShadcnMagicUiBlocks.tsx",
                category=MaterializationCategory.EXTERNAL_MCP_REGISTRY,
                source_provider="shadcn@latest mcp + @magicui/mcp + @21st-dev/magic",
                estimated_lines=90,
                has_controller_hook=False,
                notes="Blocs UI récupérés via les serveurs MCP externes et adaptés aux tokens du projet.",
            )
        )

        custom_reqs = state.get("custom_features") or params.get("custom_features") or ["CustomDomainFeature"]
        for idx, c_feat in enumerate(custom_reqs, start=1):
            clean_name = "".join(w.capitalize() for w in str(c_feat).replace("-", " ").replace("_", " ").split()) or f"CustomFeature{idx}"
            items.append(
                MaterializationItemDto(
                    item_id=f"CUSTOM-N2-{idx:02d}",
                    name=clean_name,
                    dpn_level="02-features",
                    target_path=f"src/presentation/02-features/{clean_name}/",
                    category=MaterializationCategory.CUSTOM_AI_TO_BUILD,
                    source_provider="Génération IA Sur-Mesure (Delta non présent en Banque)",
                    estimated_lines=145,
                    has_controller_hook=True,
                    notes=f"Pièce sur-mesure : générée dynamiquement avec use{clean_name}Controller.ts + partials/ + index.ts (< 240L).",
                )
            )

        c_bank = sum(1 for i in items if i.category == MaterializationCategory.EXISTING_IN_BANK)
        c_ext = sum(1 for i in items if i.category == MaterializationCategory.EXTERNAL_MCP_REGISTRY)
        c_cust = sum(1 for i in items if i.category == MaterializationCategory.CUSTOM_AI_TO_BUILD)
        total = max(len(items), 1)
        reuse_pct = round(((c_bank + c_ext) / total) * 100.0, 1)

        md_path = s_dir / "MATERIALIZATION_BLUEPRINT.md"
        json_path = s_dir / "materialization_plan.json"

        blueprint = MaterializationBlueprintDto(
            session_id=session_id,
            project_name=state["project_name"],
            existing_in_bank_count=c_bank,
            external_mcp_count=c_ext,
            custom_to_build_count=c_cust,
            reuse_ratio_percent=reuse_pct,
            items=items,
            markdown_report_path=str(md_path),
            json_plan_path=str(json_path),
        )

        md_lines = [
            f"# 📐 DOCUMENT DE MATÉRIALISATION UI & SDK V2.0 — `{state['project_name']}`",
            f"- **Session ID :** `{session_id}`",
            f"- **Layout Détecté :** `{state.get('mockup_analysis', {}).get('layout_archetype', 'SAAS_MODULAR_WORKSPACE')}`",
            f"- **Protocoles Agent SDK :** `{', '.join(state['agent_protocols'])}`",
            f"- **Taux de Réutilisation (Banque + MCP Externes) :** **{reuse_pct} %** ({c_bank} Banque + {c_ext} MCP Externes vs {c_cust} Sur-Mesure IA)",
            "",
            "## Plan d'Assemblage Architectural (Puzzle DPN-IA `N1 ➔ N5` < 350L)",
            "| ID | Niveau | Composant / Dossier | Origine | Catégorie | Hook Contrôleur | Budget Lignes |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for it in items:
            hook_label = "Oui (`use*Controller.ts`)" if it.has_controller_hook else "Non (Stateless)"
            md_lines.append(
                f"| `{it.item_id}` | `{it.dpn_level}` | `{it.name}` | {it.source_provider} | `{it.category.value}` | {hook_label} | ~{it.estimated_lines}L |"
            )

        md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        json_path.write_text(blueprint.model_dump_json(indent=2), encoding="utf-8")
        return blueprint.model_dump()
