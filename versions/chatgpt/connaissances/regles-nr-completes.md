<!-- Fichier généré par scripts/generer-versions.py, ne pas éditer à la main.
     Source : .continue/rules/ -->

# Règles Numérique Responsable : écoconception et accessibilité

Ces règles s'appliquent à tout code que tu écris ou modifies dans ce projet.
Chaque section « S'applique aux fichiers » ne concerne que les fichiers de son
langage : applique-la quand tu travailles sur ce type de fichier, ignore-la sinon.
Cite le critère source (RGESN x.x, GR491_xxx, Opquast n°xxx) quand tu appliques
une règle, pour la montée en compétence de l'équipe.

Référentiels : RGESN v2 (ARCEP/ARCOM/ADEME), GR491 (INR), Opquast (CC BY-SA), RGAA 4.

# Principes de numérique responsable (transverses)

Ces principes s'appliquent à toute contribution, quel que soit le langage ou la couche technique.

## Accessibilité (RGAA / WCAG)

- Tout HTML produit doit être sémantique (balises appropriées, hiérarchie de titres cohérente, `alt` pertinents, labels de formulaires associés).
- Contraste suffisant, navigation clavier complète, focus visible, pas d'information portée uniquement par la couleur.
- Vise la conformité RGAA 4 ; signale tout écart que tu ne peux pas corriger dans le périmètre de la tâche.

## Durabilité et pérennité

- Compatibilité large : le service doit fonctionner sur des appareils anciens et des connexions lentes (RGESN : ne pas contribuer à l'obsolescence des terminaux).
- Prévois une dégradation gracieuse quand une fonctionnalité avancée n'est pas disponible.
- Documente ce que tu produis pour en permettre la maintenance (README, commentaires sur les contraintes non évidentes).

## Protection des données et sobriété des collectes

- Minimisation : ne collecte et ne conserve que les données strictement nécessaires à la fonctionnalité (RGPD, article 5).
- Pas de traceur ou de mesure d'audience ajouté sans demande explicite et sans base légale identifiée.
- Aucun secret (clé, jeton, mot de passe) en dur dans le code ou les fichiers versionnés.

## Posture de l'assistant

- Quand une demande entre en tension avec ces principes (fonctionnalité superflue, collecte excessive, dépendance lourde), réalise la tâche demandée si elle est légitime mais mentionne explicitement la tension et propose une alternative plus sobre.
- Dans tes réponses, cite le critère concerné quand tu appliques une règle (ex. « RGESN 4.x », « RGAA 10.x ») pour faciliter la montée en compétence de l'équipe.

---

# Usage sobre de l'assistant IA

La sobriété numérique ne s'arrête pas au code produit : la session avec l'assistant a
elle-même un coût en calcul. Le contexte envoyé au modèle est retraité à chaque tour de
conversation. Un contexte obèse ou une conversation-fleuve multiplie ce coût sur tous
les échanges suivants, pas seulement le dernier. Applique ces pratiques à ta propre
conduite de session, pas seulement au code que tu écris.

## Contexte minimal

- Ne charge pas un fichier entier dans le contexte si tu peux le lire à la demande au
  moment où tu en as besoin. Préfère un objectif clair et une capacité à aller chercher
  l'information plutôt qu'un contexte pré-rempli exhaustif.
- Ne relis pas un fichier déjà lu dans la session sauf s'il a pu changer entre-temps.
- Un index du dépôt (type `CODEMAP.md`) évite de redécouvrir la structure du projet à
  chaque session : consulte-le d'abord, ne recartographie pas le code inutilement.

## Corriger sans polluer

- Quand une tentative échoue, ne l'empile pas dans l'historique en enchaînant les
  messages de correction : chaque essai raté reste dans le contexte et est retraité à
  chaque tour suivant. Reviens avant l'erreur si l'outil le permet (rewind, nouvelle
  branche de conversation) plutôt que de corriger par-dessus.
- Pour une tâche sans lien avec ce qui précède, démarre un contexte propre plutôt que de
  poursuivre une conversation déjà longue. Pour une tâche liée, résume l'historique avec
  une consigne ciblée (ce qu'il faut garder, ce qu'il faut jeter) plutôt que de tout
  conserver tel quel.

## Capitaliser plutôt que répéter

- Une leçon apprise en session (une convention, une erreur récurrente, une contrainte du
  projet) se documente dans un fichier de règles versionné. La corriger seulement dans
  la conversation en cours la reperd à la prochaine session.
- Donne-toi un moyen de vérification déterministe (tests, build, commande) plutôt que de
  multiplier les tours de relecture manuelle : une vérification automatisée coûte moins
  cher qu'un aller-retour de plus avec le modèle.

## Proportionner la puissance à la tâche

- N'utilise pas systématiquement le modèle ou le niveau de raisonnement le plus élevé
  disponible : proportionne l'effort à la complexité réelle de la tâche. Un modèle plus
  petit bien choisi consomme un ordre de grandeur de moins pour un résultat équivalent
  sur une tâche simple.
- Pour l'automatisation récurrente (CI, scripts), démarre sans contexte projet superflu
  et mets en cache les réponses à des requêtes identiques quand c'est possible.

## Repères par outil

Les mécanismes exacts diffèrent selon l'assistant utilisé ; le principe (contexte propre,
pas de correction empilée, effort proportionné) reste le même partout.

