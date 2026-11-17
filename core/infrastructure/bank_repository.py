"""Référentiel de la Banque V3.0 : 200 Composants BatiHome, shadcn/Magic UI/21st.dev, ChatKit/ACP/ADK, Archétypes & Stitch."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List


class BankRepository:
    """Magasin central de pièces détachées UI & Skills d'Architecture (3 Cercles de recherche)."""

    def __init__(self, tool_root: Path | None = None):
        self.tool_root = tool_root or Path(__file__).resolve().parents[2]
        self.bank_dir = self.tool_root / "bank"
        self.skills_dir = self.tool_root / "skills"

    def _read_json(self, filename: str) -> Dict[str, Any]:
        p = self.bank_dir / filename
        if not p.exists():
            return {}
        return json.loads(p.read_text(encoding="utf-8"))

    def load_architecture_skills(self) -> Dict[str, Any]:
        skills_summary: List[Dict[str, Any]] = []
        if self.skills_dir.exists():
            for skill_folder in sorted(self.skills_dir.iterdir()):
                skill_md = skill_folder / "SKILL.md"
                if skill_md.exists():
                    lines = skill_md.read_text(encoding="utf-8").splitlines()
                    skills_summary.append({
                        "skill_id": skill_folder.name,
                        "path": str(skill_md.relative_to(self.tool_root)).replace("\\", "/"),
                        "lines_count": len(lines),
                        "headline": next((l.strip("# ") for l in lines if l.startswith("# ")), skill_folder.name),
                    })
        return {
            "skills_loaded_count": len(skills_summary),
            "architectural_rules": {
                "frontend_pattern": "DPN-IA Puzzle 5 Niveaux (01-primitives -> 02-features + useController + partials/ -> 03-sections -> 04-shell -> 05-pages)",
                "line_budget": "60-240L nominal, alerte 300L, plafond strict 350L (INV-02)",
                "car_assembly_rule": "Chasse 3 Cercles : 1. Banque Interne -> 2. MCP Externes Gratuits -> 3. Fabrication IA en dernier recours uniquement",
            },
            "skills": skills_summary,
        }

    def get_full_bank_inventory(self) -> Dict[str, Any]:
        ext_mcp = self._read_json("01_external_ui_mcp_servers.json")
        chat_proto = self._read_json("02_ai_chat_panels_and_protocols.json")
        comp_n1_n5 = self._read_json("03_react_components_n1_to_n5_catalog.json")
        archetypes = self._read_json("04_project_archetypes_and_page_sequences.json")
        stitch = self._read_json("05_stitch_design_system_presets.json")
        internal_200 = self._read_json("06_internal_batihome_200_index.json")

        levels = comp_n1_n5.get("levels", {})
        catalog_count = sum(len(items) for items in levels.values())
        internal_count = internal_200.get("total_indexed", 0)
        return {
            "external_mcp_providers": ext_mcp.get("providers", []),
            "ai_chat_panels": chat_proto.get("chat_panels", []),
            "agent_protocols": chat_proto.get("agent_protocols", []),
            "react_components_by_level": levels,
            "project_archetypes": list(archetypes.get("archetypes", {}).keys()),
            "stitch_presets": list(stitch.get("presets", {}).keys()),
            "summary_counts": {
                "external_mcp_servers": len(ext_mcp.get("providers", [])),
                "ai_chat_panels": len(chat_proto.get("chat_panels", [])),
                "agent_protocols": len(chat_proto.get("agent_protocols", [])),
                "catalog_react_parts": catalog_count,
                "internal_batihome_real_parts": internal_count,
                "total_ready_parts_in_bank": catalog_count + internal_count,
                "project_archetypes": len(archetypes.get("archetypes", {})),
                "stitch_presets": len(stitch.get("presets", {})),
            },
        }

    def match_archetype(self, vision_brief: str, project_type: str | None = None) -> Dict[str, Any]:
        data = self._read_json("04_project_archetypes_and_page_sequences.json").get("archetypes", {})
        if project_type and project_type in data:
            return {"archetype_id": project_type, **data[project_type]}
        q = vision_brief.lower()
        best_id, best_score = "ai_agent_console", 0
        for arch_id, arch in data.items():
            score = sum(1 for kw in arch.get("keywords", []) if kw in q)
            if score > best_score:
                best_id, best_score = arch_id, score
        return {"archetype_id": best_id, **data.get(best_id, {})}

    def get_stitch_preset(self, archetype_id: str, vision_brief: str = "") -> Dict[str, Any]:
        presets = self._read_json("05_stitch_design_system_presets.json").get("presets", {})
        q = vision_brief.lower()
        if "hotel" in q or archetype_id == "hotel_reservation":
            key = "hotel_luxury_hospitality"
        elif any(k in q for k in ("vetement", "fashion", "mode")) or archetype_id == "ecommerce_simple":
            key = "ecommerce_fashion_editorial"
        elif archetype_id == "ecommerce_complexe":
            key = "atelier_contemporain_verre_aluminium"
        elif any(k in q for k in ("medical", "3d", "dark", "bio")):
            key = "biostation_medical_dark"
        else:
            key = "snorbik_studio_clair"
        return {"preset_id": key, **presets.get(key, {})}

    def hunt_parts_3_circles(self, required_parts: Dict[str, List[str]]) -> Dict[str, Any]:
        """Chasse aux pièces en 3 Cercles : 1. Banque Interne -> 2. MCP Externes Gratuits -> 3. Dernier recours IA."""
        internal_levels = self._read_json("06_internal_batihome_200_index.json").get("levels", {})
        catalog_levels = self._read_json("03_react_components_n1_to_n5_catalog.json").get("levels", {})

        results: List[Dict[str, Any]] = []
        counts = {"CIRCLE_1_INTERNAL_BANK": 0, "CIRCLE_2_EXTERNAL_MCP_FREE": 0, "CIRCLE_3_CUSTOM_LAST_RESORT": 0}

        for level, part_names in required_parts.items():
            int_items = internal_levels.get(level, [])
            cat_items = catalog_levels.get(level, [])
            for part_name in part_names:
                p_low = part_name.lower().replace(".tsx", "").replace("page", "").strip()
                # Cercle 1 : Recherche dans notre patrimoine réel (200 composants BatiHome) ou nos composants souverains
                int_hit = next(
                    (it for it in int_items if p_low in it["name"].lower() or any(p_low == t for t in it.get("tags", []))),
                    None,
                )
                if int_hit:
                    counts["CIRCLE_1_INTERNAL_BANK"] += 1
                    results.append({
                        "part_name": part_name,
                        "dpn_level": level,
                        "circle": "CIRCLE_1_INTERNAL_BANK",
                        "matched_asset": int_hit["name"],
                        "source": int_hit["source"],
                        "action": "COPIER_ET_ADAPTER_TOKENS",
                    })
                    continue

                # Cercle 2 : Recherche dans les registres gratuits / MCP UI Externes (shadcn, Magic UI, 21st.dev, ChatKit)
                cat_hit = next(
                    (it for it in cat_items if p_low in it["name"].lower() or any(p_low == t for t in it.get("tags", []))),
                    None,
                )
                if cat_hit:
                    counts["CIRCLE_2_EXTERNAL_MCP_FREE"] += 1
                    results.append({
                        "part_name": part_name,
                        "dpn_level": level,
                        "circle": "CIRCLE_2_EXTERNAL_MCP_FREE",
                        "matched_asset": cat_hit["name"],
                        "source": cat_hit["source"],
                        "action": "INSTALLER_VIA_MCP_EXTERNE_ET_RANGER_DANS_NIVEAU",
                    })
                    continue

                # Cercle 3 : Dernier recours absolu — aucune pièce trouvée
                counts["CIRCLE_3_CUSTOM_LAST_RESORT"] += 1
                results.append({
                    "part_name": part_name,
                    "dpn_level": level,
                    "circle": "CIRCLE_3_CUSTOM_LAST_RESORT",
                    "matched_asset": None,
                    "source": "FABRICATION_SUR_MESURE_DERNIER_RECOURS",
                    "action": "CODER_EN_N2_AVEC_CONTROLLER_ET_PARTIALS",
                })

        total = max(len(results), 1)
        ready_pct = round(((counts["CIRCLE_1_INTERNAL_BANK"] + counts["CIRCLE_2_EXTERNAL_MCP_FREE"]) / total) * 100.0, 1)
        return {
            "total_parts_hunted": len(results),
            "counts_by_circle": counts,
            "ready_parts_reuse_percent": ready_pct,
            "hunted_parts": results,
        }

    def search_bank(
        self, query: str = "", required_features: List[str] | None = None, protocols: List[str] | None = None
    ) -> Dict[str, Any]:
        inv = self.get_full_bank_inventory()
        q_tokens = set(query.lower().replace(",", " ").split())
        for feat in (required_features or []):
            q_tokens.update(feat.lower().split())

        matched_components: List[Dict[str, Any]] = []
        for level_name, comp_list in inv["react_components_by_level"].items():
            for comp in comp_list:
                comp_tags = set(t.lower() for t in comp.get("tags", []))
                if (
                    level_name in ("01-primitives", "04-shell", "05-pages")
                    or comp["component_id"] == "N2-ACP-PILOT-PANEL"
                    or not q_tokens
                    or bool(q_tokens & comp_tags)
                ):
                    matched_components.append({**comp, "dpn_level": level_name})

        return {
            "query": query,
            "matched_components_count": len(matched_components),
            "matched_components": matched_components,
            "recommended_chat_panels": inv["ai_chat_panels"],
            "recommended_agent_protocols": inv["agent_protocols"],
            "external_mcp_fallbacks": inv["external_mcp_providers"],
        }
