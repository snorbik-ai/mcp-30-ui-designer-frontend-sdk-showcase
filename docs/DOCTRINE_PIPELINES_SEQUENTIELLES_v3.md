# 🧭 DOCTRINE UNIVERSELLE MCP HYBRIDE — PIPELINES SÉQUENTIELLES CONSEILLÉES (V3.0)
## De l'Encadrement Cognitif (V2) à la Banque de Skills Souveraine & la Capitalisation d'Expériences Réussies (V3)

> **Référence :** Architecture Solution Logicielle MCP Hybride Snorbik AI — Charte Universelle V3.0  
> **Continuité :** S'appuie sur `DOCTRINE_PIPELINES_SEQUENTIELLES_v1.md` et `DOCTRINE_PIPELINES_SEQUENTIELLES_v2.md`, préservées intactes.  
> **Date :** Novembre 2026 — Version 3.0  
> **Classification :** Standard d'Encadrement Cognitif, Mémoire Évolutive et Guichets Uniques pour Serveurs MCP et Systèmes Multi-Agents.

---

## 1. Genèse & Vision : Pourquoi la Version 3.0 ?

### L'Évolution en 3 Étapes Fondatrices
1. **Version 1.0 (INV-07 — Le Phare Tolérant en Boucle Ouverte) :**
   - Quinti-Bloc descriptif avec bipartition et marqueur `[CET OUTIL]`.
   - Zéro verrou 403 bloquant, repli direct One-Shot.
2. **Version 2.0 (INV-08 v2 à INV-11 — L'Encadrement Cognitif en Boucle Fermée) :**
   - Binôme `*_guide` paginé / `*_save` persistant.
   - Quality Gates déterministes tolérants (`SAVED_WITH_WARNINGS` et `next_recommended_tool` dynamique).
   - Frontière déterministe vs cognitif + `orjson` compact (20-25% de tokens économisés).
   - Outil transverse de clôture `*_session_status` et certification boîte noire.
3. **Version 3.0 (INV-12 à INV-15 — Banque de Skills & Capitalisation d'Expériences Réussies) :**
   - **Transformer chaque succès validé en compétence permanente réutilisable (Skill Agent).** Tout savoir-faire ayant abouti à un résultat validé par l'humain est gravé dans une **Banque de Skills Embarquée (Skill Bunker)**, documenté selon le standard Google Antigravity / Gemini Skill (`SKILL.md`), associé à son **Exemplaire Phare (Golden Master)** et invocable via des outils dédiés de découverte et d'application directe.

---

## 2. Les 4 Nouveaux Invariants V3.0 — Capitalisation & Mémoire Cognitive

### 2.1 INV-12 — Banque de Skills Embarquée & Format Standard Google Antigravity
Chaque serveur MCP possède son propre répertoire de compétences capitalisées : `skills/`.
Chaque compétence est scellée dans un dossier autonome portant un fichier **`SKILL.md`** respectant le format standard Google : frontmatter YAML `name`, `description`, contexte métier, matières premières, workflow pas-à-pas, paramètres calibrés et pièges évités.

### 2.2 INV-13 — Conservation des Exemplaires Phares (Golden Masters / Benchmarks)
Chaque skill référence obligatoirement son **Exemplaire Phare Validé** physique (ex: `article/MEDIA_HUB_show_case/01_copilot_medical/02_VIDEO/copilot_medical_official_60s.mp4`), avec ses métriques exactes et son script de reproduction 1-clic.

### 2.3 INV-14 — Outils MCP de Découverte & Sélection Dynamique de Skills
Tout serveur MCP V3 expose :
1. **`*_skills_list` :** Restitue la liste des compétences éprouvées disponibles (permettant à l'IA de proposer un choix clair à l'utilisateur).
2. **`*_skills_get_guide` :** Injecte la recette pas-à-pas et l'exemplaire étalon.

### 2.4 INV-15 — Guichet Unique Métier & Scellement d'Expérience Réussie
1. **Règle du Guichet Unique :** Centralisation absolue des outils d'un même domaine. Pour la vidéo, **MCP #19 est le GUICHET UNIQUE ABSOLU** (musique, voix, montage, infographies, cinémagraphes).
2. **Outil `*_skills_capture_success` :** Permet à l'agent ou à l'utilisateur de sceller une recette validée en 1 clic dans la banque de skills.