- **Continue (`cn`)** : `--resume` reprend la dernière session, `--fork <id>` repart
  d'un point antérieur sans réembarquer les tours suivants ; `ls` liste les sessions.
- **Claude Code** : rembobiner avec un double appui sur Échap, `/clear` pour une tâche
  sans lien, `/compact <consigne>` pour résumer une tâche liée, `/effort` pour ajuster
  le niveau de raisonnement.
- **Gemini CLI, OpenCode, Mistral Vibe, ChatGPT** : vérifie la commande équivalente de
  gestion de session/contexte dans la documentation de l'outil ; le principe ci-dessus
  s'applique quel que soit son nom exact.

---

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

---

# Règles d'écoconception : Frontend

> S'applique aux fichiers : `**/*.{html,css,scss,js,jsx,ts,tsx,vue,svelte}`

Applique ces règles à tout code frontend que tu écris ou modifies. Références : RGESN v2 (thématiques UX/UI, Contenus, Frontend) et GR491 (GR491_Frontend_4/5/9/10, GR491_Contenus_2/3, GR491_UXUI_5/8, voir `referentiels/gr491.md`).

## Poids et requêtes

- Minimise le poids total de chaque page : vise < 500 Ko transférés et < 25 requêtes HTTP par écran.
- N'ajoute jamais une dépendance (librairie, framework, polyfill) si une API native du navigateur suffit. Justifie toute nouvelle dépendance dans le message de commit.
- Préfère l'import ciblé (`import { x } from 'lib/x'`) à l'import global. Vérifie que le tree-shaking est effectif.
- Charge les scripts non critiques en `defer` ou `async`, et les modules lourds en import dynamique (lazy loading).

## Images et médias

- Utilise des formats modernes (AVIF, WebP) avec repli, `srcset`/`sizes` pour les images responsives, et `loading="lazy"` hors du viewport initial.
- Jamais de vidéo en lecture automatique. Toujours une affiche (`poster`) et un chargement à la demande.
- Préfère SVG ou CSS aux images matricielles pour les icônes et décorations.

## HTML et DOM

- HTML sémantique et minimal : pas de `div` d'enrobage sans rôle, vise un DOM peu profond (au-delà de ~1 500 nœuds ou 32 niveaux, restructure).
- De vrais éléments natifs (`button`, `a`, `details`, `dialog`, `select`) plutôt que des reconstructions en `div` + JS : moins de code, accessible d'office (Opquast n°245 pour les tableaux).
- Les `iframe` et widgets tiers (cartes, vidéos, réseaux sociaux) se chargent à la demande (façade cliquable), jamais au chargement initial.
- Renseigne `width`/`height` sur images et médias pour éviter les recalculs de mise en page (layout shifts).

## CSS et polices

- Maximum 2 familles de polices, formats WOFF2 uniquement, `font-display: swap`, sous-ensembles de caractères (subsetting) quand c'est possible. Préfère les polices système.
- CSS livré minimal : pas de framework CSS entier pour quelques composants (purge/extraction du CSS réellement utilisé), pas de `@import` en cascade dans les feuilles.
- Anime uniquement `transform` et `opacity` (composées par le GPU), jamais des propriétés de layout (`top`, `width`…) ; `will-change` avec parcimonie.
- Évite les animations continues (GIF animés, boucles CSS infinies) ; respecte `prefers-reduced-motion`.
- Prévois des styles d'impression sobres (Opquast n°195-196 : contenu imprimable sans blocs de navigation).

