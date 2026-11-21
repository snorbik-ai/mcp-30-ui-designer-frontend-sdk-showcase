<!-- AUTO-SYNCED FROM SSOT V4.1 | SHA256:dc66573055c9 | SOURCE: articles/01_PATTERN_MCP_HYBRIDE/01_DOCTRINE_ET_MANIFESTE/04_doctrine_universelle_pipelines_sequentielles_v4.md -->

# 🧭 DOCTRINE UNIVERSELLE MCP HYBRIDE — PIPELINES SÉQUENTIELLES, TRIAL BOÎTE NOIRE & PATRIMOINE (V4.0)
*Source Unique de Vérité (SSOT) — Continuité Intégrale V1 ➔ V2 ➔ V3 ➔ V3.1 ➔ V4.0*

> **Référence Canonique :** `articles/01_PATTERN_MCP_HYBRIDE/01_DOCTRINE_ET_MANIFESTE/04_doctrine_universelle_pipelines_sequentielles_v4.md` (SSOT unique de la flotte Snorbik AI).  
> **Continuité Historique :** S'appuie sans suppression sur `v1.md`, `v2.md`, `v3.md` et `v3_1.md`, préservés intacts.  
> **Date :** 21 Novembre 2026 — Version 4.0.  
> **Classification :** Charte Gouvernante de Runtime Boîte Noire, Encadrement Cognitif Tri-Modal, Réutilisation du Patrimoine et Anti-Fork Windows.

---

## 1. Genèse & Gouvernance SSOT : Pourquoi la Version 4.0 ?

Le passage de la V3.0 à la V3.1 puis à la **Version 4.0** fait suite à un **contre-audit boîte noire réel** exécuté sur l'ensemble du parc (59 serveurs inventoriés initialement ➔ 58 actifs après archivage de l'ébauche vide `16_2_youtube_shorts_orchestrator`). Cet audit a mis en évidence 4 angles morts de la V3.0 :
1. **Dérive du Double SSOT :** 148 copies locales `DOCTRINE_PIPELINES*.md` créaient une conformité purement déclarative tandis que des serveurs crashaient au démarrage (`#08`, `#31`, `#32`, `M09`, `M10`, forks `agents_ia/`).
2. **Illusion de Validation Statique :** Des greps syntaxiques produisaient des faux positifs (`#17`, `#19`, `#20`, `#27`, `#29`) tout en manquant le vrai stub de l'auditeur `#26` (corrigé depuis) et des crashs d'imports réels.
3. **Angles Morts Windows (`MAX_PATH` > 260 car.) :** Des chemins profonds dans `banque_de_skills/` ou dans les forks `agents_ia/` masquaient des médias présents ou déclenchaient des `ModuleNotFoundError`.
4. **Dispersion Scripts vs MCP :** Des dizaines de scripts isolés dans `scripts/` réimplémentaient du code déjà disponible dans MCP #19 sans gouvernance par cas d'usage.

**Règle d'Or SSOT V4.0 :** Ce document est **l'unique Source de Vérité**. Les serveurs MCP ne doivent plus maintenir de variantes divergentes : ils pointent vers ce canon par lien relatif ou sont synchronisés automatiquement par l'usine `#17`.

---

## 2. Socle Conservé : Acquis Validés V1.0 ➔ V3.0

