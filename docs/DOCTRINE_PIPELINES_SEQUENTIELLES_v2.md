# 🧭 DOCTRINE UNIVERSELLE MCP HYBRIDE — PIPELINES SÉQUENTIELLES CONSEILLÉES (V2.0)
## Passage de la Boucle Ouverte (V1 : Phare Passif) à la Boucle Fermée Active (V2 : Encadrement Cognitif & Quality Gates)

> **Référence :** Architecture Solution Logicielle MCP Hybride Snorbik AI — Charte Universelle V2.0  
> **Continuité :** S'appuie sur `04_doctrine_universelle_pipelines_sequentielles_v1.md` (V1 préservée intacte)  
> **Date :** Novembre 2026 — Version 2.0  
> **Classification :** Standard d'Encadrement Cognitif pour Serveurs MCP Mixtes (Exécution + Raisonnement IA)

---

## 1. Retour d'Expérience Terrain : Pourquoi la V1 Seule Ne Suffisait Plus

La **Doctrine V1 (INV-07)** a posé deux acquis fondateurs définitifs :
1. **Principe du « Phare de Navigation & Moteur Tolérant » :** Pas de verrous bloquants `403` ; repli gracieux en exécution directe (*One-Shot*).
2. **Bipartition Obligatoire du Bloc 5 (`TOOLS_METADATA`) :** *Partie 1 (Intention & Contexte Métier)* + *Partie 2 (Séquence ordonnée par noms d'outils exacts avec marqueur `[CET OUTIL : ...]`)*.

**Limites observées en production sur des workflows cognitifs complexes (ex. MCP 18) :**
- En V1, la doctrine fonctionnait en **boucle ouverte (*Open-Loop*)** : les descriptions indiquaient l'ordre des outils à appeler, mais dès qu'un outil de guide ou de sauvegarde ne retournait qu'un chemin de fichier ou acceptait n'importe quel texte sans contrôle, une IA pressée pouvait :
  1. Ne lire que le début d'une source longue (manquant un tunnel de vente ou une conclusion critique),
  2. Halluciner des chiffres, des timecodes ou des concurrents sans recherche préalable,
  3. Recopier un gabarit/exemplaire biaisé au lieu de produire une analyse neuve,
  4. Persister un livrable incomplet, contenant un lien promotionnel interdit ou un fichier audio corrompu.

**Réponse de la V2 :** La V2 conserve 100 % du phare tolérant V1 et y ajoute **4 invariants de boucle fermée active (INV-08 v2 à INV-11)** pour transformer le GPS passif en **système d'encadrement anti-dérapage**.

---

## 2. Les Acquis V1 Conservés Intégralement (Socle Obligatoire)

Tout serveur MCP de la flotte continue d'appliquer :
- **INV-07 (Bipartition & Phare Tolérant) :** Structure Quinti-Bloc (`[RÔLE]`, `DÉCLENCHEUR`, `OPÉRATION`, `SORTIE`, `PIPELINES SÉQUENTIELLES CONSEILLÉES` en 2 parties).
- **Pilier `*_get_pipelines` :** Point d'entrée d'orientation non bloquant en tête de `tools/list`.
- **Tablette `context_llm.json` & Contrôleur #26 :** Registre GPS et audit de conformité.

---

## 3. Les 4 Nouveaux Invariants V2 — Encadrement Cognitif en Boucle Fermée

### 3.1 INV-08 v2 — Pattern Binôme `*_guide` / `*_save` avec Injection Directe & Pagination
Tout traitement cognitif riche (analyse critique, scénarisation, rédaction stratégique) est découpé en **deux outils complémentaires** :
1. **L'outil `*_guide` (Fournisseur de Contexte & Prompt Maître) :**
   - Ne renvoie **jamais uniquement un chemin de fichier** : il **injecte directement dans sa réponse JSON** la matière première brute, les signaux déjà extraits par code déterministe (chiffres, dates, fin de document), les instructions pas-à-pas et un **Exemplaire Neutre Hors-Domaine**.
   - **Pagination obligatoire (`chunk_index` / `chunk_size`) :** Si la matière première dépasse la fenêtre sûre (ex. `28 000` caractères), le guide découpe sur des frontières sémantiques propres et renvoie `total_chunks`, `has_more_chunks` et `next_chunk_instruction`.
   - **Règle de l'Exemplaire Neutre :** L'exemplaire fourni doit appartenir à un domaine totalement étranger au sujet cible habituel (ex. rénovation énergétique / pompe à chaleur pour un outil média tech) afin d'éviter toute contamination par recopie.

2. **L'outil `*_save` (Persistance & Contrôle) :**
   - Reçoit le livrable produit par l'IA, l'écrit dans les répertoires de session normés, génère les artefacts dérivés (ex. audio MP3) et met à jour le manifeste de session.

### 3.2 INV-09 — Quality Gate Tolérant & `next_recommended_tool` Dynamique
Chaque outil `*_save` exécute un **Quality Gate déterministe** vérifiant des critères objectifs (présence des sections obligatoires, bornes temporelles `timecode <= duration`, citation de sources, détection anti-copie de l'exemplaire neutre, absence d'URL/spam, intégrité binaire et taille réelle des fichiers générés).
- **Zéro verrou `403` bloquant (fidélité V1) :** Si un critère échoue, l'outil sauvegarde malgré tout le brouillon pour traçabilité, retourne :
  - `status: "SAVED_WITH_WARNINGS"`
  - `quality_gate: { "passed": false, "score_pct": <score>, "missing_requirements": [...], "action_required": "..." }`
  - **`next_recommended_tool` dynamique :** pointe automatiquement vers le même outil `*_save` (ou le prérequis manquant) jusqu'à ce que `passed == true`, moment où `next_recommended_tool` bascule vers l'étape suivante.

### 3.3 INV-10 — Frontière Stricte Déterministe vs Cognitif & Sérialisation `orjson` Compacte
1. **Règle de Répartition :**
   - **Moteur Déterministe (Python/Rust/CLI) :** Extraction de métadonnées (`yt-dlp`), recherche de concurrents récents (fenêtre temporelle, vues, créneau horaire, transcripts), extraction de chiffres, validation binaire, calculs, rendu TTS. *(Interdiction de laisser l'IA deviner des métriques ou concurrents de mémoire.)*
   - **Agent IA (Cognitif) :** Compréhension sémantique, recherche web de preuves, tri critique, créativité éditoriale et rédaction diplomate.
2. **Efficacité Économique (`orjson` compact) :**
   - Les charges utiles renvoyées au LLM dans `content[0].text` et les fichiers de données brutes utilisent **`orjson` compact** (`pretty=False`, zéro `indent=2`), réduisant la consommation de tokens de **20–25 %** et accélérant la sérialisation d'un facteur **~17× à 20×**.

### 3.4 INV-11 — Certification Boîte Noire par Agent IA Vierge & `*_session_status`
Tout serveur MCP critique doit exposer un outil de clôture `*_session_status` vérifiant physiquement la présence de 100 % des livrables, les statuts de tous les Quality Gates et l'intégrité binaire des sorties.
Avant de déclarer un serveur prêt pour la production, il doit réussir un **Crash-Test Boîte Noire** : un **agent IA vierge** (n'ayant ni lu le code source interne ni reçu d'instructions cachées) doit atteindre `completion_pct == 100.0` sur un cas réel inédit en suivant uniquement `*_get_pipelines`, les descriptions INV-07 et les réponses des outils.

---

## 4. Matrice de Décision : Quand Appliquer V1 Seule vs V2 Complète

| Type de Serveur MCP | Version Doctrine Recommandée | Exemples | Justification |
| :--- | :---: | :--- | :--- |
| **Outil 100 % Déterministe / Unitaire** | **V1 (INV-07)** | `07-codefocus`, `08-docker-deployment`, `03-media-quality-auditor` | Aucun raisonnement créatif LLM requis : la bipartition + repli *One-Shot* suffit sans alourdir. |
| **Outil Mixte (Exécution + Workflows IA Riches)** | **V2 (INV-07 + INV-08 v2 à INV-11)** | `18-youtube-decoder`, `19-text-to-video-factory`, `28-cv-director`, `30-ui-designer` | L'IA produit des livrables complexes (analyses, scripts, UI, CV) exposés aux risques de paresse, d'oubli ou d'hallucination. |

---

## 5. Gabarit Canonique de Réponse d'un Outil V2 (GPS Dynamique)

```json
{
  "status": "WORKFLOW_GUIDE_READY | SUCCESS | SAVED_WITH_WARNINGS | COMPLETE",
  "session_dir": "/chemin/session",
  "quality_gate": {
    "passed": true,
    "score_pct": 100.0,
    "missing_requirements": [],
    "action_required": "OK - Livrable certifié conforme."
  },
  "next_recommended_tool": "nom_exact_de_l_outil_suivant_ou_COMPLETE"
}
```
