---
name: Écoconception JavaScript/TypeScript
description: Règles d'écoconception pour le code JavaScript et TypeScript, navigateur comme Node.js
globs: "**/*.{js,jsx,ts,tsx,mjs,cjs}"
---

# Règles d'écoconception : JavaScript / TypeScript

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
