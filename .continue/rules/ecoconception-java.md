---
name: Écoconception Java
description: Règles d'écoconception pour le code Java, JPA/Hibernate sobre, mémoire, batch, logs
globs: "**/*.java"
---

# Règles d'écoconception : Java

Applique ces règles à tout code Java que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_2/3/4, voir `referentiels/gr491.md`).

## Accès aux données (JPA / Hibernate / JDBC)

- Traque le N+1 : charge les associations nécessaires avec `JOIN FETCH` ou `@EntityGraph`, jamais en laissant le lazy loading boucler.
- Pour la lecture seule, projette dans des DTO (constructeur JPQL, interface projection Spring Data) plutôt que de charger des entités complètes managées.
- Pagine systématiquement (`Pageable`, `setMaxResults`) ; jamais de `findAll()` sur une table non bornée.
- Les écritures en masse passent par le batch JDBC (`hibernate.jdbc.batch_size`, `saveAll` par tranches) et les traitements longs par chunks (Spring Batch), pas entité par entité.
- Dimensionne le pool de connexions (HikariCP) au besoin réel ; ferme les ressources avec try-with-resources.

## Mémoire et CPU

- Évite les allocations dans les boucles chaudes ; `StringBuilder` pour les concaténations répétées.
- Streams : pas de `parallelStream()` par défaut (il consomme tous les cœurs pour un gain rarement mesuré) ; attention au boxing dans les pipelines (`IntStream` plutôt que `Stream<Integer>`).
- Choisis des structures adaptées au volume (`ArrayList` pré-dimensionnée, `EnumMap`/`EnumSet`…) ; pas de tri ou de recherche linéaire répétée sur de grosses collections.
- Tout cache doit être borné et expirant (Caffeine : `maximumSize` + `expireAfterWrite`), jamais de `HashMap` statique qui grossit sans limite.

## API et sérialisation

- Ne sérialise que les champs utiles au client : DTO dédiés ou `@JsonView`, pas d'entité JPA exposée telle quelle (poids, boucles, couplage).
- Active la compression HTTP et les en-têtes de cache sur les réponses cacheables.

## Logs et tâches

- Logging paramétré (`log.debug("x={}", x)`), jamais de concaténation évaluée inutilement ; pas de log dans les boucles serrées ; niveaux de production sobres (INFO et au-dessus).
- Pas de `@Scheduled` à haute fréquence pour surveiller un état : préfère un déclenchement événementiel (listener, message).
