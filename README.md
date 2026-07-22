<div align="center">

# Règles d'écoconception et de numérique responsable pour assistants IA

**RGESN · GR491 · Opquast · RGAA** appliqués automatiquement par votre assistant de code,
quel qu'il soit.

[![Site](https://img.shields.io/badge/site-regles--ecoconception--ia-0a7190)](https://institut-du-numerique-responsable.github.io/regles-ecoconception-ia/)
[![Licence](https://img.shields.io/badge/licence-CC%20BY--SA%204.0-2ea44f)](LICENSE.md)
[![Langages couverts](https://img.shields.io/badge/langages-13-1b7a4a)](#langages-couverts)
[![Assistants pris en charge](https://img.shields.io/badge/assistants%20IA-8-1b7a4a)](#assistants-pris-en-charge)
[![RGESN](https://img.shields.io/badge/RGESN-v2%20(78%20crit%C3%A8res)-0b6e4f)](https://ecoresponsable.numerique.gouv.fr/publications/referentiel-general-ecoconception/)
[![GR491](https://img.shields.io/badge/GR491-61%20recommandations-0b6e4f)](https://gr491.isit-europe.org/)
[![Opquast](https://img.shields.io/badge/Opquast-CC%20BY--SA-0b6e4f)](https://checklists.opquast.com/fr/qualite-numerique/)
[![RGAA](https://img.shields.io/badge/RGAA-4-0b6e4f)](https://accessibilite.numerique.gouv.fr/)
[![PR bienvenues](https://img.shields.io/badge/PR-bienvenues-blueviolet)](CONTRIBUTING.md)

</div>

---

Ce dépôt traduit quatre référentiels français de sobriété numérique, **RGESN**,
**GR491**, **Opquast** et **RGAA**, en règles directement exploitables par un assistant
IA de code : pas de PDF à lire, l'assistant applique la règle pendant qu'il écrit,
et une revue de diff automatisée vérifie ce qui a été produit.

Écrites une seule fois, ces règles sont **déclinées automatiquement pour 8 assistants** :
il n'y a pas de version « officielle » et des versions bancales : chaque outil reçoit
le format qu'il attend nativement, généré depuis une source commune.

## Assistants pris en charge

| Assistant | Ce que vous installez | Doc |
| --- | --- | --- |
| [Continue](https://continue.dev) | `.continue/rules/` + `.continue/agents/` (source de référence) | [README](#-démarrage-avec-continue) |
| [Claude Code](https://claude.com/claude-code) | `CLAUDE.md` + `.claude/agents/` | [versions/claude-code](versions/claude-code) |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `GEMINI.md` + commandes `/eco-check` | [versions/gemini-cli](versions/gemini-cli) |
| [OpenCode](https://opencode.ai) | `AGENTS.md` + `.opencode/agent/` | [versions/opencode](versions/opencode) |
| [Mistral Vibe](https://docs.mistral.ai/vibe) | `AGENTS.md` + `.vibe/agents/` | [versions/mistral-vibe](versions/mistral-vibe) |
| [OpenAI Codex](https://developers.openai.com/codex) | `AGENTS.md` (standard partagé) | [versions/opencode](versions/opencode) |
| [Kimi CLI](https://github.com/MoonshotAI/kimi-cli) (Moonshot AI) | `AGENTS.md` + `.kimi/agents/` | [versions/kimi-cli](versions/kimi-cli) |
| [ChatGPT](https://chatgpt.com) (GPT personnalisé) | instructions condensées + fichiers de connaissances | [versions/chatgpt](versions/chatgpt) |

Tout le détail d'installation par outil est dans [versions/README.md](versions/README.md).

## Ce que ça fait concrètement

Deux mécanismes complémentaires, portés par chaque déclinaison :

- **Les règles** orientent le code que l'assistant génère, en prévention. Une requête
  SQL est paginée sans qu'on le demande, une image passe en `loading="lazy"`, un accès
  Entity Framework prend `AsNoTracking()`.
- **Les agents** (`eco-check`, `accessibilite-check`) relisent un diff après coup,
  en contrôle. Ils citent le critère source (`GR491_Backend_1`, `Opquast n°124`,
  `RGESN 4.2`…) à chaque constat, pour que l'équipe monte en compétence au passage.

## Langages couverts

SQL/PL-SQL · HTML · CSS · JavaScript · TypeScript · Java · C# · Python · PHP · Ruby ·
Rust · C · C++

Chaque règle ne s'active que sur les fichiers de son langage (mécanisme `globs` côté
Continue) ; les autres assistants reçoivent l'ensemble avec un repère explicite par
section : voir [versions/README.md](versions/README.md#différence-avec-la-version-continue)
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

- 📘 [Guide développeur](docs/guide-developpeur.md) : installer, utiliser au quotidien, lancer une revue, dépanner.
- 📗 [Guide de déploiement](docs/guide-deploiement.md) : diffuser les règles aux équipes (git, Hub, CI), choix des modèles, licences.
- 📙 [Développer un skill](docs/developper-un-skill.md) : écrire une règle ou un agent, les tester, pièges connus.
- 🔧 [versions/README.md](versions/README.md) : installation détaillée par assistant.

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `.continue/rules/` | Règles source, ciblées par langage via `globs`. |
| `.continue/agents/` | Agents de revue de diff (`eco-check`, `accessibilite-check`). |
| `referentiels/` | Extractions sourcées (GR491, Opquast) avec identifiants cités par les règles. |
| `versions/` | Versions générées pour les 7 autres assistants. |
| `scripts/generer-versions.py` | Régénère `versions/` depuis `.continue/` (source unique). |
| `docs/` | Guides développeur, déploiement et contribution. |
| branche `test-eco` | Fichiers pièges par langage pour valider les agents après chaque évolution des règles. |

## Et green-claude ?

[green-claude](https://github.com/Institut-du-Numerique-Responsable/green-claude), un
autre projet de l'INR, répond à la même question : faire respecter le RGESN et le
GR491 par un assistant de code. Les choix de conception diffèrent sur trois points.

green-claude est un skill Claude Code : il s'installe une fois dans
`~/.claude/skills/` et ne vise que ce harnais, avec des hooks propres à ce produit
(cache local, avertissement aux heures de pointe). Ce dépôt part d'une source unique
et la décline pour huit assistants. Une équipe qui travaille sur Gemini CLI ou sur
Continue n'a aucun accès aux règles de green-claude ; elle a accès à celles-ci.

Sur la détection, green-claude a une longueur d'avance. Son script `eco-audit.sh`
repère des motifs par grep déterministe : `SELECT *`, `lodash`, `autoplay`. Zéro appel
modèle, zéro dépendance à sa fiabilité pour les cas simples. Ce dépôt n'a pas cet
étage : l'agent `eco-check` confie toute la détection au modèle. Sur un modèle local,
il a bien repéré les écarts attendus, mais a aussi produit un correctif Java invalide
(`.filter()` appelé sur une `List`, méthode qui n'existe pas). Un script de pré-filtre
du même genre manque encore ici.

Sur la couverture, les rôles s'inversent. green-claude retient 35 règles parmi les 78
critères RGESN, avec un ancrage marqué sur la famille Algorithmie/IA et sur la
sobriété d'usage de Claude Code lui-même (14 pratiques inspirées de Boris Cherny). Ce
dépôt couvre ce dernier point dans la règle `usage-sobre-assistant.md`, et ajoute
treize langages avec des anti-patterns propres à chacun (un N+1 ne s'écrit pas pareil
en JPA, en Entity Framework ou en ActiveRecord) ainsi qu'un référentiel que
green-claude n'utilise pas, Opquast.

Une équipe outillée des deux gagnerait le meilleur des deux mécanismes : le script de
green-claude pour un premier passage rapide sur les motifs connus, les règles de ce
dépôt pour ce que le grep ne voit pas.

## Contribuer

Une nouvelle règle, un langage manquant, un faux positif à corriger : voir
[CONTRIBUTING.md](CONTRIBUTING.md). Toute contribution se teste sur la branche
`test-eco` avant merge.

## Licence

[CC BY-SA 4.0](LICENSE.md). L'incorporation des règles Opquast (elles-mêmes CC BY-SA)
impose cette licence à l'ensemble. Attributions complètes dans [LICENSE.md](LICENSE.md).
