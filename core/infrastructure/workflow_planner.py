"""Planificateur de Montage Voiture UI V3.0 : Qualification, Pages/Séquences, Design System Stitch, N1-N5 & Chasse 3 Cercles."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List
from core.infrastructure.bank_repository import BankRepository
from core.infrastructure.path_utils import safe_path


class WorkflowPlanner:
    """Orchestre les 4 étapes de préparation avant tout assemblage de code React."""

    def __init__(self, tool_root: Path | None = None):
        self.tool_root = tool_root or Path(__file__).resolve().parents[2]
        self.sessions_dir = self.tool_root / "output" / "sessions"
        self.bank_repo = BankRepository(self.tool_root)

    def _load_state(self, session_id: str) -> tuple[Path, Dict[str, Any]]:
        s_dir = safe_path(self.sessions_dir / session_id)
        s_dir.mkdir(parents=True, exist_ok=True)
        state_file = s_dir / "session_state.json"
        if state_file.exists():
            return state_file, json.loads(state_file.read_text(encoding="utf-8"))
        return state_file, {"session_id": session_id, "project_name": "SnorbikApp", "vision_brief": "", "agent_protocols": ["ACP", "GOOGLE_ADK", "OPENAI_CHATKIT"]}

    def _save_state(self, state_file: Path, state: Dict[str, Any]) -> None:
        safe_path(state_file).write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    def qualify_and_plan_pages(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Étape 1 : Qualifie le type de projet, le cahier des charges des pages et le diagramme de séquence de chaque page."""
        session_id = params.get("session_id", "ui-sess-default")
        state_file, state = self._load_state(session_id)
        vision = params.get("vision_brief") or state.get("vision_brief", "")
        arch = self.bank_repo.match_archetype(vision, params.get("project_type"))

        s_dir = state_file.parent
        spec_path = s_dir / "PAGES_AND_SEQUENCES_SPEC.md"
        lines = [
            f"# 📋 CAHIER DES CHARGES DES PAGES & SÉQUENCES — `{state.get('project_name')}`",
            f"- **Type de Projet Qualifié :** `{arch['archetype_id']}` ({arch.get('label', '')})",
            f"- **Vision :** {vision}",
            "",
        ]
        for pg in arch.get("pages", []):
            lines.append(f"## {pg['page_id']} — {pg['name']}")
            lines.append("**Contenu de la page :** " + ", ".join(pg.get("content", [])))
            lines.append("**Diagramme de séquence utilisateur :**")
            for step in pg.get("sequence", []):
                lines.append(f"- {step}")
            lines.append("")

        spec_path.write_text("\n".join(lines), encoding="utf-8")
        res = {
            "session_id": session_id,
            "archetype_id": arch["archetype_id"],
            "archetype_label": arch.get("label", ""),
            "pages_count": len(arch.get("pages", [])),
            "pages": arch.get("pages", []),
            "spec_document_path": str(spec_path),
        }
        state["qualification"] = res
        self._save_state(state_file, state)
        return res

    def extract_design_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Étape 2 : Extrait/génère le Design System style Stitch (lettres, fond, couleurs, tokens CSS)."""
        session_id = params.get("session_id", "ui-sess-default")
        state_file, state = self._load_state(session_id)
        arch_id = state.get("qualification", {}).get("archetype_id", "ai_agent_console")
        preset = self.bank_repo.get_stitch_preset(arch_id, state.get("vision_brief", ""))

        colors = preset.get("colors", {})
        typo = preset.get("typography", {})
        s_dir = state_file.parent
        css_path = s_dir / "tokens.css"
        css_lines = [
            f"/* DESIGN SYSTEM STITCH PRESET : {preset.get('preset_id')} */",
            ":root {",
            f"  --font-display: '{typo.get('font_display', 'Inter')}', sans-serif;",
            f"  --font-body: '{typo.get('font_body', 'Inter')}', sans-serif;",
            f"  --font-mono: '{typo.get('font_mono', 'JetBrains Mono')}', monospace;",
        ]
        for k, v in colors.items():
            css_lines.append(f"  --{k.replace('_', '-')}: {v};")
        css_lines.append(f"  --radius-base: {preset.get('radius', '12px')};")
        css_lines.append("}")
        css_path.write_text("\n".join(css_lines) + "\n", encoding="utf-8")

        md_path = s_dir / "DESIGN_SYSTEM_STITCH.md"
        md_path.write_text(
            f"# 🎨 DESIGN SYSTEM STITCH — `{preset.get('label', preset.get('preset_id'))}`\n"
            f"- **Typographie :** Display `{typo.get('font_display')}` | Body `{typo.get('font_body')}` | Mono `{typo.get('font_mono')}`\n"
            f"- **Couleur de Fond (`surface_canvas`) :** `{colors.get('surface_canvas')}`\n"
            f"- **Couleur Primaire :** `{colors.get('color_primary')}` | **Secondaire :** `{colors.get('color_secondary')}`\n"
            f"- **Fichier CSS généré :** `{css_path.name}`\n",
            encoding="utf-8",
        )
        res = {"session_id": session_id, "preset": preset, "tokens_css_path": str(css_path), "design_doc_path": str(md_path)}
        state["design_system"] = res
        self._save_state(state_file, state)
        return res

    def decompose_n1_to_n5(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Étape 3 : Décompose les pages et la maquette en liste complète de pièces classées N1 -> N5."""
        session_id = params.get("session_id", "ui-sess-default")
        state_file, state = self._load_state(session_id)
        if "qualification" not in state:
            self.qualify_and_plan_pages({"session_id": session_id})
            _, state = self._load_state(session_id)

        merged: Dict[str, List[str]] = {
            "01-primitives": [],
            "02-features": [],
            "03-sections": [],
            "04-shell": [],
            "05-pages": [],
        }
        for pg in state["qualification"].get("pages", []):
            for lvl, parts in pg.get("required_parts", {}).items():
                for p in parts:
                    if p not in merged[lvl]:
                        merged[lvl].append(p)
        for cf in (state.get("custom_features") or params.get("custom_features") or []):
            if cf not in merged["02-features"]:
                merged["02-features"].append(cf)

        res = {
            "session_id": session_id,
            "total_required_parts": sum(len(v) for v in merged.values()),
            "required_parts_by_level": merged,
        }
        state["decomposition_n1_to_n5"] = res
        self._save_state(state_file, state)
        return res

    def hunt_parts_3_circles(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Étape 4 : Exécute la chasse aux pièces détachées en 3 Cercles avant toute écriture de code."""
        session_id = params.get("session_id", "ui-sess-default")
        state_file, state = self._load_state(session_id)
        if "decomposition_n1_to_n5" not in state:
            self.decompose_n1_to_n5({"session_id": session_id})
            _, state = self._load_state(session_id)

        required = state["decomposition_n1_to_n5"]["required_parts_by_level"]
        hunt = self.bank_repo.hunt_parts_3_circles(required)
        state["parts_hunt_3_circles"] = hunt
        self._save_state(state_file, state)
        return {"session_id": session_id, **hunt}
