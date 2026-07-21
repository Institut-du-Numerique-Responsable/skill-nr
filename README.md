<div align="center">

# 🌱 Règles d'écoconception et de numérique responsable pour assistants IA

**RGESN · GR491 · Opquast · RGAA** appliqués automatiquement par votre assistant de code,
quel qu'il soit.

[![Licence](https://img.shields.io/badge/licence-CC%20BY--SA%204.0-2ea44f)](LICENSE.md)
[![Langages couverts](https://img.shields.io/badge/langages-13-1b7a4a)](#langages-couverts)
[![Assistants pris en charge](https://img.shields.io/badge/assistants%20IA-7-1b7a4a)](#assistants-pris-en-charge)
[![RGESN](https://img.shields.io/badge/RGESN-v2%20(78%20crit%C3%A8res)-0b6e4f)](https://ecoresponsable.numerique.gouv.fr/publications/referentiel-general-ecoconception/)
[![GR491](https://img.shields.io/badge/GR491-61%20recommandations-0b6e4f)](https://gr491.isit-europe.org/)
[![Opquast](https://img.shields.io/badge/Opquast-CC%20BY--SA-0b6e4f)](https://checklists.opquast.com/fr/qualite-numerique/)
[![PR bienvenues](https://img.shields.io/badge/PR-bienvenues-blueviolet)](CONTRIBUTING.md)

</div>

---

Ce dépôt traduit quatre référentiels français de sobriété numérique — **RGESN**,
**GR491**, **Opquast**, **RGAA** — en règles directement exploitables par un assistant
IA de code : pas de PDF à lire, l'assistant applique la règle pendant qu'il écrit,
et une revue de diff automatisée vérifie ce qui a été produit.

Écrites une seule fois, ces règles sont **déclinées automatiquement pour 7 assistants** :
il n'y a pas de version « officielle » et des adaptations bancales — chaque outil reçoit
le format qu'il attend nativement, généré depuis une source commune.

## Assistants pris en charge

| Assistant | Ce que vous installez | Doc |
| --- | --- | --- |
| [Continue](https://continue.dev) | `.continue/rules/` + `.continue/agents/` (source de référence) | [README](#-démarrage-avec-continue) |
| [Claude Code](https://claude.com/claude-code) | `CLAUDE.md` + `.claude/agents/` | [adaptations/claude-code](adaptations/claude-code) |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `GEMINI.md` + commandes `/eco-check` | [adaptations/gemini-cli](adaptations/gemini-cli) |
| [OpenCode](https://opencode.ai) | `AGENTS.md` + `.opencode/agent/` | [adaptations/opencode](adaptations/opencode) |
| [Mistral Vibe](https://docs.mistral.ai/vibe) | `AGENTS.md` + `.vibe/agents/` | [adaptations/mistral-vibe](adaptations/mistral-vibe) |
| [OpenAI Codex](https://developers.openai.com/codex) | `AGENTS.md` (standard partagé) | [adaptations/opencode](adaptations/opencode) |
| [ChatGPT](https://chatgpt.com) (GPT personnalisé) | instructions condensées + fichiers de connaissances | [adaptations/chatgpt](adaptations/chatgpt) |

Tout le détail d'installation par outil est dans [adaptations/README.md](adaptations/README.md).

## Ce que ça fait concrètement

Deux mécanismes complémentaires, portés par chaque déclinaison :

- **Les règles** orientent le code que l'assistant génère — *prévention*. Une requête
  SQL est paginée sans qu'on le demande, une image passe en `loading="lazy"`, un accès
  Entity Framework prend `AsNoTracking()`.
- **Les agents** (`eco-check`, `accessibilite-check`) relisent un diff après coup —
  *contrôle*. Ils citent le critère source (`GR491_Backend_1`, `Opquast n°124`,
  `RGESN 4.2`…) à chaque constat, pour que l'équipe monte en compétence au passage.

## Langages couverts

SQL/PL-SQL · HTML · CSS · JavaScript · TypeScript · Java · C# · Python · PHP · Ruby ·
Rust · C · C++

Chaque règle ne s'active que sur les fichiers de son langage (mécanisme `globs` côté
Continue) ; les autres assistants reçoivent l'ensemble avec un repère explicite par
section — voir [adaptations/README.md](adaptations/README.md#différence-avec-la-version-continue)
pour cette nuance.

## Référentiels utilisés

| Référentiel | Portée | Détail dans ce dépôt |
| --- | --- | --- |
| [RGESN v2](https://ecoresponsable.numerique.gouv.fr/publications/referentiel-general-ecoconception/) (ARCEP/ARCOM/ADEME) | 78 critères, 9 thématiques | cité par identifiant dans les règles |
| [GR491](https://gr491.isit-europe.org/) (INR) | 8 familles, 61 recommandations, 516 critères | [referentiels/gr491.md](referentiels/gr491.md) |
| [Opquast](https://checklists.opquast.com/fr/qualite-numerique/) | 35 règles taguées écoconception (CC BY-SA) | [referentiels/opquast-ecoconception.md](referentiels/opquast-ecoconception.md) |
| [RGAA 4](https://accessibilite.numerique.gouv.fr/) | Accessibilité numérique | agent `accessibilite-check` |

## 🚀 Démarrage avec Continue

Continue est la source de référence de ce dépôt (règles avec ciblage par langage via
`globs`, agents `.continue/agents/` exécutés par `cn review`).

```bash
npm install -g @continuedev/cli    # commande `cn`
cn                                 # les règles .continue/rules/ sont chargées automatiquement
```

Pour un modèle sans API payante (Ollama local, validé sur ce dépôt) et la commande de
revue de diff, voir le [guide développeur](docs/guide-developpeur.md).

## Documentation

- 📘 [Guide développeur](docs/guide-developpeur.md) — installer, utiliser au quotidien, lancer une revue, dépanner.
- 📗 [Guide de déploiement](docs/guide-deploiement.md) — diffuser les règles aux équipes (git, Hub, CI), choix des modèles, licences.
- 📙 [Développer un skill](docs/developper-un-skill.md) — écrire une règle ou un agent, les tester, pièges connus.
- 🔧 [adaptations/README.md](adaptations/README.md) — installation détaillée par assistant.

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `.continue/rules/` | Règles source, ciblées par langage via `globs`. |
| `.continue/agents/` | Agents de revue de diff (`eco-check`, `accessibilite-check`). |
| `referentiels/` | Extractions sourcées (GR491, Opquast) avec identifiants cités par les règles. |
| `adaptations/` | Déclinaisons générées pour les 6 autres assistants. |
| `scripts/generer-adaptations.py` | Régénère `adaptations/` depuis `.continue/` (source unique). |
| `docs/` | Guides développeur, déploiement et contribution. |
| branche `test-eco` | Fichiers pièges par langage pour valider les agents après chaque évolution des règles. |

## Contribuer

Une nouvelle règle, un langage manquant, un faux positif à corriger : voir
[CONTRIBUTING.md](CONTRIBUTING.md). Toute contribution se teste sur la branche
`test-eco` avant merge.

## Licence

[CC BY-SA 4.0](LICENSE.md) — l'incorporation des règles Opquast (elles-mêmes CC BY-SA)
impose cette licence à l'ensemble. Attributions complètes dans [LICENSE.md](LICENSE.md).
