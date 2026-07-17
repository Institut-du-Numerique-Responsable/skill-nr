---
name: Écoconception Ruby
description: Règles d'écoconception pour le code Ruby/Rails — ActiveRecord sobre, batchs, énumérateurs paresseux
globs: "**/*.rb"
---

# Règles d'écoconception — Ruby / Rails

Applique ces règles à tout code Ruby que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_2/3/4 — voir `referentiels/gr491.md`).

## Accès aux données (ActiveRecord)

- Traque le N+1 : `includes`/`preload`/`eager_load` sur les associations parcourues, jamais de lazy loading en boucle.
- Projette les colonnes utiles : `select(:col1, :col2)`, `pluck(:col)` plutôt que `map(&:col)` sur des objets complets.
- Parcours de gros volumes par lots : `find_each`/`in_batches`, jamais de `.all.each` sur une table non bornée ; pagine toute liste exposée (pagy/kaminari).
- `exists?` plutôt que `any?`/`count > 0` (qui chargent ou comptent tout) ; `update_all`/`insert_all` pour les écritures en masse, pas de `save` en boucle.

## Mémoire et CPU

- Chaînes construites avec `<<` (mutation), pas `+=` en boucle ; symboles pour les clés.
- Énumérateurs paresseux (`.lazy`) et `each_slice` pour les longues chaînes de transformations ; ne matérialise pas de tableaux intermédiaires inutiles.
- Recherche d'appartenance dans un `Set` ou un hash, pas `include?` sur un grand tableau.
- Tout cache est borné et expirant (`Rails.cache` avec `expires_in`) — jamais de constante/variable de classe qui accumule sans limite.

## Tâches et I/O

- Jobs d'arrière-plan idempotents et par lots ; pas de job planifié à haute fréquence pour surveiller un état (préfère un déclenchement événementiel).
- Réutilise les connexions HTTP sortantes (client persistant) et le pool de connexions base.
- Logging sobre en production : pas de log dans les boucles serrées, niveaux INFO et au-dessus.
