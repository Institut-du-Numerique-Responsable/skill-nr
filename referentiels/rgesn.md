# RGESN : Référentiel général d'écoconception de services numériques (2024)

Source : [référentiel général d'écoconception des services numériques, version 2024](https://www.arcep.fr/uploads/tx_gspublication/referentiel_general_ecoconception_des_services_numeriques_version_2024.pdf)
(Arcep et Arcom, en coopération avec l'ADEME, avec des contributions de la DINUM, de la
CNIL et d'INRIA). Référentiel public de l'État français.

Extraction du 03/08/2026 depuis le PDF officiel, à partir des 78 fiches pratiques :
**78 critères, 9 thématiques**, extraction complète à ce niveau.

Ce fichier reprend l'identifiant et l'intitulé de chaque critère, rien de plus. Les
objectifs, mises en œuvre et moyens de test des fiches pratiques restent à consulter dans
le PDF source. Son rôle ici : permettre de **vérifier qu'un identifiant cité existe**.
`scripts/verifier-depot.sh` échoue si une règle cite un critère absent de ce fichier, au
même titre que pour GR491 et Opquast.

Le référentiel classe aussi chaque critère en « Prioritaire », « Recommandé » ou
« Modéré ». Ces niveaux ne sont pas repris ici : les tableaux de priorité du PDF sont sur
deux colonnes et leur extraction automatique s'est révélée non fiable (numéros migrant
d'une colonne à l'autre, un critère absent des trois tableaux alors que les totaux
annoncés le supposent présent). Plutôt que de publier une donnée dont une partie serait
fausse dans un fichier censé faire foi, la priorité est à lire dans le PDF.


## 1. Stratégie (10 critères)

- **RGESN 1.1** : Le service numérique a-t-il été évalué favorablement en termes d’utilité en tenant compte de ses impacts environnementaux ?
- **RGESN 1.2** : Le service numérique a-t-il défini ses cibles utilisatrices, les besoins métiers et les attentes réelles des utilisateurs-cibles ?
- **RGESN 1.3** : Le service numérique a-t-il au moins un référent identifié en écoconception numérique ?
- **RGESN 1.4** : Le service numérique réalise-t-il régulièrement des revues pour s’assurer du respect de sa démarche d’écoconception ?
- **RGESN 1.5** : Le service numérique s’est-il fixé des objectifs en matière de réduction ou de limitation de ses propres impacts environnementaux ?
- **RGESN 1.6** : Le service numérique collecte-t-il la donnée de façon responsable et raisonnée ?
- **RGESN 1.7** : Le service numérique a-t-il recours à un niveau de chiffrement adapté à ses besoins ?
- **RGESN 1.8** : Le service numérique a-t-il mis en place des efforts d’open source ?
- **RGESN 1.9** : Le service numérique a-t-il été conçu avec des technologies standard interopérables plutôt que des technologies spécifiques et fermées ?
- **RGESN 1.10** : Le service numérique repose-t-il sur des API documentées et ouvertes pour interagir avec le matériel ?

## 2. Spécifications (10 critères)

- **RGESN 2.1** : Le service numérique a-t-il défini la liste des profils de matériels que les utilisateurs vont pouvoir employer pour y accéder ?
- **RGESN 2.2** : Le service numérique est-il utilisable sur d’anciens modèles de terminaux ?
- **RGESN 2.3** : Le service numérique est-il utilisable via une connexion bas débit ou hors connexion ?
- **RGESN 2.4** : Le service numérique est-il utilisable sur d’anciennes versions de système d’exploitation et de navigateurs web ?
- **RGESN 2.5** : Le service numérique s’adapte-t-il à différents types de terminaux d’affichage ?
- **RGESN 2.6** : Le service numérique a-t-il été conçu avec une revue de conception et une revue de code comprenant parmi ses objectifs la réduction des impacts environnementaux de chaque fonctionnalité ?
- **RGESN 2.7** : Le service numérique a-t-il prévu une stratégie de maintenance et de décommissionnement ?
- **RGESN 2.8** : Le service numérique impose-t-il à ses fournisseurs de garantir une démarche de réduction de leurs impacts environnementaux ?
- **RGESN 2.9** : Le service numérique a-t-il pris en compte les impacts environnementaux des composants d’interface prêts à l’emploi utilisés ?
- **RGESN 2.10** : Le service numérique a-t-il pris en compte les impacts environnementaux des services tiers utilisés lors de leur sélection ?

## 3. Architecture (7 critères)

- **RGESN 3.1** : Le service numérique repose-t-il sur une architecture, des ressources ou des composants conçus pour réduire leurs propres impacts environnementaux ?
- **RGESN 3.2** : Le service numérique fonctionne-t-il sur une architecture pouvant adapter la quantité de ressources utilisées à la consommation du service ?
- **RGESN 3.3** : Le service numérique est-il en mesure de supporter l’évolution technique des protocoles ?
- **RGESN 3.4** : Le service numérique garantit-il la mise à disposition de mises à jour correctives pendant toute la durée de vie prévue des équipements et des logiciels liés au service ?
- **RGESN 3.5** : Le service numérique propose-t-il d’installer des mises à jour correctives indépendamment des mises à jour évolutives de façon transparente ?
- **RGESN 3.6** : Le service numérique propose-t-il les mises à jour incrémentielles, afin de ne pas remplacer tout le code à chaque mise à jour ?
- **RGESN 3.7** : Le service numérique optimise-t-il la sollicitation des environnements de développement, de préproduction ou de test en fonction de ses besoins ?

## 4. Expérience et interface utilisateur (UX/UI) (15 critères)

- **RGESN 4.1** : Le service numérique comporte-t-il uniquement des animations, vidéos et sons dont la lecture automatique est désactivée ?
- **RGESN 4.2** : Le service numérique affiche-t-il uniquement des contenus sans défilement infini ?
- **RGESN 4.3** : Le service numérique optimise-t-il le parcours de navigation pour chaque fonctionnalité principale ?
- **RGESN 4.4** : Le service numérique permet-il à l’utilisateur de décider de l’activation d’un service tiers ?
- **RGESN 4.5** : Le service numérique utilise-t-il majoritairement des composants fonctionnels natifs du système d’exploitation, du navigateur ou du langage utilisé ?
- **RGESN 4.6** : Le service numérique utilise-t-il uniquement du contenu vidéo, audio et animé porteur d’informations ?
- **RGESN 4.7** : Le service numérique opte-t-il pour les choix les plus sobres entre le texte, l’image, l’audio ou la vidéo, selon les besoins utilisateurs ?
- **RGESN 4.8** : Le service numérique limite-t-il le nombre des polices de caractères téléchargées ?
- **RGESN 4.9** : Le service numérique limite-t-il les requêtes serveur lors de la saisie utilisateur ?
- **RGESN 4.10** : Le service numérique informe-t-il l’utilisateur du format de saisie attendu, en évitant les requêtes serveur inutiles pour la soumission d’un formulaire ?
- **RGESN 4.11** : Le service numérique informe-t-il l’utilisateur, avant le transfert, des poids et formats de fichier attendus ?
- **RGESN 4.12** : Le service numérique indique-t-il à l’utilisateur que l’utilisation d’une fonctionnalité a des impacts environnementaux importants ?
- **RGESN 4.13** : Le service numérique limite-t-il le recours aux notifications, tout en laissant la possibilité à l’utilisateur de les désactiver ?
- **RGESN 4.14** : Le service numérique évite-t-il le recours à des procédés manipulatoires dans son interface utilisateur ?
- **RGESN 4.15** : Le service numérique fournit-il à l’utilisateur un moyen de contrôle sur ses usages afin de suivre et de réduire les impacts environnementaux associés ?

## 5. Contenus (8 critères)

- **RGESN 5.1** : Le service numérique utilise-t-il un format de fichier adapté au contenu et au contexte de visualisation de chaque image ?
- **RGESN 5.2** : Le service numérique propose-t-il des images dont le niveau de compression est adapté au contenu et au contexte de visualisation ?
- **RGESN 5.3** : Le service numérique utilise-t-il, pour chaque vidéo, une définition adaptée au contenu et au contexte de visualisation ?
- **RGESN 5.4** : Le service numérique propose-t-il des vidéos dont le mode de compression est efficace et adapté au contenu et au contexte de visualisation ?
- **RGESN 5.5** : Le service numérique propose-t-il un mode « écoute seule » pour ses vidéos ?
- **RGESN 5.6** : Le service numérique propose-t-il des contenus audios dont le mode de compression est adapté au contenu et au contexte d’écoute ?
- **RGESN 5.7** : Le service numérique utilise-t-il un format de fichier adapté au contenu et au contexte d’utilisation pour chaque document ?
- **RGESN 5.8** : Le service numérique a-t-il une stratégie d’archivage et de suppression, automatique ou manuelle, des contenus obsolètes ou périmés ?

## 6. Frontend (7 critères)

- **RGESN 6.1** : Le service numérique s’astreint-il à un poids maximum et une limite de requête par écran ?
- **RGESN 6.2** : Le service numérique utilise-t-il des mécanismes de mise en cache pour la totalité des contenus transférés dont il a le contrôle ?
- **RGESN 6.3** : Le service numérique a-t-il mis en place des techniques de compression pour les ressources transférées dont il a le contrôle ?
- **RGESN 6.4** : Le service numérique affiche-t-il majoritairement des images dont les dimensions d’origine correspondent aux dimensions du contexte d’affichage ?
- **RGESN 6.5** : Le service numérique évite-t-il de déclencher le chargement de ressources et de contenus inutilisés pour chaque fonctionnalité ?
- **RGESN 6.6** : Le service numérique restreint-il l’usage des capteurs des terminaux utilisateurs au besoin du service ?
- **RGESN 6.7** : Le service numérique héberge-t-il toutes les ressources statiques transférées dont il est l’émetteur sur un même domaine ?

## 7. Backend (4 critères)

- **RGESN 7.1** : Le service numérique a-t-il recours à un système de cache serveur pour les données les plus utilisées ?
- **RGESN 7.2** : Le service numérique met-il en place des durées de conservation sur les données et documents en vue de leur suppression ou archivage passé ce délai ?
- **RGESN 7.3** : Le service numérique informe-t-il l’utilisateur d’un traitement en cours en arrière-plan ?
- **RGESN 7.4** : Le service numérique s’appuie-t-il sur un mécanisme de consensus qui minimise sa consommation de ressources ?

## 8. Hébergement (10 critères)

- **RGESN 8.1** : Le service numérique utilise-t-il un hébergement ayant une démarche de réduction de son empreinte environnementale ?
- **RGESN 8.2** : Le service numérique utilise-t-il un hébergement qui fournit une politique de gestion durable des équipements ?
- **RGESN 8.3** : Le service numérique utilise-t-il un hébergement dont le PUE (Power Usage Effectiveness) est minimisé ?
- **RGESN 8.4** : Le service numérique utilise-t-il un hébergement dont son WUE (Water Usage Effectiveness) est minimisé ?
- **RGESN 8.5** : Le service numérique utilise-t-il un hébergement dont l’origine de consommation d’électricité est documentée et majoritairement d’origine renouvelable ?
- **RGESN 8.6** : Le service numérique utilise-t-il un hébergement dont la localisation géographique est cohérente avec ses activités et qui minimise son empreinte environnementale ?
- **RGESN 8.7** : Le service numérique utilise-t-il un hébergement qui traite efficacement la chaleur produite par les serveurs ?
- **RGESN 8.8** : Le service numérique héberge-t-il de façon distincte les données « chaudes » et « froides » ?
- **RGESN 8.9** : Le service numérique duplique-t-il les données uniquement lorsque cela est nécessaire ?
- **RGESN 8.10** : Le service numérique tient-il compte des contraintes externes pour minimiser l’impact environnemental des calculs et transferts de données asynchrones ?

## 9. Algorithmie (7 critères)

- **RGESN 9.1** : Le service numérique a-t-il interrogé la nécessité d’une phase d’entraînement pour éviter un usage non justifié et déraisonné ?
- **RGESN 9.2** : Le service numérique utilise-t-il une phase d’apprentissage avec un niveau de complexité minimisé et proportionné à l’usage effectif du service ?
- **RGESN 9.3** : Le service numérique a-t-il mis en place des mécanismes visant à limiter la quantité d’entraînement nécessaire à son fonctionnement ?
- **RGESN 9.4** : Le service numérique limite-il la quantité de données utilisées pour la phase d’apprentissage au strict nécessaire ?
- **RGESN 9.5** : Le service numérique optimise-t-il l’occurrence de mise à jour et de réentraînement des modèles en fonction de ses besoins et des cibles utilisatrices ?
- **RGESN 9.6** : Le service numérique utilise-t-il des techniques de compression pour les modèles utilisés lors de la phase d’entraînement ?
- **RGESN 9.7** : Le service numérique utilise-t-il une stratégie d’inférence optimisée en termes de consommation de ressources et des cibles utilisatrices ?
