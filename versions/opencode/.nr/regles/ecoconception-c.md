<!-- Fichier généré par scripts/generer-versions.py, ne pas éditer à la main.
     Source : .continue/rules/ -->

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
