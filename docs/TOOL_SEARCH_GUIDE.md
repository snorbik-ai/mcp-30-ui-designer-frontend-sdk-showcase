# Guide Tool Search & Micro-Prompts (`INV-20`) — `30_ui_designer_frontend_sdk_mcp`

> **Serveur MCP :** `30-ui-designer-frontend-sdk-mcp` (`outils_internes/30_ui_designer_frontend_sdk_mcp/`)  
> **Passerelle de Découverte :** `MCP #36` (`36_tool_search_codemode_mcp`)  
> **Manifeste Machine :** `canal_mcp/tool_search_manifest.json`  
> **Inventaire :** `10` outil(s) (`10` publics, `0` protégés auth)

---

## 1. Index Tool Search & Micro-Prompts Bi-Phases

| Outil (`tool_name`) | Sécurité | Chargement | Micro-Prompt Appel (Agent 1 Planner) | Micro-Prompt Restitution (Agent 2 Responder) |
| :--- | :---: | :---: | :--- | :--- |
| `ui_designer_frontend_sdk_mcp_get_pipelines` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_frontend_sdk_mcp_get_pipelines en 2 phrases  |
| `ui_designer_init_session` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_init_session en 2 phrases claires max par pa |
| `ui_designer_qualify_and_plan_pages` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_qualify_and_plan_pages en 2 phrases claires  |
| `ui_designer_extract_design_system` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_extract_design_system en 2 phrases claires m |
| `ui_designer_decompose_n1_to_n5` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_decompose_n1_to_n5 en 2 phrases claires max  |
| `ui_designer_hunt_parts_3_circles` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_hunt_parts_3_circles en 2 phrases claires ma |
| `ui_designer_generate_materialization_doc` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_generate_materialization_doc en 2 phrases cl |
| `ui_designer_materialize_frontend_sdk` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_materialize_frontend_sdk en 2 phrases claire |
| `ui_designer_generate_backend_bridge` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_generate_backend_bridge en 2 phrases claires |
| `ui_designer_audit_architecture` | `PUBLIC` | `deferred` | [USINE MONTAGE UI REACT N1-N5 & SDK AGENTS IA V3.0] Qualification pages/séquences, Design  | Synthétiser le digest renvoyé par ui_designer_audit_architecture en 2 phrases claires max  |

---

## 2. Consommation dans les 2 Environnements (`INV-20`)

1. **Mode Desktop (Claude Desktop, Cursor, Antigravity) :**  
   Au lieu de charger tous les schémas de la flotte, l'agent interroge la passerelle **`MCP #36`** :
   - `tool_search_discover(query="30_ui_designer_frontend_sdk_mcp", server_filter="30-ui-designer-frontend-sdk-mcp")`
   - `tool_search_inspect_workflow(tool_name="...")`
   - `tool_search_invoke_mcp_tool(server_id="30-ui-designer-frontend-sdk-mcp", tool_name="...", arguments={})`
2. **Mode Serveur de Production (Architecture V11) :**  
   - **Avant Contexte 1 :** Vérification cryptographique du passeport (`MCP #33` / Cookie `HttpOnly`).
   - **Agent 1 (Planificateur) :** Ne reçoit que cet index compact + `planner_micro_prompt` (économie > 85 % de tokens).
   - **Exécuteur Parallèle (0 token) :** Vérifie `requires_auth` de façon déterministe (Zero-Trust OWASP), exécute les outils en parallèle (`asyncio.gather`) et injecte `responder_micro_prompt` dans le **Pré-Contexte 2**.
   - **Agent 2 (Répondeur) :** Tourne avec `tools=[]` et un contrat `output_schema` JSON strict.
