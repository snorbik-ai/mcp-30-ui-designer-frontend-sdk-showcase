# 🧭 DOCTRINE UNIVERSELLE MCP HYBRIDE — PIPELINES SÉQUENTIELLES CONSEILLÉES
## Standard Canonique d'Autonomie Cognitive Multi-Chemins & Bipartition INV-07

> **Référence :** Architecture Solution Logicielle MCP Hybride Snorbik AI — Charte Universelle  
> **Auteur :** Collège d'Ingénierie BatiHome / SNORBIK AI  
> **Date :** Novembre 2026 — Version 1.0  
> **Classification :** Directive Fondatrice Obligatoire pour tous les Outils de la Flotte MCP  

---

## 1. Philosophie Fondatrice : Phare de Navigation vs Verrou Bloquant

Dans la conception d'outils pour agents IA autonomes, une pathologie classique consiste à enfermer les serveurs MCP dans une machine à états finis (*Finite State Machine*) rigide et bloquante :
- Si l'outil n°4 est invoqué avant l'outil n°2, le serveur lève une exception fatale du type `403 Precondition Failed : State must be STEP_2`.
- Si un développeur ou un agent IA souhaite exécuter un rendu de test rapide ou une vérification unitaire, le système refuse catégoriquement l'opération.

### Le Principe Snorbik du « Phare de Navigation & Moteur Tolérant »
La doctrine Snorbik AI récuse formellement cette approche autoritaire :
1. **L'Agent IA est le Capitaine Décisionnel :** L'agent opère dans un univers sémantique et probabiliste. Il doit être guidé avec une précision chirurgicale, mais ne doit jamais être paralysé par un verrou arbitraire.
2. **Le Serveur MCP est un Phare Bienveillant :** Le serveur expose la route optimale recommandée, mais chaque outil dispose d'un mécanisme de repli gracieux (*Graceful Fallback*) permettant une exécution directe (*One-Shot*) si les paramètres requis lui sont fournis directement.
3. **Zéro Erreur Préconditionnelle Bloquante :** Aucun outil ne doit rejeter un appel au seul prétexte qu'un outil antérieur n'a pas été appelé dans la même session.

---

## 2. La Règle d'Or de la Bipartition Obligatoire (Standard INV-07)

Dans toute description d'outil MCP (`TOOLS_METADATA`, registres `mcp_config.json`, `.cursor/mcp.json`), la section **PIPELINES SÉQUENTIELLES CONSEILLÉES** (Bloc 5 de la structure Quinti-Bloc) DOIT obligatoirement être articulée en **Deux Conseils Complémentaires** :

### 2.1 Conseil 1 — Partie 1 : L'Intention du Pipeline & Contexte Métier
- **Objectif :** Expliquer à l'agent IA **pourquoi** ce pipeline existe et **dans quelle situation** l'activer.
- **Contenu :** Définition claire du cas d'usage métier (ex: *Pipeline 1 : Audit E2E Complet*, *Pipeline 2 : Fast Check Responsive 1-Clic*, *Pipeline 3 : Recalcul Certifié Express*).
- **Valeur Ajoutée :** Évite à l'agent d'errer ou d'invoquer une suite d'outils inadaptée au contexte de la demande utilisateur.

### 2.2 Conseil 2 — Partie 2 : La Séquence Ordonnée par Noms d'Outils Exacts
- **Objectif :** Donner la recette pas-à-pas stricte et chronologique des outils à invoquer.
- **Règle Typographique Stricte :** Les noms utilisés doivent être **strictement identiques** aux identifiants techniques déclarés dans `tools/list` (ex: `visual_diag_session_init`, `quote_calculate_certified`). Aucun nom imaginaire ou approximatif n'est toléré.
- **Le Marqueur Visuel de Position :** L'outil en cours de description doit être immédiatement repérable dans la séquence grâce au marqueur explicite :
  `[CET OUTIL : nom_technique_courant]` ou `[THIS TOOL : technical_name]`
- **Bénéfice Cognitif :** L'agent IA visualise immédiatement où il se situe dans la chaîne de production et sait sans ambiguïté quel outil appeler ensuite.

---

## 3. Gabarit Canonique de Description Quinti-Bloc Bipartite

Toute primitive MCP d'un outil interne Snorbik AI respecte ce schéma universel :

```text
[RÔLE EN MAJUSCULES] Définition précise et concise de la fonction métier opérée.
DÉCLENCHEUR CONSEILLÉ : Circonstances, moments idéaux et pré-requis logiques d'appel.
OPÉRATION : Traitement déterministe local exécuté par le moteur (Clean Architecture).
SORTIE : Synthèse décisionnelle condensée (Digest JSON) et artefacts physiques persistés.

PIPELINES SÉQUENTIELLES CONSEILLÉES :
  • PARTIE 1 — INTENTION & CONTEXTE MÉTIER :
    - Pipeline 1 (Nom du flux complet) : Pourquoi et quand utiliser ce flux exhaustif.
    - Pipeline 2 (Nom du flux rapide) : Pourquoi et quand utiliser ce raccourci opérationnel.
  • PARTIE 2 — SÉQUENCE ORDONNÉE PAR NOMS D'OUTILS EXACTS :
    - Séquence Pipeline 1 :
      1. tool_a_init
      ➔ 2. tool_b_discover
      ➔ 3. [CET OUTIL : tool_c_execute]
      ➔ 4. tool_d_finalize
    - Séquence Pipeline 2 :
      1. [CET OUTIL : tool_c_execute(mode="direct")]
      ➔ 2. tool_d_finalize
```

