---
name: backend-ddd-agent-bridge
description: Architecture Backend Clean DDD 4 Couches (Domain, Application, Infrastructure, Interfaces FastAPI), Contrats Pydantic V2, et Ponts Protocolaires IA (ACP, Google ADK, AG-UI, MCP).
---

# 🧬 SKILL ADN 02 : BACKEND DDD & AGENT BRIDGE ARCHITECTURE

> **Classification :** Standard Architectural Backend & Passerelle Agentique Snorbik AI
> **Mission :** Garantir une architecture Backend Clean DDD à 4 couches (`Domain ➔ Application ➔ Infrastructure ➔ Interfaces`) avec contrats Pydantic V2 stricts et exposer des passerelles standardisées pour les interfaces graphiques (**ACP**, **Google ADK**, **AG-UI**, **OpenAI ChatKit Session Endpoint**).

---

## 1. Invariants Absolus de la Clean Architecture Backend (4 Couches)

```text
backend/
├── domain/                   # Couche 1 : Entités pures, Value Objects, Ports abstraits (Zéro dépendance externe)
├── application/              # Couche 2 : Use Cases métier, Orchestrateurs de session
├── infrastructure/           # Couche 3 : Adaptateurs SQLite/PostgreSQL, Clients MCP SDK, Bridges Google ADK / ACP
├── interfaces/               # Couche 4 : Routes FastAPI REST & SSE (Validation Pydantic V2 stricte)
│   ├── api_v1/
│   ├── acp_router.py         # Endpoint standard Agent Communication Protocol (/acp/v1/runs)
│   ├── adk_router.py         # Endpoint compatible Google ADK (/adk/v1/run_sse)
│   └── chatkit_router.py     # Endpoint de session pour OpenAI ChatKit / assistant-ui
└── tests/                    # Preuve L4 pytest
```

### Règles d'Or (Vaccins) :
- **INV-01 (Pureté du Domaine) :** Aucun import FastAPI, SQLAlchemy ou HTTP dans `domain/`.
- **INV-02 (Contrats Pydantic Stricts) :** Toute route FastAPI et tout événement SSE (ACP / ADK / AG-UI) utilise un `InputDTO` et un `OutputDTO` Pydantic V2 typés.
- **INV-03 (Budget de Lignes < 350L) :** Aucun fichier Python ne dépasse 350 lignes (cible 60–240 lignes).
- **INV-04 (Connexion In-Process aux MCP) :** Le backend consomme les outils MCP locaux via leur **Porte 3 (`canal_sdk_cli/sdk.py`)** en latence `< 2ms` sans surcharge réseau.

---

## 2. Standard d'Interopérabilité Backend ➔ Frontend SDK

Pour que n'importe quel composant de Chat Panel de la Banque (`OpenAI ChatKit`, `assistant-ui`, `DesktopPilotPanel`) puisse se brancher en 1 minute sans code glue complexe, le Backend expose 3 adaptateurs standardisés :

1. **Passerelle ACP (`Agent Communication Protocol` — `/api/acp/runs`)** :
   - Reçoit `{ agent_name, session_id, input_messages, context }`.
   - Émet un flux SSE standardisé : `agent.thought`, `tool.call.started`, `tool.call.completed` (avec payload JSON structuré pour affichage de cartes UI), et `message.completed`.
2. **Passerelle Google ADK (`/api/adk/run_sse`)** :
   - Permet d'exécuter un agent `google.adk.agents.LlmAgent` ou `SequentialAgent` équipé de nos outils MCP et de streamer directement les événements vers le composant React `GoogleAdkProvider`.
3. **Passerelle ChatKit / Assistant-UI (`/api/chat/stream`)** :
   - Compatible avec le format Data Stream de `@openai/chatkit-react` et `@assistant-ui/react`, permettant d'afficher automatiquement des widgets React riches (tableaux, cartes 3D, aperçus de devis, rapports médicaux) dès qu'un outil MCP retourne un JSON structuré.
