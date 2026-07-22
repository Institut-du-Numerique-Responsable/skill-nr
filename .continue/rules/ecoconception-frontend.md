---
name: Écoconception frontend
description: Règles d'écoconception pour le code frontend (HTML, CSS, JS, images), alignées sur le RGESN et le GR491
globs: "**/*.{html,css,scss,js,jsx,ts,tsx,vue,svelte}"
---

# Règles d'écoconception : Frontend

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