## Rendu et exécution

- Évite le re-rendu inutile : mémoïsation ciblée, pagination ou virtualisation des longues listes (jamais de scroll infini par défaut, RGESN recommandant la pagination).
- Débounce/throttle les gestionnaires d'événements coûteux (scroll, resize, input).
- Pas de polling : préfère les WebSockets ou Server-Sent Events si un rafraîchissement est réellement nécessaire, sinon un rafraîchissement manuel.
- Mets en cache les réponses réseau (HTTP cache, service worker) avec une politique explicite.

## Sobriété fonctionnelle

- Avant d'ajouter un composant ou une fonctionnalité, questionne son utilité pour l'utilisateur final. Signale dans ta réponse toute demande qui semble ajouter une fonctionnalité non essentielle.
- Supprime le code mort et les dépendances inutilisées que tu rencontres.

---

# Qualité web : règles Opquast × écoconception

> S'applique aux fichiers : `**/*.{html,css,scss,js,jsx,ts,tsx,vue,svelte,cshtml,jsp,twig,razor}`

Applique ces règles (checklist Opquast, licence CC BY-SA) à tout code web produit ou modifié. Cite le numéro de règle Opquast quand tu l'appliques. Liste complète : `referentiels/opquast-ecoconception.md`.

## Images et médias

- Les vignettes et aperçus sont servis à leur taille d'affichage, jamais une grande image redimensionnée côté client (n°119).
- Vidéos et sons sont déclenchés par l'utilisateur, jamais automatiquement (n°124, 125).
- Chaque contenu audio/vidéo est accompagné de sa transcription textuelle et sa durée est indiquée (n°121, 123).
- Un texte stylable en CSS n'est jamais remplacé par une image (n°187).

## Liens et téléchargements

- Tout lien de téléchargement interne indique le format et la taille du fichier (n°147, 148), et sa langue si elle diffère de la page (n°149).
- Les liens de même nature gardent apparence et comportement identiques sur toutes les pages (n°138).
- La navigation ne provoque pas l'ouverture de popups (n°154).

## Serveur, build et performances

- Les réponses sont compressées (gzip/brotli) et portent des en-têtes de mise en cache (n°226, 227).
- CSS et scripts internes sont minifiés en production (n°229, 230).
- Une ressource absente renvoie un vrai code HTTP 404, jamais une page 200 « non trouvé » (n°222).
- Le site expose robots.txt et sitemap (n°219, 220) et répond avec et sans préfixe www (n°218).

## Structure, formulaires et parcours

- Les tableaux de données utilisent de vraies balises `<table>`, jamais une simulation en `div`/CSS, et réciproquement, pas de `<table>` pour la mise en page (n°245).
- Les pages de résultats de recherche sont adressables par URL et permettent de relancer la recherche (n°169, 170).
- Un processus complexe annonce dès le début les données et documents exigés (n°86).
- La désinscription d'une newsletter est immédiate, sans confirmation par courriel (n°175) ; un compte créé en ligne peut être fermé par le même moyen (n°20).

---

# Règles d'écoconception : SQL et PL/SQL

> S'applique aux fichiers : `**/*.{sql,pks,pkb,prc,fnc,trg}`

Applique ces règles à tout SQL que tu écris ou modifies (requêtes, procédures stockées, migrations). Références : RGESN v2 (Backend, Architecture) et GR491 (GR491_Backend_1, GR491_Architecture_3/5, voir `referentiels/gr491.md`).

## Lectures sobres

- Jamais de `SELECT *` : liste explicitement les colonnes nécessaires au besoin.
- Pagine toute requête pouvant renvoyer un volume non borné. Préfère la pagination par curseur/keyset (`WHERE id > :dernier_id ORDER BY id LIMIT n`) à `OFFSET`, qui relit toutes les lignes ignorées.
- Filtre au plus tôt et côté base : pas de rapatriement de lignes pour filtrer ensuite dans l'applicatif.
- Préfère `EXISTS` à `IN (sous-requête)` sur de gros volumes ; méfie-toi d'un `DISTINCT` qui masque une jointure incorrecte.

## Index et plans d'exécution

- Toute clause `WHERE`, `JOIN` ou `ORDER BY` fréquente doit s'appuyer sur un index ; signale explicitement les requêtes qui provoqueraient un parcours complet (full scan) sur une table volumineuse.
- Écris des prédicats « sargables » : pas de fonction sur la colonne indexée (`WHERE UPPER(nom) = ...`, `WHERE DATE(created_at) = ...`), pas de `LIKE '%...'` avec joker en tête.
- N'ajoute pas d'index en double ou sur des tables très écrites sans le justifier : un index a un coût à chaque écriture.

