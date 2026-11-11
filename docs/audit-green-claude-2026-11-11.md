# Audit de skill-nr au regard de green-claude

Audit du 11 novembre 2026. Périmètre : dépôt `skill-nr`, générateur, règles sources, scripts, CI et lecture statique du site. Référence : skill green-claude 1.5.0 installé. Aucun correctif de code appliqué.

## Synchronisation GitHub

- **PASS** : `HEAD` local et `main` GitHub valent `01ff0f3f8157f1391bd8aefd6d552ab62674ca5f`. Arbre de travail propre avant audit. Vérification par l’API GitHub, sans se fier à une référence distante locale potentiellement ancienne.
- **PASS** : les déclinaisons générées correspondent aux sources `.continue/` après exécution du générateur.
- La dernière release de skill-nr est `v1.0.0`, publiée le 28 août 2026. `main` contient trois commits supplémentaires. Le clone est à jour ; la release ne contient pas encore ces évolutions de documentation et de vérification.
- La dernière release de green-claude est `v1.5.0`, publiée le 21 octobre 2026 ; son manifeste sur `main` annonce aussi 1.5.0. Le plugin utilisé porte cette version. Cette comparaison de version ne certifie pas l’identité de tous ses fichiers.
- Une autre entrée locale, `~/.agents/skills/green-claude/SKILL.md`, annonce 1.4.0 et contient une adaptation intitulée « Green Codex ». Clarifier les noms et la provenance avant de la mettre à jour : un remplacement direct par les instructions Claude introduirait des commandes propres à un autre client.

