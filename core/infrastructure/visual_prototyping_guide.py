"""Générateur de Prompts & Workflows « AI Visual Prototyping » (Zéro Maquette -> Phase 1 Image 2x3 -> Phase 2 Vidéo 12s)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List
from core.infrastructure.bank_repository import BankRepository
from core.infrastructure.path_utils import safe_path as _safe_path


class VisualPrototypingGuide:
    """Fournit à l'agent IA les prompts complets Phase 1 (Visual Design) et Phase 2 (Video Prototyping) sans maquette préalable."""

    def __init__(self, tool_root: Path | None = None):
        self.tool_root = tool_root or Path(__file__).resolve().parents[2]
        self.sessions_dir = self.tool_root / "output" / "sessions"
        self.bank_repo = BankRepository(self.tool_root)

    def _load_state(self, session_id: str) -> tuple[Path, Dict[str, Any]]:
        s_dir = self.sessions_dir / session_id
        s_dir.mkdir(parents=True, exist_ok=True)
        sf = s_dir / "session_state.json"
        if sf.exists():
            return sf, json.loads(sf.read_text(encoding="utf-8"))
        return sf, {"session_id": session_id, "project_name": "SnorbikProduct", "vision_brief": "Application SaaS IA"}

    def _build_6_screens(self, state: Dict[str, Any], params: Dict[str, Any]) -> List[Dict[str, str]]:
        custom_screens = params.get("screens")
        if isinstance(custom_screens, list) and len(custom_screens) >= 4:
            return custom_screens[:6]

        vision = (params.get("vision_brief") or state.get("vision_brief") or "").lower()
        if any(k in vision for k in ("bio", "atlas", "medical", "genom", "vcf", "3d")):
            return [
                {"id": "Écran 01", "name": "Main Dashboard", "desc": "Vue générale du projet, liste des analyses, indicateurs de progression, accès aux espaces de travail et historique."},
                {"id": "Écran 02", "name": "Genomic Data Import", "desc": "Import de fichiers génomiques (VCF), informations échantillons, statut de validation et vue structurée des données."},
                {"id": "Écran 03", "name": "Variant Analysis", "desc": "Tableau d'exploration des variants, filtres, critères de sélection et panneau de détail d'un variant."},
                {"id": "Écran 04", "name": "Genome Explorer", "desc": "Visualisation du génome et des chromosomes, navigation dans les régions génomiques et position des variants."},
                {"id": "Écran 05", "name": "Molecular 3D Visualization", "desc": "Structure moléculaire 3D détaillée de la protéine, mise en évidence des régions mutées et outils de rotation."},
                {"id": "Écran 06", "name": "Analysis Report", "desc": "Synthèse des analyses effectuées, résultats structurés, tableaux, visualisations et export PDF/Markdown."},
            ]

        pages = state.get("qualification", {}).get("pages", [])
        screens: List[Dict[str, str]] = []
        for idx, pg in enumerate(pages[:6], start=1):
            screens.append({
                "id": f"Écran {idx:02d}",
                "name": pg.get("name", f"Page {idx}"),
                "desc": ", ".join(pg.get("content", ["Interface métier structurée"])),
            })
        while len(screens) < 6:
            idx = len(screens) + 1
            defaults = [
                ("Console Pilote IA", "Chat Panel ACP / Google ADK / OpenAI ChatKit intégré avec cartes d'outils structurées."),
                ("Paramètres & Design System", "Configuration des préférences, thèmes Stitch et connecteurs API."),
                ("Rapports & Exports", "Synthèse structurée, tableaux comparatifs et export PDF / Word / Markdown."),
            ]
            name, desc = defaults[(idx - 1) % len(defaults)]
            screens.append({"id": f"Écran {idx:02d}", "name": name, "desc": desc})
        return screens

    def generate_phase1_design_prompt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Génère le Prompt Maître Phase 1 (Planche 6 Écrans 2x3) pour l'agent générateur d'images."""
        session_id = params.get("session_id", "ui-sess-default")
        sf, state = self._load_state(session_id)
        project_name = params.get("project_name") or state.get("project_name", "SnorbikProduct")
        vision = params.get("vision_brief") or state.get("vision_brief", "Plateforme SaaS professionnelle avec assistant IA.")
        screens = self._build_6_screens(state, params)
        arch_id = state.get("qualification", {}).get("archetype_id", "ai_agent_console")
        preset = self.bank_repo.get_stitch_preset(arch_id, vision)
        colors = preset.get("colors", {})

        screens_block = "\n".join(f"- **{s['id']} — {s['name']}** : {s['desc']}" for s in screens)
        prompt_text = f"""# PHASE 1 — AI VISUAL DESIGN EXPLORATION ({project_name})

