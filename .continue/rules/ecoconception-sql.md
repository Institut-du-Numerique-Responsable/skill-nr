---
name: Écoconception SQL
description: Règles d'écoconception pour les requêtes et scripts SQL — sobriété des lectures, index, pagination, cycle de vie des données
globs: "**/*.sql"
---

# Règles d'écoconception — SQL

Applique ces règles à tout SQL que tu écris ou modifies (requêtes, procédures stockées, migrations). Références : RGESN v2 (Backend, Architecture) et GR491 (GR491_Backend_1, GR491_Architecture_3/5 — voir `referentiels/gr491.md`).

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

## Cycle de vie des données

- Toute nouvelle table ou colonne doit avoir une raison d'être : pas de champ « au cas où », pas de duplication de données existantes.
- Prévois dès la création la politique de rétention/purge (RGESN : maîtrise du cycle de vie) ; propose partitionnement ou archivage pour les tables à forte croissance.
- Choisis les types les plus compacts adaptés au besoin (pas de `VARCHAR(MAX)`/`TEXT` par défaut, pas de `BIGINT` si `INT` suffit).