Sources : [commit skill-nr](https://github.com/Institut-du-Numerique-Responsable/skill-nr/commit/01ff0f3f8157f1391bd8aefd6d552ab62674ca5f), [écart release/main](https://github.com/Institut-du-Numerique-Responsable/skill-nr/compare/v1.0.0...main), [release green-claude](https://github.com/Institut-du-Numerique-Responsable/green-claude/releases/tag/v1.5.0).

## Évolutions prioritaires

`FAIL` désigne un écart confirmé dans ce périmètre ; `REVIEW` demande une mesure ou un arbitrage ; `PASS` indique un contrôle effectué. Ces verdicts ne constituent pas une certification RGESN. P1 : fiabilité et contexte récurrent ; P2 : méthode et mesure ; P3 : optimisation secondaire.

| Priorité / verdict | Preuve | Évolution et vérification attendue |
| --- | --- | --- |
| **P1 · FAIL** : le hook peut valider un index fautif | `scripts/eco-audit.sh:128` sélectionne les noms indexés, mais `:158` lit les fichiers de travail. Reproduction : indexer `SELECT * FROM clients;`, puis remplacer le fichier sans le réindexer par `SELECT id FROM clients;`. L’audit sort en 0 alors que le commit contiendrait encore `SELECT *`. | Auditer les blobs de l’index en mode pre-commit ; conserver la lecture du disque pour l’audit explicite. Tester les deux sens d’un index et d’un arbre de travail divergents. Principe green-claude : NR-TOK-027, qualité avant économie. |
| **P1 · FAIL** : des noms accentués disparaissent de la sélection | `scripts/eco-audit.sh:125` et `:130` lisent les sorties Git ligne par ligne, sans `-z`. Avec la configuration Git par défaut, un fichier indexé `requête.sql` contenant `SELECT *` produit « Aucun fichier à auditer. », code 0. | Utiliser des chemins terminés par NUL dans les deux sélections. Tester accent, tabulation, saut de ligne, espaces et nom commençant par tiret, en sélection automatique. Les tests actuels couvrent seulement le passage explicite de certains noms. NR-TOK-027. |
| **P1 · FAIL** : des commentaires déclenchent un blocage | `scripts/eco-audit.sh:158` applique les motifs au texte brut. Un fichier contenant `-- SELECT * FROM clients;` puis `SELECT id FROM clients;` sort en 1. | Écarter les commentaires avec une méthode adaptée au langage, préserver les numéros de ligne et tester les chaînes qui ressemblent à des commentaires. Ajouter un corpus conforme pour mesurer les faux positifs. NR-TOK-027 et méthode de qualification de green-claude. |
| **P1 · FAIL** : trop de consignes chargées ensemble | `scripts/generer-versions.py:96`, `:121`, `:138`, `:163`, `:179`, `:209` concatènent toutes les règles. Les fichiers Claude et OpenCode font chacun **526 lignes / 34 361 octets**. Demander d’ignorer les autres langages ne retire pas leur texte du contexte. | Générer un socle court et des références par langage, ou sélectionner les langages lors de l’installation quand le client ne permet pas le chargement ciblé. Garder les formats Cursor/Copilot déjà ciblés. Vérifier le chargement réel dans chaque client et comparer la qualité sur le même corpus. NR-TOK-012/013/014. Gain en tokens et énergie non mesuré. |
| **P2 · FAIL** : affirmation énergétique sans preuve associée | `.continue/rules/usage-sobre-assistant.md:48` affirme qu’un petit modèle consomme « un ordre de grandeur de moins » pour un résultat équivalent, sans protocole ni référence. | Remplacer le ratio général par une recommandation conditionnelle ; documenter modèle, matériel, cache, charge et qualité pour tout chiffre. Ajouter les principes de mesure, arrêt après validation et préservation de la qualité des NR-TOK-022/027/028/029/030, sans recopier toute la checklist en contexte permanent. |
| **P2 · FAIL** : revue et correction mêlées sans qualification explicite | `.continue/agents/eco-check.md:34` demande des corrections directes, dont lazy loading et pagination, avant tout verdict formalisé. Le fichier ne distingue pas FAIL/REVIEW/PASS. | Séparer diagnostic et correction selon la demande, exiger preuve et test de validation. Ne pas appliquer automatiquement lazy loading à une image critique ni changer un contrat de pagination sans contexte. Préciser les limites de la revue et proposer un registre de décisions validées par l’équipe. NR-TOK-027 et méthode de rapport de green-claude. |
| **P2 · REVIEW** : corpus trop étroit pour garantir les langages annoncés | La CI détecte **12/18** écarts dans deux fixtures HTML/SQL, avec un seuil de **10** (`scripts/verifier-depot.sh:125`). Les tests de robustesse passent malgré les défauts reproduits ci-dessus. | Ajouter cas positifs et négatifs par famille de détecteurs, tests d’index et de chemins. Suivre précision et rappel par règle ; ne pas confondre règles de processus et motifs automatisables. Fixer le seuil après stabilisation des fixtures, sans exiger artificiellement 18/18 du préfiltre. |
| **P3 · REVIEW** : coût CI et processus shell à mesurer | `.github/workflows/verification.yml:42` récupère tout l’historique ; aucune annulation des exécutions supersédées. `scripts/verifier-depot.sh:91` lance plusieurs processus par fichier Markdown et utilise des chemins `/tmp/nr-*` fixes. | Ajouter une concurrence par branche/PR, isoler les fichiers temporaires avec nettoyage, mesurer les étapes avant de réduire les parcours. Conserver le merge-base nécessaire si le fetch est limité. ECO-SH-01/02/03 ; bénéfice absolu non quantifié sur ce petit dépôt. |

## Résultats et alertes écartées

- **PASS** : `bash scripts/verifier-depot.sh`, code 0. Génération, frontmatters, liens, références citées, syntaxe, tests de noms explicites, tests de release et corpus passent. Le préfiltre interne rapporte zéro constat élevé et un moyen.
- **PASS** : les dernières exécutions GitHub « Vérification » et « pages-build-deployment » du commit audité sont en succès.
- **PASS, lecture statique seulement** : site léger, HTML/CSS local et polices système ; pages FR/EN de 17 714 et 17 516 octets. Pas d’alerte green-claude sur ces pages. Aucun test navigateur, mesure réseau réelle ou audit complet d’accessibilité effectué.
- L’audit green-claude a examiné les neuf scripts, le workflow et les deux pages : **huit alertes candidates**. Cinq portent sur du texte de règles ou de fixtures (`autoplay`, bibliothèques, SQL dans le préfiltre, ses tests et le générateur). Elles ne démontrent aucune exécution de ces opérations : faux positifs écartés.
- L’alerte ECO-SH-01 vise la substitution dans l’en-tête d’une boucle, évaluée une seule fois : ce motif ne démontre pas le défaut annoncé. Le corps comporte cependant des processus par fichier, d’où la recommandation de mesure P3.
- Les alertes ECO-SH-02/03 sur les pipelines sont confirmées, mais leur priorité reste faible. Réduire quelques processus ne doit pas diminuer la lisibilité.
- L’alerte interne sur `scripts/scorer-detection.py:127` concerne la lecture complète du rapport. **REVIEW** : mesurer les tailles réelles avant d’introduire du streaming dans un scorer dont les recherches utilisent l’ensemble du texte.

## Ordre de réalisation proposé

1. Fiabiliser le préfiltre et enrichir les tests avec les trois reproductions. Ne pas intégrer green-claude en mode bloquant sans qualification de ses faux positifs.
2. Réduire les instructions permanentes dans le générateur et tester les déclinaisons sur des tâches comparables, en conservant accessibilité et exactitude.
3. Clarifier les verdicts de revue, les consignes de mesure et la provenance des skills installés.
4. Mesurer et optimiser la CI, puis préparer une nouvelle release après validation. Vérifier les licences et attributions avant toute reprise de code ou de règles de green-claude.

## Limites et sobriété de la session

Audit du dépôt courant, sans inventaire des autres projets locaux. Les contrôles existants passent mais ne couvrent pas les défauts supplémentaires reproduits. Les correctifs restent à réaliser ; aucune installation, publication ou mise à jour distante effectuée.

NR-TOK-007/009/018/020/025/027 appliquées : carte du dépôt consultée, scripts existants exécutés, lectures indépendantes regroupées, reproductions locales sans modèle supplémentaire. NR-TOK-028/030 : tokens d’entrée/sortie/cache, nombre d’appels modèle, coût et économie indisponibles. Aucun pourcentage d’économie ni équivalence carbone avancé.


## Intégration consécutive à l’audit

Les constats ci-dessus décrivent l’état initial. À la demande de l’utilisateur,
les évolutions suivantes ont ensuite été intégrées dans l’arbre de travail :

- Audit explicite de l’index, chemins Git terminés par NUL et régressions associées.
- Masquage SQL/HTML/Python, préservation des lignes et des délimiteurs dans les chaînes ;
  les autres langages restent à qualifier en revue. Aucun fichier sans règle applicable
  n’est traité par le filtre Python.
- Socle des cinq formats uniques : **7 928 octets / 128 lignes**, contre 34 361 octets /
  526 lignes avant modification ; références spécialisées conservées dans `.nr/regles/`.
  Documentation de migration et contrôle des références d’installation.
- Verdicts de revue, correction selon la demande, limites des mesures et suppression
  du ratio énergétique sans preuve.
- Douze paires fautif/conforme pour les familles du préfiltre, tests de chemins,
  index, commentaires et installation. Couverture des motifs encore partielle.
- Vérification de génération non mutante, temporaires isolés et nettoyés,
  annulation CI des exécutions supersédées, délai maximal et durée locale affichée.

La récupération de l’historique Git complet reste nécessaire au merge-base utilisé
par la CI actuelle ; aucune réduction de profondeur sans validation de ce calcul.
La lecture complète des petits rapports du scorer reste inchangée faute de volume
justifiant un traitement plus complexe.

Les règles spécialisées sont présentes et vérifiables, mais leur lecture effective
et la qualité des réponses restent à mesurer dans chaque client. La provenance des
skills locaux 1.4.0/1.5.0 est documentée ci-dessus ; leurs installations hors projet
n’ont pas été remplacées. Les scripts ajoutés ici sont spécifiques à skill-nr,
sans reprise de code du plugin green-claude. Le journal contient une section
« À publier » ; aucune release distante n’a été créée.
