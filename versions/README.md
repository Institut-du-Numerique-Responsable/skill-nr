# Versions pour d'autres assistants IA

Les règles NR de ce dépôt existent nativement au format [Continue](https://continue.dev)
(`.continue/`, source de vérité). Ce dossier contient leur version **générée** pour
d'autres assistants. Ne modifiez jamais ces fichiers à la main :

```bash
# après toute modification de .continue/rules/ ou .continue/agents/ :
python3 scripts/generer-versions.py
```

## Installation par outil

**La procédure complète, outil par outil, est dans le
[README principal](../README.md#installation)** : commandes de copie, pièges (`AGENTS.md`
déjà présent, `active_model` de Mistral Vibe), et
[vérification de l'installation](../README.md#vérifier-que-linstallation-fonctionne).
Ce tableau n'en est que le résumé : copiez le contenu du sous-dossier correspondant à la
racine de votre projet.

| Outil | Fichiers | Revue de diff |
| --- | --- | --- |
| **Claude Code** | `claude-code/CLAUDE.md` + `claude-code/.claude/agents/` | demander « lance l'agent eco-check » (sous-agents) |
| **Cursor** | `cursor/.cursor/rules/` (une règle `.mdc` par langage) + `cursor/.cursor/commands/` | `/eco-check` dans le chat |
| **GitHub Copilot** | `copilot/.github/instructions/` (`applyTo` par langage) + `copilot/.github/prompts/` | `/eco-check` dans Copilot Chat |
| **Gemini CLI** | `gemini-cli/GEMINI.md` + `gemini-cli/.gemini/commands/` | `/eco-check` et `/accessibilite-check` (le diff est injecté automatiquement) |
| **OpenCode** | `opencode/AGENTS.md` + `opencode/.opencode/agent/` | mentionner l'agent `eco-check` (mode subagent) |
| **Mistral Vibe** | `mistral-vibe/AGENTS.md` + `mistral-vibe/.vibe/` | `vibe --agent eco-check` (ajustez `active_model` dans les `.toml`) |
| **Kimi CLI** (Moonshot AI) | `kimi-cli/AGENTS.md` + `kimi-cli/.kimi/agents/` | `kimi --agent-file .kimi/agents/eco-check.yaml` |
| **Kilo Code** | `kilo/.kilo/skills/<nom>/SKILL.md` + `kilo/.kilo/agents/` | `@eco-check` dans le chat (sous-agents) |
| **ChatGPT** | voir ci-dessous (GPT personnalisé) | demander une revue du diff collé, méthode `revue-ecoconception.md` |

`AGENTS.md` étant un standard partagé, la version OpenCode/Mistral Vibe/Kimi CLI est
aussi lisible par les autres outils qui l'adoptent, y compris **OpenAI Codex** (CLI/IDE)
et **ZCode** (harnais officiel de Z.ai pour GLM), qui lisent tous les deux `AGENTS.md`
nativement : copiez `opencode/AGENTS.md` et `opencode/.nr/` à la racine pour l’un ou l’autre.

## Cas non retenus : DeepSeek, GLM via un autre harnais

**GLM** (Z.ai) se branche le plus souvent comme *provider* dans un outil déjà couvert
ici (Claude Code, OpenCode, Cline…) : dans ce cas, aucune action nécessaire, les
fichiers existants s'appliquent tels quels. Seul le harnais officiel ZCode (ci-dessus)
justifiait une mention séparée, et il lit déjà notre `AGENTS.md`.

**DeepSeek** n'a pas de harnais officiel unique avec un format de règles stabilisé :
le paysage 2026 se partage entre un terminal propriétaire, un TUI communautaire non
officiel et un usage en tant que modèle dans des outils déjà couverts (Claude Code,
OpenCode, Cline via un endpoint compatible OpenAI). Dans ce dernier cas, nos fichiers
existants s'appliquent aussi. Une déclinaison dédiée n'est pas retenue tant qu'aucun
format ne se stabilise.

## Cas particulier ChatGPT (GPT personnalisé)

Les instructions d'un GPT sont limitées à ~8 000 caractères : impossible d'y mettre les
règles complètes. Le dossier `chatgpt/` fournit donc deux étages :

1. **`instructions-gpt.md`** (~2,5 Ko), à coller dans les *Instructions* du GPT
   (ChatGPT → Explorer les GPT → Créer) ou d'un *Projet* : principes toujours actifs +
   index des sections par langage.
2. **`connaissances/`** : les 5 fichiers à téléverser dans *Connaissances* (Knowledge)
   du GPT : règles complètes, méthodes de revue écoconception et accessibilité,
   extraction GR491 et Opquast. Le GPT y pioche la section du langage concerné.

Partagez ensuite le GPT à l'organisation (lien interne). Nécessite ChatGPT Plus/Team/
Enterprise pour la création.

## Différence avec la version Continue

Kilo Code utilise des skills : les métadonnées sont découvertes au démarrage et
le modèle lit le contenu selon la description. Les 15 règles sont disponibles dans
`.kilo/skills/`, sans liste `instructions` à maintenir dans `kilo.jsonc`.

Trois outils activent chaque règle **par type de fichier** : Continue (`globs`), Cursor
(`globs` dans le frontmatter `.mdc`) et GitHub Copilot (`applyTo`). Un fichier Java n'y
charge que les règles Java. Les fichiers de contexte uniques (`CLAUDE.md`, `GEMINI.md`,
`AGENTS.md`) contiennent désormais un socle commun et un index de références locales
`.nr/regles/`. Le modèle doit lire les références adaptées au langage et à la couche
technique, à la demande. Copiez le dossier `.nr/` avec le fichier d’entrée ;
`verifier-installation.sh` signale les références manquantes. Ce routage reste une
instruction au modèle, à valider en situation dans chaque client.