---

## 4. Exemple Concret Référent : L'Outil `visual_diag_audit_layout`

L'exemple suivant matérialise l'application exacte de la doctrine pour l'outil d'audit géométrique :

```text
[ANALYSE GÉOMÉTRIQUE DU DOM & DÉTECTION DES COLLISIONS]
DÉCLENCHEUR CONSEILLÉ : Après capture multi-formats pour mesurer les espacements et les collisions réelles.
OPÉRATION : Analyse les bounding boxes, calcule les dégagements (clearance < 0) et chevauchements.
SORTIE : Digest condensé des anomalies géométriques classées P0/P1/P2 avec coordonnées DOM.

PIPELINES SÉQUENTIELLES CONSEILLÉES :
  • PARTIE 1 — INTENTION & CONTEXTE MÉTIER :
    - Pipeline 1 (Audit E2E Complet) : Cartographie, capture, géométrie, contraste, plan et validation de non-régression.
    - Pipeline 2 (Fast Check Responsive 1-Clic) : Diagnostic géométrique ciblé et immédiat sans exploration de l'arborescence.
  • PARTIE 2 — SÉQUENCE ORDONNÉE PAR NOMS D'OUTILS EXACTS :
    - Séquence Pipeline 1 :
      1. visual_diag_session_init
      ➔ 2. visual_diag_discover
      ➔ 3. visual_diag_capture_matrix
      ➔ 4. [CET OUTIL : visual_diag_audit_layout]
      ➔ 5. visual_diag_audit_contrast
      ➔ 6. visual_diag_plan_corrections
      ➔ 7. [ACTION CODEUR / AGENT]
      ➔ 8. visual_diag_validate_diff
    - Séquence Pipeline 2 :
      1. visual_diag_capture_matrix
      ➔ 2. [CET OUTIL : visual_diag_audit_layout]
```

---

## 5. Les 4 Piliers d'Implémentation Technique dans chaque MCP

Pour être certifié conforme, chaque serveur MCP de la flotte doit matérialiser cette doctrine sur 4 piliers :

1. **Pilier 1 — L'Outil d'Introspection Dédié :**
   Tout serveur MCP expose obligatoirement une fonction `[nom_outil]_get_pipelines` (ex: `visual_diag_get_pipelines`, `quote_orchestrator_get_pipelines`, `video_studio_get_pipelines`) permettant à l'agent de découvrir les chemins sans effet de bord.
2. **Pilier 2 — La Façade SDK & CLI :**
   - Le SDK in-process (`canal_sdk_cli/sdk.py`) fournit `sdk.get_recommended_pipelines()`.
   - L'interface terminal (`canal_sdk_cli/cli.py`) propose `--list-pipelines`.
3. **Pilier 3 — La Tablette Contextuelle `context_llm.json` :**
   La section `SEC_03_GPS_TOOLS_REGISTRY` intègre systématiquement le composant `COMP_05_OFFICIAL_PIPELINES`.
4. **Pilier 4 — Le Sas de Validation Pré-Vol & Outil #26 :**
   L'Outil #26 (`doctrine_compliance_orchestrator`) vérifie que 100% des outils exposés respectent la bipartition et la nomenclature ordonnée.

---

## 6. Directive d'Usine MCP #17

Tout nouveau serveur MCP généré par l'Usine MCP #17 (`17_mcp_factory_launcher`) embarque automatiquement un exemplaire conforme de la présente doctrine dans son dossier `docs/DOCTRINE_PIPELINES_SEQUENTIELLES.md`.

---

## 7. Doctrine du Double Rôle : Exécuteur Déterministe & Guide Cognitif (INV-08)

Un serveur MCP Snorbik AI ne sert **pas uniquement à exécuter des scripts ou du code local**. Il remplit deux missions complémentaires :
1. **Exécuteur Déterministe :** Traiter des données, auditer du code, calculer des devis ou générer des fichiers avec zéro hallucination.
2. **Guide Cognitif (Fournisseur de Workflows & Prompts Maîtres) :** Guider l'agent IA étape par étape et lui fournir des **prompts structurés prêts à l'emploi** ou des **plans de séquence** (ex: AI Visual Prototyping Phase 1/Phase 2, qualification de besoin, plans d'architecture), afin que l'utilisateur n'ait jamais à rédiger de prompts complexes.
