---
name: Écoconception C#
description: Règles d'écoconception pour le code C#/.NET, Entity Framework sobre, async, allocations, logs
globs: "**/*.cs"
---

# Règles d'écoconception : C# / .NET

Applique ces règles à tout code C# que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_2/3/4, voir `referentiels/gr491.md`).

## Accès aux données (Entity Framework Core / ADO.NET)

- Lecture seule : `AsNoTracking()` systématique, et projection `Select(x => new Dto { ... })` plutôt que de matérialiser des entités complètes.
- Traque le N+1 : `Include`/`ThenInclude` ciblés ou requête projetée ; jamais de lazy loading qui boucle sur une collection.
- Garde le travail côté base : filtre et agrège sur `IQueryable` avant toute matérialisation ; un `ToList()`/`AsEnumerable()` prématuré rapatrie la table entière.
- Pagine systématiquement (`Skip`/`Take` ou pagination par curseur : `Where(x => x.Id > dernierId).Take(n)`) ; jamais de chargement non borné.
- Écritures en masse : `ExecuteUpdate`/`ExecuteDelete` (EF Core 7+) ou batch, pas d'aller-retour entité par entité ; `SaveChanges` par tranches pour les gros lots.

## Asynchronisme et réseau

- Async de bout en bout (`async`/`await`) pour tout I/O ; jamais de `.Result` ou `.Wait()` qui bloque un thread.
- `HttpClient` via `IHttpClientFactory` (réutilisation des connexions), jamais instancié par requête.
- Ne renvoie que les champs utiles au client (DTO dédiés) ; active la compression de réponse et les en-têtes de cache (`ResponseCache`, `ETag`).

## Mémoire et CPU

- Évite les allocations dans les chemins chauds : `StringBuilder` pour les concaténations répétées, `Span<T>`/`Memory<T>` pour le parsing intensif, attention aux captures de lambdas dans les boucles.
- LINQ : attention à l'énumération multiple d'un même `IEnumerable` (matérialise une fois si réutilisé) ; pas de `Count()` quand `Any()` suffit.
- Tout cache doit être borné et expirant (`IMemoryCache` avec `SizeLimit`/`AbsoluteExpiration`), jamais de dictionnaire statique qui grossit sans limite.
- Utilise `IAsyncEnumerable`/streaming pour les gros volumes plutôt que de tout charger en mémoire.

## Logs et tâches

- Logging structuré paramétré (`_logger.LogDebug("x={X}", x)`) avec niveaux de production sobres ; pas de log dans les boucles serrées.
- Pas de `BackgroundService` qui interroge un état en boucle rapprochée : préfère un déclenchement événementiel (message, webhook) ou espace les intervalles.