1. **V1.0 (`INV-07`) — Le Phare Tolérant :**
   - Quinti-Bloc descriptif (`RÔLE`, `DÉCLENCHEUR`, `OPÉRATION`, `SORTIE`, `PIPELINES SÉQUENTIELLES` bipartite avec marqueur `[CET OUTIL]`).
   - Zéro blocage par machine à états (jamais d'erreur 403) : repli gracieux direct (*One-Shot*) dès que les paramètres sont fournis.
2. **V2.0 (`INV-08` à `INV-11`) — L'Encadrement Cognitif en Boucle Fermée :**
   - Binôme `*_guide` (injection contextuelle paginée, exemplaire neutre anti-copie) et `*_save` (contrôle qualité déterministe tolérant `SAVED_WITH_WARNINGS` + `next_recommended_tool`).
   - Frontière stricte Déterministe (Python/CLI) vs Cognitif (LLM), sérialisation `orjson` compacte et clôture physique via `*_session_status`.
3. **V3.0 (`INV-12` à `INV-15`) + Taxonomie Tri-Modale :**
   - Chaque outil déclare explicitement sa nature dans `tools/list` : `[NATURE : DOC_PURE]`, `[NATURE : SCRIPT_PUR]` ou `[NATURE : HYBRIDE_DOC_ET_SCRIPT]` (`mode="get_skill_and_guide"` / `mode="execute"`).
   - **Banque de Skills à Double Niveau** (prouvée sur MCP #19 v3.0.0) : banque globale embarquée (`banque_de_skills/skills/`) + sous-banques dédiées par outil (`tool_skill_banks_registry.py`), avec découverte via `*_skills_list`, `*_skills_get_guide` et scellement via `*_skills_capture_success`.

---

## 3. Les 3 Nouveaux Invariants V4.0 (Runtime, Patrimoine & Architecture)

### 3.1 `INV-00` — Protocole JSON-RPC 2.0 & Test Trial Boîte Noire Obligatoire
Aucun serveur MCP ne peut être déclaré conforme s'il échoue au **crash-test runtime JSON-RPC 2.0 stdio** :
1. Répondre proprement à `initialize` (`protocolVersion`, `capabilities`, `serverInfo`).
2. Ignorer silencieusement `notifications/initialized` (requêtes sans `id`).
3. Répondre à `tools/list` avec le schéma valide de tous les outils déclarés.
4. **Préservation stricte de `req_id` sur erreur JSON-RPC :** Ne jamais émettre `"id": null` lors d'un `tools/call` identifié (source de timeouts client).
5. **Zéro Stub Silencieux :** Interdiction absolue de renvoyer `"COMPLETED"` sans traitement effectif ; toute action non supportée doit retourner explicitement `"UNSUPPORTED_ACTION"`.
- **Application :** Audité en réel par **MCP #26 (`26_doctrine_compliance_orchestrator`)** via `core/infrastructure/fleet_trial_scanner.py` (`audit_fleet(..., run_trial=True)`), avec timeout adapté ($\ge 18$s) pour les serveurs à chargement lourd (ex. `#02`).

### 3.2 `INV-16` — Réutilisation du Patrimoine & Capability Registry SNORBIK
Conformément à `docs/00_GOUVERNANCE/02_DOCTRINE_REUTILISATION_PATRIMOINE_SNORBIK_V1.md` et `capability_registry_v1.json` :
1. **Cycle obligatoire avant tout développement :** *Analyser ➔ Reproduire ➔ Réutiliser ➔ Renforcer ➔ Créer sur Use Case*.
2. **Use Case Obligatoire :** Aucun outil ou module n'est créé sans problème métier, entrées/sorties, capacités existantes réutilisées et critères de validation.
3. **Fiche de Qualification en 10 points :** Toute brique extraite depuis `scripts/` est qualifiée avant intégration dans un serveur cible (priorité : renforcement continu de **MCP #19** plutôt que multiplication de scripts autonomes).

### 3.3 `INV-17` — Règle Anti-Fork `agents_ia/` & Prévention des Collisions d'ID
1. **Interdiction de Forker les Mini-MCP :** Il est interdit de copier `mini_mcp/M05..M09` dans `agents_ia/<agent>/mcp_servers/` (source directe de 9 crashs `ModuleNotFoundError` sous Windows `MAX_PATH`). Tous les agents doivent consommer la source unique `outils_internes/mini_mcp/`.
2. **Unicité des Préfixes & IDs Flotte :** Toute collision de préfixe numérique (ex. `#12`, `#16`) détectée par `#26` doit être résolue de manière coordonnée avec `.mcp.json` et `install_mcp.py`.

### 3.4 `INV-18` — Doctrine SDK & Documentation Embarquée Autonome Synchronisée
Pour éviter tout lien mort lors d'une installation client isolée hors monorepo, **chaque MCP, Mini-MCP et SDK (petit ou grand)** doit :
1. Embarquer dans `docs/DOCTRINE_PIPELINES_SEQUENTIELLES.md` la copie autonome générée depuis ce SSOT (`<!-- AUTO-SYNCED FROM SSOT V4.1 | SHA256:... -->`).
2. Exposer côté SDK les méthodes `get_doctrine()`, `get_runtime_requirements()` et `get_recommended_pipelines()` (ou via le module embarqué `sdk_doctrine.py`).

### 3.5 `INV-19` — Minimum Python Embarqué & Zéro-Installation Client
Aucun client ne doit avoir à télécharger ou installer Python manuellement :
1. Chaque MCP et SDK embarque `snorbik_bootstrap.py` v2.0 + `runtime_requirements.json` (`min_python: "3.10"`, `docker_base_image: "python:3.12-slim"`).
2. Cascade de résolution : (1) mini-Python pré-embarqué dans le bundle ou l'image (`SNORBIK_EMBEDDED_PYTHON`, `./runtime/python/`, `/opt/snorbik-python/`), (2) cache `~/.snorbik/python-runtime/`, (3) Python système $\ge 3.10$, (4) auto-provisionnement silencieux sans droits admin (via `install.ps1` / `install.sh` / `snorbik_bootstrap.py`).
3. Tout livrable ou image destiné à un client passe obligatoirement la barrière `verify_embedded_runtime_for_delivery` (`Dockerfile.runtime` / image `python:3.12-slim` ou `runtime/python/` présent) avant expédition.

---

## 4. Les 3 Paliers Adaptatifs de Conformité

Afin d'éviter la sur-ingénierie cosmétique sur les utilitaires atomiques tout en maintenant une rigueur maximale sur les usines de production :

| Palier | Cible | Exigences Obligatoires | Exemples Flotte |
| :--- | :--- | :--- | :--- |
| **Palier 1 — Atomique / Mini-MCP** | Briques unitaires déterministes | `INV-00` (trial PASS) + `INV-07` (`[CET OUTIL]` bipartite + One-Shot) | `#03`, `#10`, `#14`, `M01`–`M11` |
| **Palier 2 — Workflow / Cognitif** | Processus multi-étapes ou rédaction LLM | Palier 1 + `*_get_pipelines` + boucle V2 `guide / save / session_status` si rédaction | `#06`, `#08`, `#16`, `#18`, `#26`, `#28`, `#29`, `#31` |
| **Palier 3 — Usine à Skills & Tri-Modal** | Production récurrente à forte capitalisation | Palier 2 + Taxonomie Tri-Modale (`DOC_PURE` / `SCRIPT_PUR` / `HYBRIDE`) + `INV-12..17` | `#15`, `#16.2`, `#19`, `#30`, `#32` |

---

## 5. Révisions Officielles V4.0 de `INV-13` et `INV-15`

### 5.1 `INV-13` Révisé — Exemplaires Phares & Résilience Windows `MAX_PATH`
- **Problème résolu :** Les chemins profonds dépassant 260 caractères dans `banque_de_skills/.../exemplaire_phare/` provoquaient des `WinError 3` sous Windows et donnaient l'illusion de fichiers manquants.
- **Règle V4.0 :**
  1. Référencer prioritairement des **chemins canoniques courts** (`article/MEDIA_HUB_show_case/...`), accompagnés d'un script `reproduce.py`, d'une empreinte `SHA-256` et de métriques mesurées.
  2. Tout adaptateur d'E/S sous Windows (ex. `studio_usecases.py`, `multilingual_showcase_builder.py`) **doit** résoudre les chemins relatifs, utiliser le préfixe étendu `\\?\` (`win_long` / `safe_copy`), et isoler les rendus FFmpeg dans un répertoire temporaire court.

### 5.2 `INV-15` Révisé — Guichet Unique de Responsabilité & Chaînage Inter-MCP
Plutôt qu'un monopole absolu irréaliste sur toute la chaîne média, `INV-15` formalise le **Guichet Unique par Domaine + Chaînage Inter-MCP** :
- **Capture & Audit UX Web :** `#16` (`16_web_site_crawler_ux_auditor`) et `#16.2` (`16_2_web_media_studio_orchestrator` ; le dossier vide `16_2_youtube_shorts_orchestrator` est archivé).
- **Décodage, Savoir & Voix :** `#18` (`18_youtube_decoder_knowledge_engine`) et `M11`.
- **Montage, QA, Miniatures & Banque de Skills :** `#19` (`19_text_to_video_factory`), dont les **9 identifiants réels de skills** dans `banque_de_skills/skills/` sont désormais normalisés :
  - `marketing_multichannel_publication_pack`
  - `snorbik_marketing_script_writer`
  - `video_bio_atlas_biostation`
  - `video_copilot_medical`
  - `video_demo_vitrine_60s`
  - `video_images_to_commercial_30s`
  - `video_loop_cinemagraphe_6s`
  - `video_spot_commercial_30s`
  - `video_website_walkthrough_30s`

---

## 6. Matrice Comparative : Évolution V1 ➔ V2 ➔ V3 ➔ V4

| Critère | V1.0 (`INV-07`) | V2.0 (`INV-08..11`) | V3.0 (`INV-12..15`) | V4.0 (`INV-00`, `16`, `17`) |
| :--- | :--- | :--- | :--- | :--- |
| **SSOT Doctrine** | Copies multiples par outil | Copies multiples enrichies | Double SSOT + 148 copies | **SSOT Unique** + pointeurs sync `#17` |
| **Vérification Flotte** | Relecture statique | Test agent vierge ponctuel | Benchmark cold-start `#19` | **Trial Boîte Noire `INV-00`** via `#26` |
| **Taxonomie & Skills** | Descriptions libres | `guide / save / session_status` | Banque de skills `SKILL.md` | **Tri-Modal** + double niveau + vrais IDs |
| **Réutilisation Code** | Non encadrée | Séparation LLM / Python | Guichet unique vidéo | **`INV-16` Capability Registry** + Use Case |
| **Portabilité Windows** | Non traitée | `orjson` & pagination 28k | Chemins longs fragiles | **`\\?\` obligatoire + `INV-17` Anti-Fork** |
| **Granularité** | Uniforme | Quasi-uniforme | Pression uniforme V3 | **3 Paliers Adaptatifs** (P1 / P2 / P3) |