## Écritures et traitements

- Traite en ensembliste, pas ligne à ligne : pas de curseur ou de boucle quand un `UPDATE ... WHERE`, un `INSERT ... SELECT` ou un `MERGE` suffit.
- Regroupe les insertions en lots (batch/multi-valeurs) ; borne les transactions (pas de transaction longue tenant des verrous).
- Les purges et migrations sur de gros volumes se font par tranches (chunks) avec pauses, jamais en un seul ordre massif.

## Spécifique PL/SQL (Oracle)

- Minimise les bascules de contexte SQL ↔ PL/SQL : traite en un seul ordre SQL quand c'est possible ; sinon `BULK COLLECT` (avec `LIMIT`) et `FORALL`, jamais de boucle `FOR ... LOOP` qui exécute un ordre par ligne.
- Pas de fonction PL/SQL appelée dans un prédicat `WHERE` sur chaque ligne d'une grande table (elle interdit l'index et multiplie les bascules) ; matérialise ou réécris en SQL pur.
- `COMMIT` par lots dimensionnés, pas à chaque ligne (coût de journalisation) ni en une transaction géante (undo, verrous).
- Curseurs explicites uniquement quand le traitement ligne à ligne est inévitable ; ferme-les systématiquement.
- Pas de `DBMS_OUTPUT` ni de journalisation ligne à ligne dans les boucles de production.

## Cycle de vie des données

- Toute nouvelle table ou colonne doit avoir une raison d'être : pas de champ « au cas où », pas de duplication de données existantes.
- Prévois dès la création la politique de rétention/purge (RGESN : maîtrise du cycle de vie) ; propose partitionnement ou archivage pour les tables à forte croissance.
- Choisis les types les plus compacts adaptés au besoin (pas de `VARCHAR(MAX)`/`TEXT` par défaut, pas de `BIGINT` si `INT` suffit).

---

# Règles d'écoconception : JavaScript / TypeScript

> S'applique aux fichiers : `**/*.{js,jsx,ts,tsx,mjs,cjs}`

Applique ces règles à tout code JS/TS que tu écris ou modifies, côté navigateur comme côté Node.js. Complète `ecoconception-frontend` (plateforme web) pour les fichiers d'interface. Références : RGESN v2 (Frontend, Backend, Algorithmie) et GR491 (GR491_Frontend_9/10, GR491_Backend_4, voir `referentiels/gr491.md`).

## Dépendances

- API natives d'abord : `fetch`, `Intl`, `URL`, `crypto`, `structuredClone`, `Array`/`Object` modernes : n'ajoute une librairie que si le natif ne suffit pas, et justifie-la.
- Imports ciblés (`import { x } from 'lib/x'`) pour préserver le tree-shaking ; surveille le poids ajouté au bundle ou à `node_modules`.

## Exécution

- Ne bloque jamais le thread principal ni l'event loop : pas d'API synchrone (`fs.*Sync`, `JSON.parse` de payloads géants) sur un chemin de requête ou d'interaction ; déporte le calcul lourd (`worker_threads`, Web Worker).
- Pas de polling (`setInterval` + requête) : préfère SSE/WebSocket si le rafraîchissement est réellement nécessaire, sinon une action utilisateur.
- Débounce/throttle les gestionnaires coûteux ; regroupe les manipulations du DOM hors des boucles.
- Pas de motif quadratique sur des collections non bornées : `Map`/`Set` pour les recherches, pas `Array.includes`/`find` répétés.

## Données et flux

- Streame les gros volumes (`stream`/`pipeline` côté Node, `ReadableStream` côté navigateur) au lieu de tout charger en mémoire.
- Pagine toute réponse d'API ; mets en cache les réponses répétitives avec une politique explicite (TTL, invalidation).
- Réutilise les connexions sortantes (agent keep-alive, client HTTP partagé) et les pools de base de données.
- Attention aux fuites : pas de grandes structures retenues par des closures ou des listeners jamais détachés ; caches bornés (taille max + expiration), `WeakMap` pour les associations à des objets.

## TypeScript

- Les types disparaissent à l'exécution : ne duplique pas en runtime ce que le compilateur garantit déjà (validations redondantes), mais valide bien les entrées externes (une seule fois, en bordure).

