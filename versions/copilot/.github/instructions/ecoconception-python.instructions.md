---
applyTo: "**/*.py"
description: Règles d'écoconception pour le code Python, ORM sobre, générateurs, vectorisation, caches bornés
---

<!-- Fichier généré par scripts/generer-versions.py, ne pas éditer à la main.
     Source : .continue/rules/ -->

# Règles d'écoconception : Python

Applique ces règles à tout code Python que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_2/3/4, voir `referentiels/gr491.md`).

## Accès aux données (Django ORM / SQLAlchemy)

- Traque le N+1 : `select_related`/`prefetch_related` (Django) ou `joinedload`/`selectinload` (SQLAlchemy), jamais de lazy loading en boucle.
- Projette les champs nécessaires : `only()`/`defer()`/`values()` plutôt que des objets complets.
- Parcours de gros volumes en flux : `iterator()`, `yield_per()`, jamais de `.all()` matérialisé sur une table non bornée ; pagine toute liste exposée.
- Écritures en masse : `bulk_create`/`bulk_update` (Django), `executemany`, pas de `save()` en boucle.

## Mémoire et flux

- Générateurs et `itertools` pour les grandes séquences ; ne matérialise une liste que si tu la réutilises.
- Fichiers et réponses HTTP lus par morceaux (`iter_content`, lecture par chunks), jamais chargés entiers en mémoire.
- pandas/numpy : vectorise au lieu de boucler ligne à ligne (`.apply` row-wise en dernier recours) ; réduis la mémoire avec des dtypes adaptés (`category`, entiers courts).

## CPU et algorithmie

- Recherche d'appartenance dans un `set`/`dict`, pas `in` sur une grande liste (O(n)) ; pas de traitement quadratique sur des collections non bornées.
- Concatène les chaînes avec `''.join(...)`, pas `+=` en boucle.
- Tout cache est borné et expirant (`functools.lru_cache(maxsize=...)`, TTL côté Redis), jamais de dict global qui grossit sans limite.

## I/O et réseau

- Réutilise les connexions : `requests.Session`, pool de connexions base de données ; async (`asyncio`, `httpx`) pour les I/O concurrentes.
- Pas de polling en boucle serrée : préfère un déclenchement événementiel ou espace les intervalles.
- Logging paramétré (`logger.debug("x=%s", x)`), pas de f-string évaluée inutilement dans les chemins chauds ; niveaux de production sobres.
