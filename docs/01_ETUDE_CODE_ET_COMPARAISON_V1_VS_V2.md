# 🔬 ÉTUDE DU CODE SOURCE (V1.0) vs SYSTÈME ATTENDU (V2.0) — MCP #30 UI Designer & Frontend SDK

> **Document d'Ingénierie & Boucle de Validation**  
> **Objet :** Audit ligne par ligne du code source initial (`V1.0`), cartographie des dépendances, comparaison entre l'Infographie 1 (*État Réel V1.0*) et l'Infographie 2 (*Projet Attendu V2.0*), et plan d'implémentation corrective vers la `V2.0`.

---

## 1. Étude du Code Source Initial (`V1.0`) & Concept du MCP Pattern (4 Piliers)

### 1.1. Les 4 Piliers du MCP Pattern dans `30_ui_designer_frontend_sdk_mcp`
1. **Pilier 1 — Porte MCP JSON-RPC 2.0 (`canal_mcp/`)** :
   - `mcp_server.py` (83 lignes) et `tools_metadata.py` (193 lignes).
   - Expose les outils au format Quinti-Bloc Bipartite (`INV-07`) pour que n'importe quel Agent IA (Google ADK, Cursor, Antigravity, Claude) connaisse l'ordre d'appel sans prompt complexe.
2. **Pilier 2 — Porte SDK Python In-Process `< 2ms` (`canal_sdk_cli/sdk.py`)** :
   - `UiDesignerFrontendSdkMcpSdk` (114 lignes) : appelable directement en Python par un orchestrateur ou un backend FastAPI sans surcharge réseau.
3. **Pilier 3 — Porte CLI, Extensions & Tablette IA (`canal_sdk_cli/cli.py` + `mcp_agent_coding/` + `skills/`)** :
   - `cli.py` (37 lignes), `context_llm.json` (Tablette 7 Sections), `golden_output_scelle.json` et les **5 Skills ADN** (`01-frontend-puzzle-sdk-architecture`, `02-backend-ddd-agent-bridge`, `03-mcp-hybrid-tri-canal-standard`, `04-ui-fabrication-session-workflow`, `05-snorbik-infographic-designer`).
4. **Pilier 4 — La Banque de Matières Premières (`bank/`) & Le SDK UI Généré (`src/sdk/`)** :
   - `01_external_ui_mcp_servers.json` (`shadcn@latest mcp`, `@magicui/mcp`, `@21st-dev/magic`).
   - `02_ai_chat_panels_and_protocols.json` (`OpenAI ChatKit`, `assistant-ui`, `DesktopPilotPanel`, protocoles `ACP`, `Google ADK`, `AG-UI`).
   - `03_react_components_n1_to_n5_catalog.json` + `bank/templates/`.

### 1.2. Cartographie des Dépendances par Outil dans le Code Source
| Outil MCP | Module Python Exécuté | Dépendances & Fichiers Lus / Écrits |
| :--- | :--- | :--- |
| `ui_designer_frontend_sdk_mcp_ping` | `mcp_server.py` / `sdk.py` | Aucune (Sonde mémoire vive `< 1ms`) |
| `ui_designer_frontend_sdk_mcp_get_pipelines` | `sdk.py` (`RECOMMENDED_PIPELINES`) | Retourne les pipelines séquentielles conseillées |
| `ui_designer_init_session` | `MaterializerEngine.init_session` | Dépend de `BankRepository.load_architecture_skills()` ➔ Écrit `session_state.json` |
| `ui_designer_analyze_mockup` *(Nouveau V2.0)* | `MaterializerEngine.analyze_mockup` | Analyse `mockup_image_path` + `vision_brief` ➔ Extrait `design_tokens` & `layout_zones` dans `session_state.json` |
| `ui_designer_load_architecture_skills` | `BankRepository.load_architecture_skills` | Lit `skills/01..05/SKILL.md` |
| `ui_designer_list_bank_inventory` | `BankRepository.get_full_bank_inventory` | Lit `bank/01_*.json`, `02_*.json`, `03_*.json` |
| `ui_designer_search_bank` | `BankRepository.search_bank` | Filtre les 3 fichiers JSON de `bank/` selon la vision et les tags |
| `ui_designer_generate_materialization_doc` | `MaterializerEngine.generate_materialization_doc` | Lit `session_state.json` + `BankRepository.search_bank` ➔ Écrit `MATERIALIZATION_BLUEPRINT.md` & `materialization_plan.json` |
| `ui_designer_materialize_frontend_sdk` | `SdkBuilderAndAuditor.materialize_frontend_sdk` | Lit `materialization_plan.json` + `bank/templates/*` ➔ Génère `src/presentation/01..05`, `src/sdk/acp`, `src/sdk/google-adk`, `package.json`, `components.json` + **composants sur-mesure `CUSTOM_AI_TO_BUILD`** |
| `ui_designer_generate_backend_bridge` *(Nouveau V2.0)* | `BackendBridgeGenerator.generate_bridge` | Génère le pont Backend FastAPI DDD (`acp_router.py`, `adk_router.py`, `chatkit_router.py`) pour brancher le SDK Frontend |
| `ui_designer_audit_architecture` | `SdkBuilderAndAuditor.audit_architecture` | Scanne l'arborescence générée : vérifie les 5 niveaux DPN-IA, le plafond `< 350L`, la présence des `use*Controller.ts`, `index.ts`, `package.json` et `components.json` |
| `ui_designer_frontend_sdk_mcp_run` | `ExecuteActionUseCase` ➔ `ConcreteOperationalAdapter` | Routeur polymorphe universel One-Shot |

