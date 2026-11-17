---
name: frontend-puzzle-sdk-architecture
description: Architecture Frontend React/TypeScript en Puzzle 5 Niveaux (N1 ➔ N5), Budget < 350L, Custom Hooks Contrôleurs, pattern partials/ + index.ts, et intégration SDK UI Agents (OpenAI ChatKit, assistant-ui, ACP, Google ADK, AG-UI).
---

# 🧬 SKILL ADN 01 : FRONTEND PUZZLE SDK ARCHITECTURE (DPN-IA N1 ➔ N5)

> **Classification :** Standard Architectural Frontend & SDK UI Snorbik AI (Référence E-Commerce BatiHome & BioStation Pro)
> **Mission :** Construire et assembler des interfaces graphiques React/TypeScript rapidement à partir de pièces prêtes à l'emploi (Banque UI, shadcn, Magic UI, OpenAI ChatKit, assistant-ui) tout en garantissant le respect absolu de l'Architecture en Puzzle à 5 Niveaux (`N1 ➔ N2 ➔ N3 + N4 ➔ N5`) et du plafond de 350 lignes par fichier.

---

## 1. Philosophie Fondatrice : « Assembler des Pièces Prêtes dans une Architecture Stricte »

1. **Ne jamais réinventer les composants de base :** Utiliser les briques éprouvées de la **Banque du MCP Designer** (`shadcn/ui`, `Magic UI`, `21st.dev`, `OpenAI ChatKit`, `assistant-ui`, `BatiHome N1-N5`, `BioStation 3D`) et les configurer selon le Design System du projet.
2. **Ne jamais importer un composant externe en vrac :** Toute pièce externe récupérée depuis la Banque ou un MCP UI externe est immédiatement encapsulée et rangée dans son niveau exact (`01-primitives/` à `05-pages/`).
3. **Le Projet devient un SDK UI Prêt à l'Emploi :** Chaque interface produite expose un point d'entrée SDK (`src/sdk/index.ts`) intégrant nativement le panneau de chat IA et les connecteurs protocolaires **ACP (Agent Communication Protocol)**, **Google ADK (`google-adk`)** et **AG-UI**.

---

## 2. Les 5 Niveaux de l'Architecture en Puzzle (`src/presentation/`)

```text
frontend/src/
├── presentation/
│   ├── 01-primitives/        # N1 : Briques UI atomiques & stateless (35 à 60 lignes)
│   ├── 02-features/          # N2 : Composants métier & Chat Panels IA + use[Feature]Controller.ts + partials/
│   ├── 03-sections/          # N3 : Sections scénographiques (1280px/1440px, split-screen) assemblant N2
│   ├── 04-shell/             # N4 : Coquille applicative (MainLayout, WorkbenchLayout, Header, DevisModal)
│   ├── 05-pages/             # N5 : Pages déclaratives légères (35 à 80 lignes) assemblant N4 + N3
│   └── index.ts              # Barrel export unifié
├── sdk/                      # Couche SDK Agent & Protocoles (ACP, Google ADK, OpenAI ChatKit, assistant-ui)
│   ├── acp/                  # Client Agent Communication Protocol (SSE / REST / JSON-RPC)
│   ├── google-adk/           # Connecteur direct Google Agent Development Kit (useGoogleAdkSession)
│   ├── chat-panels/          # Adaptateurs OpenAI ChatKit (@openai/chatkit-react) & assistant-ui
│   └── index.ts              # Façade SDK exportable
├── core/                     # Domaine et logique pure côté client
├── styles/                   # Design tokens CSS/Tailwind configurables
└── types/                    # Contrats TypeScript stricts (Zéro 'any')
```

### Détail des Responsabilités par Niveau :
- **Niveau 1 (`01-primitives/`)** : Boutons (`Button.tsx`), Badges (`Badge.tsx`), Cartes (`Card.tsx`), Champs (`Input.tsx`), Puces KPI (`KpiChip.tsx`). Purement visuels (*stateless*), **35 à 60 lignes max**.
- **Niveau 2 (`02-features/`)** : Blocs fonctionnels interactifs (ex: `desktop-pilot-panel/`, `configurator-step-form/`, `acp-chat-dock/`). Chaque feature est **obligatoirement** pilotée par son Custom Hook Contrôleur (`use[Feature]Controller.ts`).
- **Niveau 3 (`03-sections/`)** : Grilles et sections larges (`HeroSection`, `CatalogSection`, `WorkspaceSplitSection`) qui orchestrent plusieurs composants N2.
- **Niveau 4 (`04-shell/`)** : `MainLayout.tsx`, `WorkbenchLayout.tsx`, `Header/`, `Footer.tsx`, `SlideOverDrawer.tsx`.
- **Niveau 5 (`05-pages/`)** : Assemblage déclaratif léger (**35 à 80 lignes**) qui branche les sections N3 dans le Shell N4.

---

## 3. Discipline Anti-Fichiers Lourds & Pattern `partials/` + `index.ts`

- **Cible idéale :** **60 à 240 lignes** par fichier.
- **Seuil d'alerte :** **300 lignes**.
- **Plafond absolu (Invariant INV-02) :** **350 lignes maximum**.
- Dès qu'un composant N2 ou N3 dépasse **250 lignes**, il est **obligatoirement** structuré en sous-répertoire partiel :

```text
02-features/acp-pilot-panel/
├── index.ts                          # 1. Barrel Export unique (composant + hook + types)
├── useAcpPilotController.ts          # 2. Custom Hook Contrôleur (état, streaming ACP/ADK, actions)
├── AcpPilotPanel.tsx                 # 3. Orchestrateur visuel léger (80–140 lignes)
└── partials/                         # 4. Sous-vues atomiques (80–200 lignes chacune)
    ├── PilotHeaderBarPartial.tsx
    ├── PilotMessageStreamPartial.tsx
    ├── PilotToolCallCardPartial.tsx
    └── PilotInputQuickChipsPartial.tsx
```

---

## 4. Intégration Standardisée des Chat Panels IA & Protocoles Agents

Au lieu de recoder la logique de chat à la main, le niveau N2 + `src/sdk/` s'appuie sur 4 briques standardisées de la Banque :
1. **OpenAI ChatKit (`@openai/chatkit-react`)** : Composant officiel OpenAI pour le streaming, les threads, les pièces jointes et les widgets d'outils, encapsulé dans `PilotMessageStreamPartial.tsx`.
2. **`assistant-ui` (`@assistant-ui/react`)** : Primitives composables Radix/Tailwind open-source MIT pour le rendu Markdown, le code highlighting et les cartes d'exécution d'outils MCP.
3. **Protocole ACP (`Agent Communication Protocol`)** : Hook standard `useAcpAgentController.ts` gérant les sessions, les événements SSE (`run.created`, `message.delta`, `tool.call`, `run.completed`) et l'annulation.
4. **Google ADK (`google-adk`)** : Hook `useGoogleAdkBridge.ts` permettant de brancher directement l'interface sur un agent ou un swarm Google ADK (`/run_sse`, `/apps/{app_name}/users/{user_id}/sessions`).
