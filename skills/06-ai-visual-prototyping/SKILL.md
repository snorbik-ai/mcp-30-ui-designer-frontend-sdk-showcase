---
name: ai-visual-prototyping
description: Méthode SNORBIK Studio « AI Visual Prototyping » (Quand l'utilisateur arrive SANS MAQUETTE) : Phase 1 Planche 6 Écrans 2x3 (AI Visual Design) ➔ Validation Humaine ➔ Phase 2 Storyboard Vidéo 12s (AI Video Prototyping) ➔ Extraction & Montage React N1-N5.
---

# 🎨 SKILL ADN 06 : AI VISUAL PROTOTYPING (MÉTHODE SNORBIK « ZÉRO MAQUETTE »)

> **Classification :** Méthodologie Officielle SNORBIK Studio — De l'Idée Brute à la Maquette Validée puis au Produit  
> **Principe Fondateur :** **Concevoir ➔ Valider ➔ Animer ➔ Reconstruire.**  
> Ne jamais demander immédiatement une vidéo (coûteuse en crédits si le design est mauvais) et ne jamais coder une interface à l'aveugle sans référence visuelle validée.

---

## 1. Quand activer ce Skill ?

Dès que l'utilisateur dit :
- *"Je n'ai pas encore de maquette, j'ai juste une idée de projet / produit."*
- *"Génère-moi des propositions visuelles d'écrans pour mon application avant de développer."*
- *"Fais-moi le prompt pour créer les maquettes visuelles puis la vidéo de démonstration."*

---

## 2. Le Pipeline Complet « AI Visual-to-Product » (7 Étapes)

1. **Product Brief (`ui_designer_qualify_and_plan_pages`)** : Définition du besoin, des utilisateurs, des 6 écrans clés et de leurs séquences.
2. **Phase 1 — AI Visual Design (`ui_designer_generate_phase1_design_prompt`)** :
   - Génère le **Prompt Maître Phase 1** pour l'agent `image-generator` (agissant comme *Senior SaaS Product Designer + UI/UX Architect + Art Director*).
   - Exige **1 planche haute résolution en paysage (16:9)** organisée en **grille 2 rangées × 3 colonnes (6 écrans distincts)** partageant le même Design System (sans mockup de PC portable ni personnage, sans inventer de fausses conclusions cliniques/métier).
   - **Livrable :** `Visual Design Board` (ex: les 6 écrans de *Bio-Atlas Medical* : Dashboard, Import VCF, Analyse Variants, Genome Explorer, Visualisation 3D, Rapport d'Analyse).
3. **Design Validation (Porte Humaine Obligatoire)** :
   - L'utilisateur et le designer examinent la planche, valident la direction artistique et sélectionnent les écrans retenus **avant** de passer à la Phase 2.
4. **Phase 2 — AI Video Prototyping (`ui_designer_generate_phase2_video_prompt`)** :
   - Génère le **Prompt Storyboard Vidéo de 12 secondes** (6 tranches de `2 secondes` : `00–02s`, `02–04s`, `04–06s`, `06–08s`, `08–10s`, `10–12s`) pour animer et présenter les écrans validés avec des transitions fluides.
   - **Livrable :** `Video Prototype` (10–15s) dont on peut aussi extraire les meilleures frames (à 2s, 4s, 6s…).
5. **UI Reconstruction (`ui_designer_extract_design_system` ➔ `ui_designer_decompose_n1_to_n5`)** :
   - L'image validée sert de **référence de conception** (ce n'est pas du code fonctionnel). Les composants, textes, données et interactions sont reconstruits proprement en React `N1 ➔ N5` + Design System `tokens.css`.
6. **Chasse aux Pièces & Montage (`ui_designer_hunt_parts_3_circles` ➔ `ui_designer_materialize_frontend_sdk`)** :
   - Recherche dans les 3 Cercles (Banque Interne 200+ ➔ MCP Externes gratuits `shadcn` / `Magic UI` / `ChatKit` ➔ Dernier recours IA).
7. **Agentic Coding & Product Delivery (`ui_designer_generate_backend_bridge` ➔ `ui_designer_audit_architecture`)**.

---

## 3. Précaution Critique à Rappeler Systématiquement

| Générateur Visuel / Vidéo | Figma / React (SNORBIK N1–N5) |
| :--- | :--- |
| Explore des directions artistiques | Reproduit précisément les écrans |
| Propose des compositions rapides | Crée des composants réutilisables (`< 350L`) |
| Peut inventer des chiffres ou libellés | Implémente les vraies données & règles déterministes |
| Produit des **références visuelles** | Produit un **logiciel fonctionnel certifié L4** |
