<!-- Fichier généré par scripts/generer-versions.py, ne pas éditer à la main.
     Source : .continue/rules/ -->

# Règles d'écoconception : Backend, API et données

> S'applique aux fichiers : `**/*.{js,ts,py,java,go,rb,rs,php,sql,kt,cs,c,cc,cpp}`

Applique ces règles à tout code serveur que tu écris ou modifies. Références : RGESN v2 (thématiques Architecture, Backend, Hébergement, Algorithmie) et GR491 (GR491_Backend_1/3/4, GR491_Architecture_3/5, voir `referentiels/gr491.md`).

## API et transferts

- Les API ne renvoient que les champs nécessaires au client : pagine systématiquement les collections, propose un filtrage/une projection des champs, jamais de `SELECT *` exposé tel quel.
- Active la compression (gzip/brotli) et les en-têtes de cache (`Cache-Control`, `ETag`) sur toute réponse cacheable.
- Évite les appels réseau en boucle (problème N+1) : regroupe les requêtes (batch), utilise des jointures ou un dataloader.

## Base de données

- Toute requête sur une table volumineuse doit s'appuyer sur un index ; signale les requêtes qui déclencheraient un full scan.
- Définis une politique de rétention et de purge pour toute nouvelle table ou tout nouveau stockage de données (RGESN : maîtrise du cycle de vie des données).
- Ne stocke pas de données redondantes ou jamais lues ; questionne tout nouveau champ « au cas où ».

## Traitements et algorithmie

- Choisis la structure de données et l'algorithme adaptés au volume réel ; évite les traitements quadratiques sur des collections non bornées.
- Les traitements par lots (batch) doivent être planifiés en heures creuses quand c'est possible et être idempotents pour éviter les ré-exécutions complètes.
- Pas de tâche planifiée à haute fréquence pour vérifier un état : préfère un déclenchement événementiel.
- Pour les usages d'IA : n'appelle un modèle que si un traitement déterministe ne suffit pas, choisis le modèle le plus petit adapté à la tâche, mets en cache les réponses répétitives.

## Ressources et infrastructure

- Dimensionne les ressources au besoin réel : pas de sur-provisionnement par défaut, prévois l'extinction ou la mise à l'échelle à zéro des environnements hors production.
- Journalisation sobre : pas de log verbeux en production, définis une rétention des logs.
- Toute nouvelle dépendance ou service tiers doit être justifié ; préfère les composants déjà présents dans le projet.