---

## 2. Comparaison : Infographie 1 (Code Réel V1.0) vs Infographie 2 (Projet Attendu V2.0)

| Dimension Technique | État Réel Initial (`V1.0` — Infographie 1) | Résultat Attendu Cible (`V2.0` — Infographie 2) | Écart / Action Corrective (`V1 ➔ V2`) |
| :--- | :--- | :--- | :--- |
| **1. Analyse de la Maquette (`mockup_image_path`)** | Stockait uniquement le chemin string sans extraire ni layout ni tokens. | Outil dédié `ui_designer_analyze_mockup` extrayant le profil de layout (`WORKBENCH_3_COLS`, `ECOMMERCE_SPLIT`, `SAAS_DASHBOARD`), la palette et les zones UI. | **Implémenter `analyze_mockup` dans `MaterializerEngine`**. |
| **2. Matérialisation des Composants Sur-Mesure (`CUSTOM_AI_TO_BUILD`)** | `materialize_frontend_sdk` générait uniquement 15 fichiers statiques et ignorait les composants `CUSTOM_AI_TO_BUILD` du plan. | Lit dynamiquement `materialization_plan.json` et génère pour chaque brique `CUSTOM_AI_TO_BUILD` son dossier `02-features/<Feature>/`, son `use<Feature>Controller.ts`, son `partials/` et son `index.ts`. | **Rendre `SdkBuilderAndAuditor` 100 % dynamique sur `materialization_plan.json`**. |
| **3. Manifestes NPM & Registres MCP UI (`shadcn` / `ChatKit`)** | Aucun `package.json` ni `components.json` généré dans le SDK. | Génère `package.json` (`@openai/chatkit-react`, `@assistant-ui/react`, `@ag-ui/client`) et `components.json` préconfiguré vers `src/presentation/01-primitives` et `02-features`. | **Générer `package.json` + `components.json` dans `SdkBuilderAndAuditor`**. |
| **4. Pont Backend FastAPI (`ACP` + `Google ADK` + `ChatKit`)** | Documenté dans le Skill 02 mais non généré par le MCP. | Outil `ui_designer_generate_backend_bridge` générant `backend_bridge/acp_router.py`, `adk_router.py` et `chatkit_router.py` (< 150L chacun). | **Créer `core/infrastructure/backend_bridge_generator.py`**. |
| **5. Audit Architectural & Auto-Validation** | Vérifiait uniquement les 5 dossiers et `< 350L`. | Vérifie aussi que chaque feature N2 possède son `use*Controller.ts` et son `index.ts`, que `package.json` et `components.json` sont présents, et que tous les items du `materialization_plan.json` sont matérialisés. | **Enrichir `audit_architecture` avec contrôle de complétude du plan**. |
| **6. Pipelines Séquentielles Conseillées (`INV-07`)** | 3 pipelines (7 étapes max). | **4 Pipelines complètes** incluant le Pipeline E2E 9 étapes (Vision + Maquette ➔ Analyse Maquette ➔ Skills ➔ Fouille Banque ➔ Document de Matérialisation ➔ SDK Frontend Dynamique ➔ Pont Backend ACP/ADK ➔ Audit Certifié). | **Mettre à jour `sdk.py` et `tools_metadata.py` (12 outils)**. |
