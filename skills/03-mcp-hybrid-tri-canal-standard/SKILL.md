---
name: mcp-hybrid-tri-canal-standard
description: Architecture MCP Hybride Tri-Canal Snorbik AI (MCP JSON-RPC, CLI, SDK Python <2ms), Tablette Contextuelle 7 Sections et Doctrine des Pipelines Séquentielles Conseillées Bipartites (INV-07).
---

# 🧬 SKILL ADN 03 : MCP HYBRID TRI-CANAL & DOCTRINE INV-07

> **Classification :** Standard Industriel de la Flotte Souveraine MCP Snorbik AI
> **Mission :** Structurer chaque serveur MCP interne (y compris le MCP UI Designer #30) selon l'architecture Tri-Canal hermétique, la Tablette Contextuelle 7 Sections et les Pipelines Séquentielles Conseillées Bipartites (`INV-07`).

---

## 1. Architecture Tri-Canal Hermétique (INV-01)

Chaque outil dans `outils_internes/{id}_{nom}/` expose le même cœur métier (`core/`) à travers 3 portes synchronisées :
1. **Porte 1 — Serveur MCP (`canal_mcp/mcp_server.py`)** : Transport standard JSON-RPC 2.0 stdio pour les agents IA (Cursor, Antigravity, Claude Desktop, Claude Code, Google ADK).
2. **Porte 2 — Interface CLI (`canal_sdk_cli/cli.py`)** : Exécution directe en terminal (`--action`, `--list-pipelines`, `--json`).
3. **Porte 3 — SDK Python In-Process (`canal_sdk_cli/sdk.py`)** : Appel Python direct (`< 2ms`, zéro IPC) pour intégration dans un backend FastAPI ou un agent Google ADK.

---

## 2. Les 7 Invariants Industriels (INV-01 à INV-07)

- **INV-01 :** Architecture Tri-Canal (`canal_mcp`, `cli.py`, `sdk.py`) branchée sur `core/domain`, `core/application`, `core/infrastructure`.
- **INV-02 :** Budget de lignes strict `< 350 lignes` par fichier source (cible 60–240 lignes).
- **INV-03 :** Restitution *Digest-First* (résumé décisionnel concis en sortie JSON-RPC, artefacts complets écrits sur disque).
- **INV-04 :** Zéro secret / zéro donnée sensible dans les prompts ou logs.
- **INV-05 :** Contrats Pydantic V2 stricts (`core/domain/entities.py`).
- **INV-06 :** Preuve de test L4 (`tests/test_*.py` couvrant SDK, CLI et MCP).
- **INV-07 :** **Bipartition des Pipelines Séquentielles Conseillées** dans chaque description d'outil :
  - **Partie 1 — Intention & Contexte Métier du Pipeline** (pourquoi utiliser ce chemin).
  - **Partie 2 — Séquence Ordonnée par Noms d'Outils Exacts** avec le marqueur `[CET OUTIL : nom_technique]`.
  - Présence obligatoire de `docs/DOCTRINE_PIPELINES_SEQUENTIELLES.md`.

---

## 3. Principe « Boussole & Moteur Tolérant » (Zéro Prompt Complexe)

L'utilisateur ou le développeur n'a jamais besoin d'écrire un prompt complexe :
- L'outil `*_get_pipelines` agit comme une **boussole** qui indique à l'agent IA la séquence exacte d'outils à appeler selon l'objectif métier.
- Chaque outil accepte aussi une invocation directe (*One-Shot Graceful Fallback*) sans jamais bloquer par une machine à états rigide.
