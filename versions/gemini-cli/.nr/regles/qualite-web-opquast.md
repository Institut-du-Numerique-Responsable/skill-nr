<!-- Fichier généré par scripts/generer-versions.py, ne pas éditer à la main.
     Source : .continue/rules/ -->

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