---

# Règles d'écoconception : Java

> S'applique aux fichiers : `**/*.java`

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

---

# Règles d'écoconception : C# / .NET

> S'applique aux fichiers : `**/*.cs`

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

---

# Règles d'écoconception : Python

> S'applique aux fichiers : `**/*.py`

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

---

# Règles d'écoconception : PHP

> S'applique aux fichiers : `**/*.php`

Applique ces règles à tout code PHP que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_2/3/4, voir `referentiels/gr491.md`).

## Accès aux données (Doctrine / Eloquent / PDO)

- Traque le N+1 : `with()` (Eloquent) ou jointures/`fetch join` (Doctrine) sur les associations parcourues, jamais de lazy loading en boucle.
- Projette les colonnes utiles (`select([...])`, DQL partiel) plutôt que des entités complètes hydratées.
- Gros volumes par lots : `chunk()`/`cursor()` (Eloquent), `iterate()`/`toIterable()` (Doctrine), jamais de `->get()`/`findAll()` sur une table non bornée ; pagine toute liste exposée.
- Écritures en masse : `insert()` multi-lignes, `upsert()`, pas de `save()` en boucle ; `exists()` plutôt que `count() > 0`.

## Mémoire et flux

- Générateurs (`yield`) pour produire et consommer de grandes séquences sans tableau intermédiaire.
- Fichiers lus en flux (`fopen` + lecture par blocs), jamais `file_get_contents` sur un gros fichier ; `fputcsv`/streams pour les exports.
- Recherche d'appartenance par clés de tableau (`isset($index[$k])`), pas `in_array` répété sur un grand tableau.

## Exécution et infrastructure

- OPcache activé en production ; autoload optimisé (`composer dump-autoload -o`) ; pas de dépendance Composer ajoutée quand une fonction native suffit.
- Réutilise les connexions : client HTTP partagé (Guzzle injecté), connexions PDO persistantes ou pool selon la plateforme.
- Tout cache est borné et expirant (APCu, Redis avec TTL), jamais de cache fichier qui grossit sans purge.
- Logging sobre en production : pas de log dans les boucles, niveaux INFO et au-dessus.

---

# Règles d'écoconception : Ruby / Rails

> S'applique aux fichiers : `**/*.rb`

Applique ces règles à tout code Ruby que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_2/3/4, voir `referentiels/gr491.md`).

## Accès aux données (ActiveRecord)

- Traque le N+1 : `includes`/`preload`/`eager_load` sur les associations parcourues, jamais de lazy loading en boucle.
- Projette les colonnes utiles : `select(:col1, :col2)`, `pluck(:col)` plutôt que `map(&:col)` sur des objets complets.
- Parcours de gros volumes par lots : `find_each`/`in_batches`, jamais de `.all.each` sur une table non bornée ; pagine toute liste exposée (pagy/kaminari).
- `exists?` plutôt que `any?`/`count > 0` (qui chargent ou comptent tout) ; `update_all`/`insert_all` pour les écritures en masse, pas de `save` en boucle.

## Mémoire et CPU

- Chaînes construites avec `<<` (mutation), pas `+=` en boucle ; symboles pour les clés.
- Énumérateurs paresseux (`.lazy`) et `each_slice` pour les longues chaînes de transformations ; ne matérialise pas de tableaux intermédiaires inutiles.
- Recherche d'appartenance dans un `Set` ou un hash, pas `include?` sur un grand tableau.
- Tout cache est borné et expirant (`Rails.cache` avec `expires_in`), jamais de constante/variable de classe qui accumule sans limite.

## Tâches et I/O

- Jobs d'arrière-plan idempotents et par lots ; pas de job planifié à haute fréquence pour surveiller un état (préfère un déclenchement événementiel).
- Réutilise les connexions HTTP sortantes (client persistant) et le pool de connexions base.
- Logging sobre en production : pas de log dans les boucles serrées, niveaux INFO et au-dessus.

---

# Règles d'écoconception : Rust

> S'applique aux fichiers : `**/*.rs`

Applique ces règles à tout code Rust que tu écris ou modifies. Rust est déjà sobre par conception : l'enjeu est de ne pas gaspiller cet avantage. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_2/4, voir `referentiels/gr491.md`).

## Allocations et copies

