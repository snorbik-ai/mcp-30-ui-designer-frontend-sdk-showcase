---
name: ui-fabrication-session-workflow
description: Protocole de Session de Fabrication d'Interface Graphique & Site Web Frontend piloté par le MCP UI Designer (#30) : Vision/Maquette ➔ Skills Architecture ➔ Fouille Banque ➔ Document de Matérialisation ➔ Assemblage SDK Frontend.
---

# 🧬 SKILL ADN 04 : PROTOCOLE DE SESSION DE FABRICATION UI & FRONTEND SDK

> **Classification :** Protocole Opérationnel du MCP UI Designer & Frontend Builder (`MCP #30`)
> **Mission :** Transformer une idée, un besoin métier ou une maquette image en une interface graphique React/TypeScript complète (avec SDK Chat Panel IA `OpenAI ChatKit` / `assistant-ui` et protocoles `ACP` / `Google ADK`) au sein d'une **Session de Fabrication structurée en 5 étapes**, en maximisant la réutilisation des composants prêts à l'emploi de la **Banque**.

---

## 1. Règle d'Or : « Ne Jamais Coder à l'Aveugle avant le Document de Matérialisation »

Lorsqu'un utilisateur demande de créer ou d'adapter une interface graphique (ou fournit une image de maquette), l'agent IA **ne doit jamais** se précipiter pour écrire des fichiers React improvisés de zéro. Il ouvre une **Session de Fabrication UI** qui suit obligatoirement les **5 Temps Canoniques** ci-dessous.

---

## 2. Les 5 Temps d'une Session de Fabrication UI (`Pipeline E2E MCP #30`)

### Temps 1 — Initialisation de la Session & Analyse de la Vision / Maquette (`ui_designer_init_session`)
- **Entrées :**
  - `project_name` : Nom du projet ou de l'application cible.
  - `vision_brief` : Description de l'idée, du métier et des fonctionnalités attendues.
  - `mockup_image_path` *(optionnel)* : Chemin vers l'image de la maquette ou capture d'écran de référence.
  - `agent_protocols` : Protocoles IA souhaités (`["ACP", "GOOGLE_ADK", "OPENAI_CHATKIT", "ASSISTANT_UI"]`).
- **Action :** Crée le dossier de session `sessions/<session_id>/`, extrait les zones visuelles requises (Shell, Sections, Features interactives, Chat Panel IA, Vues Métier) et verrouille le cadre de travail.

### Temps 2 — Chargement des Skills d'Architecture (`ui_designer_load_architecture_skills`)
- **Action :** Avant de choisir le moindre composant, le moteur charge les 3 Skills d'Architecture :
  1. `01-frontend-puzzle-sdk-architecture` (Puzzle 5 niveaux `N1 ➔ N5`, `< 350L`, `partials/` + `index.ts` + `use[Feature]Controller.ts`).
  2. `02-backend-ddd-agent-bridge` (Passerelles `ACP`, `Google ADK`, `ChatKit SSE`).
  3. `03-mcp-hybrid-tri-canal-standard` (Connexion au SDK MCP `< 2ms`).
- **Résultat :** Définit la grille architecturale exacte dans laquelle les composants devront s'insérer.

### Temps 3 — Fouille dans la Banque de Matières Premières (`ui_designer_search_bank`)
- **Action :** Pour chaque zone identifiée dans la maquette ou la vision, le moteur interroge **La Banque du MCP Designer (`bank/`)** :
  - **Banque Interne Certifiée (`N1 ➔ N5`)** : Composants BatiHome E-Commerce (`Stepper`, `CatalogGrid`, `DevisModal`, `DesktopPilotPanel`) et BioStation Pro (`Workspace3D`, `TelemetryCard`, `ReportEditor`).
  - **Banque Chat Panels & SDK Agents** : `OpenAI ChatKit` (`@openai/chatkit-react`), `assistant-ui` (`@assistant-ui/react`), `CopilotKit AG-UI`, `ACP Client Hook`, `Google ADK Session Hook`.
  - **Banque Serveurs MCP UI Externes** : `shadcn MCP` (`@shadcn/mcp`), `Magic UI MCP` (`@magicui/mcp`), `21st.dev Magic MCP` (`@21st-dev/magic`).

### Temps 4 — Rédaction du Document de Matérialisation (`ui_designer_generate_materialization_doc`)
- **Action :** Une fois la fouille terminée, l'outil génère un **Document de Matérialisation (`MATERIALIZATION_BLUEPRINT.md`)** qui trie explicitement toutes les pièces nécessaires en **3 catégories** :
  1. 🟢 **MATIÈRES PREMIÈRES DÉJÀ EXISTANTES EN BANQUE (70% à 85% du projet)** : Pièces prêtes à l'emploi qu'il suffit de copier et configurer (thème, couleurs, labels).
  2. 🔵 **MATIÈRES PREMIÈRES À RÉCUPÉRER VIA MCP UI EXTERNE (`shadcn` / `Magic UI` / `21st.dev`)** : Commandes exactes d'installation ou d'extraction depuis les registres gratuits.
  3. 🟠 **DELTA SUR-MESURE À FABRIQUER PAR L'IA (15% à 30% restant)** : Uniquement les composants métier spécifiques qui n'existent dans aucune banque, avec leur contrat de props, leur hook contrôleur `use[Feature]Controller.ts` et leur budget de lignes (`< 240L`).

### Temps 5 — Matérialisation du SDK Frontend & Audit de Conformité (`ui_designer_materialize_frontend_sdk` ➔ `ui_designer_audit_architecture`)
- **Action :**
  1. Génère l'arborescence complète (`01-primitives/`, `02-features/`, `03-sections/`, `04-shell/`, `05-pages/`, et `sdk/` avec `acp/`, `google-adk/`, `chat-panels/`) en assemblant les pièces de la Banque et les pièces sur-mesure.
  2. Exécute l'audit automatique (`ui_designer_audit_architecture`) qui vérifie :
     - 100 % des fichiers `< 350 lignes`,
     - Présence de `index.ts` et `use[Feature]Controller.ts` pour chaque feature N2,
     - Présence des connecteurs SDK (`ACP`, `Google ADK`, `ChatKit` / `assistant-ui`).
