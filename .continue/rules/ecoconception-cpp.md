---
name: Écoconception C++
description: Règles d'écoconception pour le code C++ — copies évitées, conteneurs adaptés, RAII
globs: "**/*.{cpp,cc,cxx,hpp,hh}"
---

# Règles d'écoconception — C++

Applique ces règles à tout code C++ que tu écris ou modifies. Références : RGESN v2 (Backend, Algorithmie) et GR491 (GR491_Backend_4 — voir `referentiels/gr491.md`).

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
