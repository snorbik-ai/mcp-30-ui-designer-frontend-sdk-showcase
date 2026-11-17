"""Métadonnées des 18 Outils MCP V3.0 — Standard Quinti-Bloc Bipartite INV-07 & INV-08 pour MCP #30."""
from __future__ import annotations

from typing import List, Dict, Any


def _tool(name: str, role: str, trigger: str, op: str, out: str, p1: str, p2: str, props: Dict[str, Any] | None = None, req: List[str] | None = None) -> Dict[str, Any]:
    schema: Dict[str, Any] = {"type": "object", "properties": props or {}}
    if req:
        schema["required"] = req
    return {
        "name": name,
        "description": (
            f"[{role}]\n"
            f"DÉCLENCHEUR CONSEILLÉ : {trigger}\n"
            f"OPÉRATION : {op}\n"
            f"SORTIE : {out}\n"
            "PIPELINES SÉQUENTIELLES CONSEILLÉES :\n"
            f"• PARTIE 1 — INTENTION & CONTEXTE MÉTIER DU PIPELINE : {p1}\n"
            f"• PARTIE 2 — SÉQUENCE ORDONNÉE PAR NOMS D'OUTILS EXACTS :\n  {p2}"
        ),
        "inputSchema": schema,
    }


TOOLS_METADATA: List[Dict[str, Any]] = [
    _tool(
        "ui_designer_frontend_sdk_mcp_ping", "SONDE DE SANTÉ SOUVERAINE V3.0",
        "Vérification initiale de disponibilité du serveur MCP #30.",
        "Contrôle instantané en mémoire vive.", "Statut HEALTHY et version 3.0.0.",
        "Vérifier l'état du MCP Designer avant d'ouvrir une session.",
        "1. [CET OUTIL : ui_designer_frontend_sdk_mcp_ping] -> 2. ui_designer_frontend_sdk_mcp_get_pipelines",
    ),
    _tool(
        "ui_designer_frontend_sdk_mcp_get_pipelines", "BOUSSOLE CHAÎNE DE MONTAGE VOITURE UI V3.0",
        "Au démarrage de toute conception de site web, e-commerce, hôtel, SaaS ou SDK Frontend.",
        "Restitue l'ordre exact de travail (11 étapes) sans prompt complexe.", "Catalogue des 4 pipelines.",
        "Guider l'IA pas-à-pas : Qualification & Séquences -> Design System Stitch -> Décomposition N1-N5 -> Chasse 3 Cercles -> Montage SDK.",
        "1. [CET OUTIL : ui_designer_frontend_sdk_mcp_get_pipelines] -> 2. ui_designer_init_session -> 3. ui_designer_qualify_and_plan_pages -> 4. ui_designer_extract_design_system -> 5. ui_designer_load_architecture_skills -> 6. ui_designer_decompose_n1_to_n5 -> 7. ui_designer_hunt_parts_3_circles -> 8. ui_designer_generate_materialization_doc -> 9. ui_designer_materialize_frontend_sdk -> 10. ui_designer_generate_backend_bridge -> 11. ui_designer_audit_architecture",
    ),
    _tool(
        "ui_designer_init_session", "INITIALISATION DE SESSION (VISION & MAQUETTE)",
        "Dès que l'utilisateur fournit une idée de site/application ou une image de maquette.",
        "Crée la session, enregistre la vision/maquette et active ACP, Google ADK, OpenAI ChatKit, assistant-ui.", "État de session initialisé.",
        "Pipeline 1 (Chaîne de Montage Voiture UI V3.0).",
        "1. ui_designer_frontend_sdk_mcp_get_pipelines -> 2. [CET OUTIL : ui_designer_init_session] -> 3. ui_designer_qualify_and_plan_pages",
        {"session_id": {"type": "string"}, "project_name": {"type": "string"}, "vision_brief": {"type": "string"}, "mockup_image_path": {"type": "string"}, "agent_protocols": {"type": "array", "items": {"type": "string"}}, "custom_features": {"type": "array", "items": {"type": "string"}}},
        ["project_name", "vision_brief"],
    ),
    _tool(
        "ui_designer_qualify_and_plan_pages", "ÉTAPE 1 : QUALIFICATION TYPE DE SITE, CAHIER DES CHARGES PAGES & SÉQUENCES",
        "Juste après init_session pour clarifier le type de site (e-commerce simple/complexe, hôtel, SaaS, console IA) et ses pages.",
        "Détermine l'archétype, génère la liste des pages, leur contenu et leur diagramme de séquence utilisateur.", "PAGES_AND_SEQUENCES_SPEC.md.",
        "Éviter de coder à l'aveugle : fixer toutes les pages et séquences avant de chercher des pièces.",
        "1. ui_designer_init_session -> 2. [CET OUTIL : ui_designer_qualify_and_plan_pages] -> 3. ui_designer_extract_design_system",
        {"session_id": {"type": "string"}, "project_type": {"type": "string"}, "vision_brief": {"type": "string"}}, ["session_id"],
    ),
    _tool(
        "ui_designer_extract_design_system", "ÉTAPE 2 : DESIGN SYSTEM STITCH (POLICES, FOND, PALETTE, TOKENS CSS)",
        "Après la qualification des pages pour extraire les couleurs, polices et styles à appliquer aux pièces.",
        "Génère DESIGN_SYSTEM_STITCH.md et tokens.css à partir des presets Stitch et de la maquette.", "tokens.css & DESIGN_SYSTEM_STITCH.md.",
        "Préparer le thème visuel pour adapter chaque pièce détachée de la Banque.",
        "1. ui_designer_qualify_and_plan_pages -> 2. [CET OUTIL : ui_designer_extract_design_system] -> 3. ui_designer_load_architecture_skills",
        {"session_id": {"type": "string"}}, ["session_id"],
    ),
    _tool(
        "ui_designer_analyze_mockup", "ANALYSE COMPLÉMENTAIRE DE LA MAQUETTE IMAGE",
        "Optionnel : pour extraire les zones d'écran à partir du chemin d'une maquette image.",
        "Identifie l'archétype de layout (3 colonnes, Split E-Commerce, SaaS) et les zones UI.", "Mapping DPN-IA N1->N5.",
        "Compléter le cahier des charges des pages par l'analyse visuelle de la maquette.",
        "1. ui_designer_init_session -> 2. [CET OUTIL : ui_designer_analyze_mockup] -> 3. ui_designer_decompose_n1_to_n5",
        {"session_id": {"type": "string"}, "mockup_image_path": {"type": "string"}, "vision_brief": {"type": "string"}}, ["session_id"],
    ),
    _tool(
        "ui_designer_load_architecture_skills", "ÉTAPE 3 : CHARGEMENT DES 5 SKILLS D'ARCHITECTURE",
        "Avant de décomposer et chercher des pièces pour imposer notre architecture Puzzle N1-N5 (<350L).",
        "Charge les 5 Skills ADN (Frontend N1-N5, Backend DDD, MCP Tri-Canal, Session Workflow, Infographie).", "Règles architecturales actives.",
        "Verrouiller les règles du Puzzle 5 Niveaux avant la chasse aux pièces.",
        "1. ui_designer_extract_design_system -> 2. [CET OUTIL : ui_designer_load_architecture_skills] -> 3. ui_designer_decompose_n1_to_n5",
    ),
    _tool(
        "ui_designer_decompose_n1_to_n5", "ÉTAPE 4 : DÉCOMPOSITION ATOMIQUE EN 5 NIVEAUX (N1 ➔ N5)",
        "Une fois les pages et séquences fixées, pour lister toutes les pièces nécessaires de N1 à N5.",
        "Agrège toutes les pièces requises classées par niveau (01-primitives à 05-pages).", "Liste structurée des pièces requises.",
        "Dresser la liste exacte des pièces détachées à commander au magasin avant de coder.",
        "1. ui_designer_load_architecture_skills -> 2. [CET OUTIL : ui_designer_decompose_n1_to_n5] -> 3. ui_designer_hunt_parts_3_circles",
        {"session_id": {"type": "string"}, "custom_features": {"type": "array", "items": {"type": "string"}}}, ["session_id"],
    ),
    _tool(
        "ui_designer_hunt_parts_3_circles", "ÉTAPE 5 : CHASSE AUX PIÈCES EN 3 CERCLES (INTERNE ➔ MCP GRATUITS ➔ DERNIER RECOURS)",
        "Après la décomposition N1->N5 pour trouver chaque pièce déjà prête sans réinventer la roue.",
        "Cherche dans : Cercle 1 (200+ composants BatiHome), Cercle 2 (shadcn/Magic UI/21st.dev/ChatKit), Cercle 3 (Dernier recours IA).", "Taux de pièces prêtes (%) & provenance.",
        "Principe Montage Voiture : ne fabriquer sur-mesure qu'en tout dernier recours.",
        "1. ui_designer_decompose_n1_to_n5 -> 2. [CET OUTIL : ui_designer_hunt_parts_3_circles] -> 3. ui_designer_generate_materialization_doc",
        {"session_id": {"type": "string"}}, ["session_id"],
    ),
    _tool(
        "ui_designer_list_bank_inventory", "INVENTAIRE DU MAGASIN DE PIÈCES (BANQUE 200+)",
        "Pour consulter tous les composants internes indexés, serveurs MCP UI externes et Chat Panels IA.",
        "Lit les 6 registres de la Banque (200+ composants BatiHome, shadcn, Magic UI, 21st.dev, ChatKit, assistant-ui, ACP, ADK).", "Compteurs et inventaire complet.",
        "Pipeline 2 (Chasse Rapide aux Pièces Détachées).",
        "1. [CET OUTIL : ui_designer_list_bank_inventory] -> 2. ui_designer_decompose_n1_to_n5 -> 3. ui_designer_hunt_parts_3_circles",
    ),
    _tool(
        "ui_designer_search_bank", "RECHERCHE CIBLÉE DANS LA BANQUE",
        "Pour rechercher des composants spécifiques par mots-clés ou tags.",
        "Filtre les composants N1->N5, Chat Panels et connecteurs ACP/Google ADK.", "Composants correspondants.",
        "Recherche ponctuelle dans le magasin de pièces.",
        "1. ui_designer_list_bank_inventory -> 2. [CET OUTIL : ui_designer_search_bank] -> 3. ui_designer_generate_materialization_doc",
        {"query": {"type": "string"}, "required_features": {"type": "array", "items": {"type": "string"}}, "protocols": {"type": "array", "items": {"type": "string"}}},
    ),
    _tool(
        "ui_designer_generate_materialization_doc", "ÉTAPE 6 : DOCUMENT DE MATÉRIALISATION & PLAN DE MONTAGE",
        "Après la chasse aux pièces en 3 cercles, avant de générer les fichiers.",
        "Produit MATERIALIZATION_BLUEPRINT.md et materialization_plan.json.", "Plan de montage chiffré et taux de réutilisation.",
        "Valider le plan d'assemblage complet avant la génération physique.",
        "1. ui_designer_hunt_parts_3_circles -> 2. [CET OUTIL : ui_designer_generate_materialization_doc] -> 3. ui_designer_materialize_frontend_sdk",
        {"session_id": {"type": "string"}, "project_name": {"type": "string"}, "vision_brief": {"type": "string"}, "custom_features": {"type": "array", "items": {"type": "string"}}}, ["session_id"],
    ),
    _tool(
        "ui_designer_materialize_frontend_sdk", "ÉTAPE 7 : ASSEMBLAGE DU SDK FRONTEND + TOKENS STITCH + ACP/ADK",
        "Après validation du Document de Matérialisation.",
        "Génère package.json, components.json, src/styles/tokens.css, les 5 niveaux N1->N5, src/sdk/acp & google-adk, et le delta sur-mesure.", "Arborescence SDK prête à lancer.",
        "Monter l'interface graphique complète avec ses pièces configurées.",
        "1. ui_designer_generate_materialization_doc -> 2. [CET OUTIL : ui_designer_materialize_frontend_sdk] -> 3. ui_designer_generate_backend_bridge -> 4. ui_designer_audit_architecture",
        {"session_id": {"type": "string"}, "target_dir": {"type": "string"}}, ["session_id"],
    ),
    _tool(
        "ui_designer_generate_backend_bridge", "ÉTAPE 8 : PONT BACKEND FASTAPI (ACP · GOOGLE ADK · CHATKIT)",
        "Après matérialisation du SDK Frontend pour exposer les routes serveur correspondantes.",
        "Génère interfaces/acp_router.py, adk_router.py et chatkit_router.py.", "Routeurs FastAPI Pydantic V2 prêts.",
        "Connecter le Chat Panel React au backend Python / Google ADK.",
        "1. ui_designer_materialize_frontend_sdk -> 2. [CET OUTIL : ui_designer_generate_backend_bridge] -> 3. ui_designer_audit_architecture",
        {"session_id": {"type": "string"}, "target_dir": {"type": "string"}}, ["session_id"],
    ),
    _tool(
        "ui_designer_audit_architecture", "ÉTAPE 9 : AUDIT DE CONFORMITÉ L4 (N1-N5, HOOKS, <350L)",
        "En fin de montage pour certifier que le SDK généré respecte 100% de notre architecture.",
        "Vérifie 5 niveaux DPN-IA, package.json/components.json, use*Controller.ts + index.ts, et <350L.", "Certificat de conformité L4.",
        "Clôturer la chaîne de montage avec preuve de qualité.",
        "1. ui_designer_generate_backend_bridge -> 2. [CET OUTIL : ui_designer_audit_architecture]",
        {"session_id": {"type": "string"}, "target_dir": {"type": "string"}},
    ),
    _tool(
        "ui_designer_generate_phase1_design_prompt", "ZÉRO MAQUETTE — PHASE 1 : PROMPT PLANCHE VISUELLE (6 ÉCRANS 2x3)",
        "Quand l'utilisateur n'a AUCUNE maquette et veut explorer des propositions UI/UX avant de développer ou d'animer.",
        "Génère PHASE1_VISUAL_DESIGN_PROMPT.md pour que l'IA génératrice d'images produise 1 planche 16:9 (6 écrans en grille 2x3).", "Prompt prêt à exécuter + liste des 6 écrans.",
        "Pipeline 0 (AI Visual Prototyping : Concevoir -> Valider -> Animer).",
        "1. ui_designer_qualify_and_plan_pages -> 2. [CET OUTIL : ui_designer_generate_phase1_design_prompt] -> 3. (Validation humaine) -> 4. ui_designer_generate_phase2_video_prompt",
        {"session_id": {"type": "string"}, "project_name": {"type": "string"}, "vision_brief": {"type": "string"}}, ["session_id"],
    ),
    _tool(
        "ui_designer_generate_phase2_video_prompt", "ZÉRO MAQUETTE — PHASE 2 : PROMPT STORYBOARD VIDÉO 12s (AI VIDEO PROTOTYPING)",
        "Après validation humaine de la planche Phase 1 pour animer les 6 écrans retenus en vidéo 10-15s et extraire des frames.",
        "Génère PHASE2_VIDEO_STORYBOARD_PROMPT.md découpé en tranches de 2 secondes (00-02s à 10-12s).", "Prompt Storyboard Vidéo prêt à exécuter.",
        "Pipeline 0 (Phase 2 : Animer uniquement les écrans validés puis reconstruire en React N1->N5).",
        "1. ui_designer_generate_phase1_design_prompt -> 2. [CET OUTIL : ui_designer_generate_phase2_video_prompt] -> 3. ui_designer_extract_design_system -> 4. ui_designer_decompose_n1_to_n5",
        {"session_id": {"type": "string"}, "duration_seconds": {"type": "integer", "default": 12}}, ["session_id"],
    ),
    _tool(
        "ui_designer_frontend_sdk_mcp_run", "EXÉCUTEUR POLYMORPHE DIRECT ONE-SHOT",
        "Pour exécuter n'importe quelle action du MCP #30 en appel direct.",
        "Route l'action vers le cas d'usage Clean Architecture correspondant.", "Digest opérationnel structuré.",
        "Pipeline 4 (Exécution Directe One-Shot).",
        "1. ui_designer_frontend_sdk_mcp_get_pipelines -> 2. [CET OUTIL : ui_designer_frontend_sdk_mcp_run]",
        {"action": {"type": "string", "default": "execute"}, "parameters": {"type": "object", "default": {}}},
    ),
]