- Pas de `clone()`/`to_owned()` de confort : emprunte (`&`) quand la possession n'est pas nécessaire ; `Cow<str>` pour les cas « parfois possédé ».
- Chaîne les itérateurs sans `collect()` intermédiaire ; ne matérialise un `Vec` que pour le résultat final, avec `with_capacity` quand la taille est connue.
- Expose `&str`/`&[T]` (ou `impl AsRef<str>`) dans les signatures plutôt que `String`/`Vec<T>` possédés.
- Réutilise les buffers dans les boucles chaudes (`clear()` + réemploi) au lieu de réallouer.

## Async et I/O

- Jamais de travail CPU long ni d'appel bloquant dans une tâche async : `spawn_blocking` ou thread dédié.
- Réutilise les clients réseau (`reqwest::Client` cloné, pools de connexions), jamais un client par requête.
- I/O bufferisées (`BufReader`/`BufWriter`) et streaming pour les gros volumes, jamais de lecture entière en mémoire quand un flux suffit.
- Canaux et caches bornés (`bounded`, taille max + expiration) pour éviter toute croissance mémoire non maîtrisée.

## Dépendances et build

- Sobriété du graphe de dépendances : justifie chaque crate ajoutée, désactive les features inutiles (`default-features = false`), vérifie avec `cargo tree`.
- Les binaires de production sont compilés en `--release` ; active LTO si le temps de build le permet.
- Pas de `unwrap()`/panique sur les chemins d'erreur attendus : une erreur gérée évite un redémarrage de service (et son coût).

---

# Règles d'écoconception : C

> S'applique aux fichiers : `**/*.{c,h}`

Applique ces règles à tout code C que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_4, voir `referentiels/gr491.md`).

## Mémoire

- Alloue au besoin réel et réutilise les buffers dans les boucles ; chaque `malloc` a un chemin de `free` identifié (y compris en cas d'erreur).
- Structures compactes : types dimensionnés au besoin, attention à l'alignement/padding sur les structures massivement instanciées.
- Pas de copie de grandes zones mémoire quand un pointeur ou un index suffit.

## CPU et algorithmie

- Pas de motif quadratique caché : `strlen()` hors de la condition de boucle, pas de `strcat()` répété (garde un pointeur de fin ou utilise `memcpy` avec offset).
- Structures et algorithmes adaptés au volume : table de hachage ou recherche dichotomique plutôt que balayage linéaire répété sur de grandes collections.
- Compile la production avec optimisations (`-O2`) ; mesure avant d'optimiser à la main.

## I/O et attente

- I/O bufferisées : jamais de lecture/écriture octet par octet ou d'appel système par petite unité ; regroupe (`fread`/`fwrite` par blocs, `writev`).
- Jamais d'attente active (busy-wait, boucle sur `sleep` court) : bloque sur `poll`/`epoll`/`select` ou une variable de condition.
- Ferme et libère systématiquement les ressources (descripteurs, handles) ; vérifie les codes retour pour éviter les fuites en chemin d'erreur.

---

# Règles d'écoconception : C++

> S'applique aux fichiers : `**/*.{cpp,cc,cxx,hpp,hh}`

Applique ces règles à tout code C++ que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_4, voir `referentiels/gr491.md`).

## Copies et allocations

- Passe les objets non triviaux par `const&` ; utilise la sémantique de déplacement (`std::move`) pour transférer la possession.
- Vues non possédantes pour lire sans copier : `std::string_view`, `std::span`.
- `reserve()` sur les `vector` dont la taille est prévisible ; `emplace_back` plutôt que `push_back` d'un temporaire.
- Réutilise les buffers dans les boucles chaudes (`clear()` conserve la capacité) au lieu de reconstruire.

## Conteneurs et algorithmie

- Conteneur adapté à l'accès : `unordered_map`/`unordered_set` pour les recherches fréquentes, jamais de `std::find` linéaire répété sur un grand `vector`.
- Pas de matérialisation intermédiaire inutile : algorithmes de la STL et ranges plutôt que des copies successives.
- `shared_ptr` seulement quand la possession est réellement partagée (le compteur atomique a un coût) ; `unique_ptr` par défaut, RAII partout.

## I/O et attente

- I/O bufferisées et par blocs ; streaming pour les gros volumes plutôt que chargement entier en mémoire.
- Jamais d'attente active : `condition_variable`, `poll`/`epoll` ou primitives async, pas de boucle de scrutation.
- Production compilée avec optimisations (`-O2`) ; mesure (profiling) avant toute optimisation manuelle.
