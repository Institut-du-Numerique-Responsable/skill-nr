# Écarts attendus dans les fichiers de test

Les deux fichiers `exemple-a-corriger.html` et `exemple-a-corriger.sql` contiennent des
écarts volontaires. Ils servent à vérifier qu'un assistant IA a bien chargé les règles
de ce dépôt : un assistant qui n'a rien chargé passera à côté de la plupart d'entre eux,
ou les signalera sans jamais citer de critère.

Les deux fichiers totalisent **18 écarts**, 13 côté HTML et 5 côté SQL.

## Barème, calé sur des mesures

Deux passages sur ce corpus, mesurés le 03/08/2026 :

| Source | Écarts détectés | Tracés au bon critère | Identifiants inventés |
| --- | --- | --- | --- |
| Modèle local (qwen3-coder via Continue, règles chargées) | 16/18 | 1/18 | 1 inventé : `RGESN 6.8` |
| Pré-filtre déterministe `scripts/eco-audit.sh` | 12/18 | 12/18 | 0 |

**Repère : 12 écarts sur 18.** Au-dessus, les règles sont chargées. En dessous de 5,
elles ne le sont pas, reprenez l'installation.

Ce que ces mesures ont changé : le barème reposait au départ sur « au moins 3 critères
cités ». Le modèle en a cité 13, dont un qui **n'existe pas** : la thématique 6 du RGESN
compte 7 critères, il a écrit `RGESN 6.8`, avec des intitulés inventés pour les autres.
Une citation ne prouve donc rien par elle-même. `scripts/scorer-detection.py` vérifie
désormais chaque identifiant contre `referentiels/` et signale les inventés.

C'est aussi le partage des rôles entre les deux étages : le modèle voit plus de choses
(16 contre 12), le pré-filtre les rattache correctement (12 contre 1). L'un sans l'autre
est incomplet.

Attention si vous testez depuis ce dépôt : donner le corpus à un assistant qui a accès à
`verification/` lui donne aussi ce fichier, donc les réponses. Le premier passage mesuré
ici l'a montré, 18/18 avec des formulations reprises mot pour mot. Testez dans un dossier
isolé contenant les règles et les deux fichiers pièges, rien d'autre.

Ne corrigez pas ces fichiers dans ce dépôt. Si votre assistant applique les correctifs
directement (c'est le cas de `cn review` et des agents en mode écriture), annulez ensuite
avec `git checkout -- verification/`.

## exemple-a-corriger.html

| # | Écart | Critères |
| --- | --- | --- |
| 1 | Image sans `alt` (contenu porteur de sens, non décoratif) | RGAA 1.1 |
| 2 | Image sans `loading="lazy"`, sans `width`/`height`, sans `srcset` ni format moderne | GR491_UXUI_8, GR491_Contenus_2 |
| 3 | Image servie en 4000x3000 puis redimensionnée par le navigateur | Opquast n°119 |
| 4 | Vidéo en `autoplay` et en boucle | Opquast n°124, GR491_Contenus_3 |
| 5 | Iframe YouTube chargée dès l'ouverture de la page, sans façade cliquable | GR491_Frontend_9, GR491_Contenus_3 |
| 6 | Tableau de données simulé en `div` | Opquast n°245, RGAA 5.x |
| 7 | Framework CSS complet et police distante multi-graisses pour deux composants | GR491_Frontend_9, GR491_UXUI_8 |
| 8 | `div` cliquable au lieu d'un `button` : inatteignable au clavier | RGAA 7.1, GR491_UXUI_4 |
| 9 | Champ de formulaire sans `label` associé (`placeholder` seul) | RGAA 11.1 |
| 10 | Contraste insuffisant (#b9b9b9 sur #ffffff, ratio ≈ 1,9:1) | RGAA 3.2 |
| 11 | jQuery et lodash ajoutés là où les API natives suffisent | GR491_Frontend_9, GR491_Backend_2 |
| 12 | Polling toutes les 3 secondes au lieu d'un rafraîchissement à la demande | GR491_Frontend_10, GR491_Backend_3 |
| 13 | Structure sans balises sémantiques ni hiérarchie de titres (`div` partout) | RGAA 9.1, GR491_Frontend_5 |

## exemple-a-corriger.sql

| # | Écart | Critères |
| --- | --- | --- |
| 14 | `SELECT *` sur une jointure à trois tables, sans projection des colonnes utiles | GR491_Backend_3 |
| 15 | Aucune pagination sur un volume non borné | GR491_Backend_1 |
| 16 | Prédicats non sargables : `UPPER(c.nom)`, `LIKE '%...'`, `YEAR(cmd.date_creation)` | GR491_Backend_4 |
| 17 | Nouvelle table de journalisation sans politique de rétention ni purge | GR491_Backend_1, RGESN (données) |
| 18 | Collecte d'IP et de user-agent sans nécessité démontrée | GR491_Backend_5, RGPD art. 5 |

Un assistant correctement configuré relève typiquement les écarts 1, 4, 5, 8, 9, 11, 12,
14, 15 et 17 dès le premier passage. Les écarts 3, 10 et 16 demandent une lecture plus
fine et sont un bon signe de qualité du modèle utilisé, pas de la qualité de
l'installation.
