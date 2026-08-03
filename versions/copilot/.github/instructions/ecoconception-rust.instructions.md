---
applyTo: "**/*.rs"
description: Règles d'écoconception pour le code Rust, allocations maîtrisées, itérateurs, async non bloquant
---

<!-- Fichier généré par scripts/generer-versions.py, ne pas éditer à la main.
     Source : .continue/rules/ -->

# Règles d'écoconception : Rust

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
