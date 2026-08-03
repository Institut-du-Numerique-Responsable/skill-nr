# Écarts attendus dans les fichiers de test

Les deux fichiers `exemple-a-corriger.html` et `exemple-a-corriger.sql` contiennent des
écarts volontaires. Ils servent à vérifier qu'un assistant IA a bien chargé les règles
de ce dépôt : un assistant qui n'a rien chargé passera à côté de la plupart d'entre eux,
ou les signalera sans jamais citer de critère.

Les deux fichiers totalisent **18 écarts**, 13 côté HTML et 5 côté SQL.

Barème indicatif : **10 écarts sur 18 relevés, avec au moins 3 critères cités**
(RGESN, GR491, Opquast ou RGAA), c'est une installation qui fonctionne. En dessous de 5,
les règles ne sont pas chargées, reprenez l'installation.

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
