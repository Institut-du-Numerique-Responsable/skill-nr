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

`AGENTS.md` étant un standard partagé, la version OpenCode/Mistral Vibe est aussi lisible
par les autres outils qui l'adoptent.

## Différence avec la version Continue

Continue active chaque règle **par type de fichier** (`globs`) : un fichier Java ne charge
que les règles Java. Les fichiers de contexte uniques (`CLAUDE.md`, `GEMINI.md`,
`AGENTS.md`) n'ont pas ce mécanisme : **toutes les règles (~31 Ko) sont chargées à chaque
session**, avec une mention « S'applique aux fichiers : … » par section pour guider le
modèle. C'est le compromis de ces formats ; si votre projet n'utilise que certains
langages, supprimez les sections inutiles de votre copie (ou générez une variante) pour
économiser du contexte.