## 1. TON RÔLE
Agis comme une équipe composée de : Senior SaaS Product Designer, Senior UI/UX Designer, Interface Architect et Art Director spécialisé dans les logiciels professionnels.
Il ne s'agit pas de créer une affiche publicitaire ou un mockup d'ordinateur : conçois directement l'interface graphique d'un véritable produit logiciel cohérent.

## 2. PRÉSENTATION DU PRODUIT
- **Nom :** {project_name}
- **Concept & Vision :** {vision}

## 3. LES 6 ÉCRANS À REPRÉSENTER (Grille 2 rangées × 3 colonnes)
{screens_block}

## 4. DIRECTION ARTISTIQUE (Design System)
- **Thème :** {preset.get('label', 'SaaS Professionnel Moderne')}
- **Fond principal :** `{colors.get('surface_canvas', '#090E1A')}` | **Primaire :** `{colors.get('color_primary', '#10B981')}` | **Secondaire :** `{colors.get('color_secondary', '#06B6D4')}`
- **Règles :** Navigation latérale structurée, hiérarchie claire, espacement régulier, zéro carte décorative inutile, zéro conclusion métier inventée.

## 5. ORGANISATION & LIVRABLE DE PHASE 1
- Produire **1 planche haute résolution en format paysage (16:9)** présentant les **6 écrans distincts en grille 2×3**.
- Chaque écran doit être entièrement visible, lisible et appartenir au même Design System.
- **INTERDICTION :** Ne pas générer de vidéo à cette étape. **ATTENDRE LA VALIDATION HUMAINE AVANT LA PHASE 2.**
"""
        out_path = sf.parent / "P1_DESIGN_PROMPT.md"
        _safe_path(out_path).write_text(prompt_text, encoding="utf-8")

        res = {
            "session_id": session_id,
            "phase": "PHASE_1_AI_VISUAL_DESIGN",
            "deliverable_type": "Visual Design Board (Grille 2x3 — 6 Écrans)",
            "screens_count": len(screens),
            "screens": screens,
            "prompt_file_path": str(out_path),
            "ready_prompt_for_image_generator": prompt_text,
            "next_human_gate": "Faire générer la planche par image-generator, valider les écrans retenus, puis appeler ui_designer_generate_phase2_video_prompt.",
        }
        state["phase1_visual_design"] = {"prompt_file_path": str(out_path), "screens": screens}
        sf.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        return res

    def generate_phase2_video_prompt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Génère le Prompt Storyboard Vidéo 12s (Phase 2) après validation de la planche Phase 1."""
        session_id = params.get("session_id", "ui-sess-default")
        sf, state = self._load_state(session_id)
        project_name = params.get("project_name") or state.get("project_name", "SnorbikProduct")
        screens = state.get("phase1_visual_design", {}).get("screens") or self._build_6_screens(state, params)
        duration_sec = int(params.get("duration_seconds", 12))
        step_sec = max(duration_sec // max(len(screens), 1), 2)

        storyboard_rows = []
        for idx, s in enumerate(screens):
            t0, t1 = idx * step_sec, (idx + 1) * step_sec
            storyboard_rows.append(f"- **{t0:02d}–{t1:02d} s** : {s['id']} — {s['name']} ({s['desc']})")

        video_prompt = f"""# PHASE 2 — AI VIDEO PROTOTYPING STORYBOARD ({project_name} — {duration_sec}s)

## OBJECTIVE
Act as a senior SaaS product designer and UI/UX motion architect.
Animate ONLY the validated UI screens from Phase 1 into a cohesive {duration_sec}-second widescreen (16:9) product walkthrough video.
Do NOT invent new layouts or marketing fluff: show the software interfaces directly with smooth transitions.

## VISUAL STORYBOARD ({duration_sec} SECONDS)
{chr(10).join(storyboard_rows)}

## SCREEN EXTRACTION & NEXT STEP
- Extract key frames at {', '.join(f'{(i+1)*step_sec - 1}s' for i in range(len(screens)))} as reference mockups.
- Feed validated screens into `ui_designer_init_session(mockup_image_path=...)` to reconstruct reusable React components (`N1->N5` + Bank).
"""
        out_path = sf.parent / "P2_VIDEO_PROMPT.md"
        _safe_path(out_path).write_text(video_prompt, encoding="utf-8")

        return {
            "session_id": session_id,
            "phase": "PHASE_2_AI_VIDEO_PROTOTYPING",
            "deliverable_type": f"Video Prototype Storyboard ({duration_sec}s)",
            "storyboard_slots": len(screens),
            "prompt_file_path": str(out_path),
            "ready_prompt_for_video_generator": video_prompt,
            "next_step": "Extraire les écrans validés et lancer la reconstruction React N1->N5 via ui_designer_decompose_n1_to_n5 & ui_designer_hunt_parts_3_circles.",
        }
