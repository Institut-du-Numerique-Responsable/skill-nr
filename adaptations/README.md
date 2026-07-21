# Adaptations pour d'autres assistants IA

Les règles NR de ce dépôt existent nativement au format [Continue](https://continue.dev)
(`.continue/`, source de vérité). Ce dossier contient leur déclinaison **générée** pour
d'autres assistants. Ne modifiez jamais ces fichiers à la main :

```bash
# après toute modification de .continue/rules/ ou .continue/agents/ :
python3 scripts/generer-adaptations.py
```

## Installation par outil

Copiez le contenu du sous-dossier correspondant à la racine de votre projet :

| Outil | Fichiers | Revue de diff |
| --- | --- | --- |
| **Claude Code** | `claude-code/CLAUDE.md` + `claude-code/.claude/agents/` | demander « lance l'agent eco-check » (sous-agents) |
| **Gemini CLI** | `gemini-cli/GEMINI.md` + `gemini-cli/.gemini/commands/` | `/eco-check` et `/accessibilite-check` (le diff est injecté automatiquement) |
| **OpenCode** | `opencode/AGENTS.md` + `opencode/.opencode/agent/` | mentionner l'agent `eco-check` (mode subagent) |
| **Mistral Vibe** | `mistral-vibe/AGENTS.md` + `mistral-vibe/.vibe/` | `vibe --agent eco-check` (ajustez `active_model` dans les `.toml`) |
| **Kimi CLI** (Moonshot AI) | `kimi-cli/AGENTS.md` + `kimi-cli/.kimi/agents/` | `kimi --agent-file .kimi/agents/eco-check.yaml` |
| **ChatGPT** | voir ci-dessous (GPT personnalisé) | demander une revue du diff collé, méthode `revue-ecoconception.md` |

`AGENTS.md` étant un standard partagé, la version OpenCode/Mistral Vibe/Kimi CLI est
aussi lisible par les autres outils qui l'adoptent — y compris **OpenAI Codex** (CLI/IDE)
et **ZCode** (harnais officiel de Z.ai pour GLM), qui lisent tous les deux `AGENTS.md`
nativement : copiez simplement `opencode/AGENTS.md` à la racine pour l'un ou l'autre.

## Cas non retenus : DeepSeek, GLM via un autre harnais

**GLM** (Z.ai) se branche le plus souvent comme *provider* dans un outil déjà couvert
ici (Claude Code, OpenCode, Cline…) : dans ce cas, aucune action nécessaire, les
fichiers existants s'appliquent tels quels. Seul le harnais officiel ZCode (ci-dessus)
justifiait une mention séparée, et il lit déjà notre `AGENTS.md`.

**DeepSeek** n'a pas de harnais officiel unique avec un format de règles stabilisé —
le paysage 2026 se partage entre un terminal propriétaire, un TUI communautaire non
officiel et un usage en tant que modèle dans des outils déjà couverts (Claude Code,
OpenCode, Cline via un endpoint compatible OpenAI). Dans ce dernier cas, nos fichiers
existants s'appliquent aussi. Une déclinaison dédiée n'est pas retenue tant qu'aucun
format ne se stabilise.

## Cas particulier ChatGPT (GPT personnalisé)

Les instructions d'un GPT sont limitées à ~8 000 caractères : impossible d'y mettre les
règles complètes. Le dossier `chatgpt/` fournit donc deux étages :

1. **`instructions-gpt.md`** (~2,5 Ko) — à coller dans les *Instructions* du GPT
   (ChatGPT → Explorer les GPT → Créer) ou d'un *Projet* : principes toujours actifs +
   index des sections par langage.
2. **`connaissances/`** — les 5 fichiers à téléverser dans *Connaissances* (Knowledge)
   du GPT : règles complètes, méthodes de revue écoconception et accessibilité,
   extraction GR491 et Opquast. Le GPT y pioche la section du langage concerné.

Partagez ensuite le GPT à l'organisation (lien interne). Nécessite ChatGPT Plus/Team/
Enterprise pour la création.

## Différence avec la version Continue

Continue active chaque règle **par type de fichier** (`globs`) : un fichier Java ne charge
que les règles Java. Les fichiers de contexte uniques (`CLAUDE.md`, `GEMINI.md`,
`AGENTS.md`) n'ont pas ce mécanisme : **toutes les règles (~31 Ko) sont chargées à chaque
session**, avec une mention « S'applique aux fichiers : … » par section pour guider le
modèle. C'est le compromis de ces formats ; si votre projet n'utilise que certains
langages, supprimez les sections inutiles de votre copie (ou générez une variante) pour
économiser du contexte.
