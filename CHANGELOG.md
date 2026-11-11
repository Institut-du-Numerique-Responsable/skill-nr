# Journal des versions

Les changements notables de skill-nr sont documentés ici. Le projet suit le
[versionnement sémantique](https://semver.org/lang/fr/).

## À publier

- Kilo Code : migration des 15 règles vers `.kilo/skills/<nom>/SKILL.md`, descriptions
  YAML citées et chargement à la demande ; retrait de la configuration de chargement intégral.

- Préfiltre : audit du contenu indexé, chemins Git terminés par NUL, commentaires
  SQL/HTML/Python masqués sans décaler les lignes ; erreurs techniques explicites.
- Contexte ciblé : socle et références `.nr/regles/` pour Claude Code, Gemini,
  OpenCode, Mistral Vibe, Kimi et les clients utilisant la version OpenCode.
  Migration : copier le dossier `.nr/` avec le fichier d’entrée.
- Revue : verdicts FAIL/REVIEW/PASS, correction selon la demande, mesures sans
  équivalence énergétique supposée.
- Vérification : génération non mutante avec `--check`, tests de régression et
  d’installation, temporaires isolés, durée des contrôles, annulation CI des runs supersédés.

## [1.0.0] — 2026-08-28

Première version stable :

- règles d’écoconception et de numérique responsable pour 11 assistants IA et 13 langages ;
- référentiels RGESN, GR491, Opquast et RGAA traçables ;
- génération automatique des formats depuis une source unique ;
- agents de revue écoconception et accessibilité ;
- pré-filtre déterministe et corpus de vérification reproductible.

[1.0.0]: https://github.com/Institut-du-Numerique-Responsable/skill-nr/releases/tag/v1.0.0
