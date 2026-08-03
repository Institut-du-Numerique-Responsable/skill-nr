<div align="center">

# Eco-design and digital sustainability rules for AI coding assistants

**RGESN · GR491 · Opquast · RGAA** applied automatically by your coding assistant,
whichever one you use.

[![Site](https://img.shields.io/badge/site-regles--ecoconception--ia-0a7190)](https://institut-du-numerique-responsable.github.io/regles-ecoconception-ia/)
[![Licence](https://img.shields.io/badge/licence-CC%20BY--SA%204.0-2ea44f)](LICENSE.md)
[![Languages covered](https://img.shields.io/badge/languages-13-1b7a4a)](#languages-covered)
[![AI assistants](https://img.shields.io/badge/AI%20assistants-8-1b7a4a)](#supported-assistants)
[![RGESN](https://img.shields.io/badge/RGESN-v2%20(78%20criteria)-0b6e4f)](https://ecoresponsable.numerique.gouv.fr/publications/referentiel-general-ecoconception/)
[![GR491](https://img.shields.io/badge/GR491-61%20recommendations-0b6e4f)](https://gr491.isit-europe.org/)
[![Opquast](https://img.shields.io/badge/Opquast-CC%20BY--SA-0b6e4f)](https://checklists.opquast.com/fr/qualite-numerique/)
[![RGAA](https://img.shields.io/badge/RGAA-4-0b6e4f)](https://accessibilite.numerique.gouv.fr/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-blueviolet)](CONTRIBUTING.md)

🇫🇷 [Version française](README.md)

</div>

---

This repository turns four French digital sustainability frameworks, **RGESN**,
**GR491**, **Opquast** and **RGAA**, into rules an AI coding assistant can act on
directly: no PDF to read, the assistant applies the rule while it writes, and an
automated diff review checks what came out.

Written once, these rules are **generated automatically for 8 assistants**: there is no
"official" version with shaky ports alongside it. Each tool gets the format it expects
natively, produced from a single source.

> **A note on language.** The rule files themselves are written in French, because they
> quote French frameworks (RGESN, GR491, RGAA) whose criteria have no official English
> wording. This has little effect in practice: current models read them fine and answer
> in whatever language you write in. Only this page and the repository's documentation
> are translated. If you need the rules in English, open an issue, it is a reasonable
> thing to want.

## Supported assistants

| Assistant | What you install | Setup |
| --- | --- | --- |
| [Continue](https://continue.dev) | `.continue/rules/` + `.continue/agents/` (reference source) | [↓](#continue) |
| [Claude Code](https://claude.com/claude-code) | `CLAUDE.md` + `.claude/agents/` | [↓](#claude-code) |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `GEMINI.md` + `/eco-check` commands | [↓](#gemini-cli) |
| [OpenCode](https://opencode.ai) | `AGENTS.md` + `.opencode/agent/` | [↓](#opencode) |
| [Mistral Vibe](https://docs.mistral.ai/vibe) | `AGENTS.md` + `.vibe/agents/` | [↓](#mistral-vibe) |
| [OpenAI Codex](https://developers.openai.com/codex) | `AGENTS.md` (shared standard) | [↓](#openai-codex-and-zcode-glm) |
| [Kimi CLI](https://github.com/MoonshotAI/kimi-cli) (Moonshot AI) | `AGENTS.md` + `.kimi/agents/` | [↓](#kimi-cli-moonshot-ai) |
| [ChatGPT](https://chatgpt.com) (custom GPT) | condensed instructions + knowledge files | [↓](#chatgpt-custom-gpt) |

## What it actually does

Two complementary mechanisms, carried by every version:

- **The rules** steer the code the assistant generates, as prevention. A SQL query comes
  out paginated without anyone asking, an image gets `loading="lazy"`, an Entity Framework
  read gets `AsNoTracking()`.
- **The agents** (`eco-check`, `accessibilite-check`) review a diff afterwards, as control.
  They cite the source criterion (`GR491_Backend_1`, `Opquast n°124`, `RGESN 4.2`…) on
  every finding, so the team learns the frameworks along the way.

## Languages covered

SQL/PL-SQL · HTML · CSS · JavaScript · TypeScript · Java · C# · Python · PHP · Ruby ·
Rust · C · C++

Each rule only activates on files of its own language (the `globs` mechanism on the
Continue side). Other assistants receive the whole set with an explicit marker per
section: see [versions/README.md](versions/README.md#différence-avec-la-version-continue)
for that nuance.

## Frameworks used

| Framework | Scope | Detail in this repository |
| --- | --- | --- |
| [RGESN v2](https://ecoresponsable.numerique.gouv.fr/publications/referentiel-general-ecoconception/) (ARCEP/ARCOM/ADEME) | 78 criteria, 9 themes | cited by identifier in the rules |
| [GR491](https://gr491.isit-europe.org/) (INR) | 8 families, 61 recommendations, 516 criteria | [referentiels/gr491.md](referentiels/gr491.md) |
| [Opquast](https://checklists.opquast.com/fr/qualite-numerique/) | 35 rules tagged eco-design (CC BY-SA) | [referentiels/opquast-ecoconception.md](referentiels/opquast-ecoconception.md) |
| [RGAA 4](https://accessibilite.numerique.gouv.fr/) | Digital accessibility | `accessibilite-check` agent |

## Installation

The principle is the same for every tool: **files to copy into the root of the project you
code in**. Nothing to install on the machine, nothing to configure in the IDE, no service
to reach. The assistant reads them when it opens the project.

One prerequisite, whichever tool you use: get this repository once, somewhere.

```bash
git clone https://github.com/Institut-du-Numerique-Responsable/regles-ecoconception-ia.git
cd regles-ecoconception-ia
```

In everything below, `$REGLES` is that folder and `$PROJET` is your application's
repository. You can set both variables and paste the commands as they are:

```bash
export REGLES=$PWD
export PROJET=~/dev/my-application
```

A word on what you are copying: `.continue/` is the **source**, everything else is
generated from it by `scripts/generer-versions.py`. So you install either `.continue/`
(Continue) or one folder from `versions/` (all the others). Never both.

### Continue

This is the reference version: every rule carries `globs` and only loads on files of its
own language. An open `.sql` file costs you the SQL rules and nothing else.

```bash
cp -r "$REGLES/.continue" "$PROJET/"
```

Then, on the tool side, either:

- **IDE extension** (day-to-day use): install Continue from the VS Code or JetBrains
  marketplace, reopen `$PROJET`, the rules are live. The pen icon in the Continue bar
  lists the loaded rules, which is where you see whether they were picked up.
- **CLI** (diff review, CI):

  ```bash
  npm install -g @continuedev/cli   # provides the `cn` command
  cd "$PROJET" && cn                # .continue/rules/ is loaded automatically
  ```

  The CLI needs a model declared in `~/.continue/config.yaml`. It no longer connects to a
  Continue account (`cn login` does not exist in v1.5.47, contrary to its docs). Validated
  on this repository with a local Ollama model, free and with no code leaving the machine:
  see the [developer guide](docs/guide-developpeur.md) (in French).

Reviewing a diff:

```bash
cn review --review-agents .continue/agents/eco-check.md
cn review --review-agents .continue/agents/accessibilite-check.md
```

Two things to know before you run it: the agent **edits your files directly** when it
fixes something, and the detailed report only shows in a real interactive terminal. Work
from a committed state, and read the patches like any other merge request.

### Claude Code

```bash
cp "$REGLES/versions/claude-code/CLAUDE.md" "$PROJET/"
cp -r "$REGLES/versions/claude-code/.claude" "$PROJET/"
```

If the project already has a `CLAUDE.md`, do not overwrite it: append the content, or keep
the rules in a separate file and reference it from yours with `@regles-nr.md`.

Run `claude` in `$PROJET`. Both subagents show up under `/agents`; for a review, ask
"run the eco-check agent on my changes".

### Gemini CLI

```bash
cp "$REGLES/versions/gemini-cli/GEMINI.md" "$PROJET/"
cp -r "$REGLES/versions/gemini-cli/.gemini" "$PROJET/"
```

This is the most comfortable version for reviews: the `/eco-check` and
`/accessibilite-check` commands inject `git diff HEAD` into the prompt themselves, you
have nothing to paste. Run `gemini` in `$PROJET` and type `/eco-check`.

### OpenCode

```bash
cp "$REGLES/versions/opencode/AGENTS.md" "$PROJET/"
cp -r "$REGLES/versions/opencode/.opencode" "$PROJET/"
```

Careful if the project already has an `AGENTS.md` (common, since several tools share the
format): concatenate rather than overwrite.

```bash
cat "$REGLES/versions/opencode/AGENTS.md" >> "$PROJET/AGENTS.md"
```

Run `opencode` in `$PROJET`, then mention the `eco-check` agent (declared as
`mode: subagent`) or `accessibilite-check` for a review.

### Mistral Vibe

```bash
cp "$REGLES/versions/mistral-vibe/AGENTS.md" "$PROJET/"
cp -r "$REGLES/versions/mistral-vibe/.vibe" "$PROJET/"
```

One extra step: open `.vibe/agents/eco-check.toml` and
`.vibe/agents/accessibilite-check.toml` and replace `active_model` with a model available
in your organisation (the generated value, `mistral-medium-latest`, is only a sane
default).

```bash
cd "$PROJET" && vibe --agent eco-check
```

### Kimi CLI (Moonshot AI)

```bash
cp "$REGLES/versions/kimi-cli/AGENTS.md" "$PROJET/"
cp -r "$REGLES/versions/kimi-cli/.kimi" "$PROJET/"
```

Same care as OpenCode about an existing `AGENTS.md`. The `.yaml` files point at the
neighbouring `.md` through `system_prompt_path`: keep both together in `.kimi/agents/`.

```bash
cd "$PROJET" && kimi --agent-file .kimi/agents/eco-check.yaml
```

### OpenAI Codex and ZCode (GLM)

Both tools read `AGENTS.md` natively, so the OpenCode file suits them as is. No dedicated
folder to copy, no declared review agent: you ask for the review in plain language.

```bash
cp "$REGLES/versions/opencode/AGENTS.md" "$PROJET/"
```

Related case: **GLM used as a model provider** inside Claude Code, OpenCode or Cline.
Nothing specific to do there, the host tool's installation applies.

### ChatGPT (custom GPT)

No files in the project here: ChatGPT does not read your repository. You build a GPT that
carries the rules, and the team submits its code to it.

A GPT's instructions are capped at roughly 8,000 characters, far too little for the full
rules. Hence two layers:

1. **ChatGPT → Explore GPTs → Create**. In *Instructions*, paste the content of
   `versions/chatgpt/instructions-gpt.md` (about 2.5 KB: the always-on principles and the
   index of sections by language).
2. In *Knowledge*, upload the 5 files from `versions/chatgpt/connaissances/`: the full
   rules, both review methods, and the GR491 and Opquast extracts. The GPT picks the
   section for the language at hand from there.

Then share the GPT through an internal link. Creating one requires a Plus, Team or
Enterprise account. A ChatGPT *Project* works too, with the same two layers.

## The deterministic guardrail

Rules steer generation and agents review on demand: neither fires by itself at commit
time. `scripts/eco-audit.sh` fills that gap. It greps for known patterns, calling no
model at all: no cost, no wait, no invented fix.

```bash
bash scripts/eco-audit.sh                    # staged files, otherwise the whole repo
bash scripts/eco-audit.sh src/api.sql        # specific files
bash scripts/eco-audit.sh --installer-hook   # blocks the commit on a high finding
```

Every finding comes out with its file, line and source criterion. Only "Élevé" findings
fail the command; `--avertir` never fails, for a first rollout across a team.

Calibration was done against real third-party code: on 600 files of an open source
project, 3 blocking findings, all genuine. Patterns too noisy for a hook (`import * as`,
`.ToList()`, `.clone()`) sit behind `--tout`, for one-off audits. `--motifs` prints the
full table.

What the script cannot see stays with the rules and the agents: it catches no absence
(a missing pagination, an undefined retention policy) and nothing that requires reading
intent. Out of the corpus's 18 defects it finds 12. It is a filter, not a judge.

## Checking that the installation works

Copying files does not prove the assistant reads them. An overwritten `AGENTS.md`, a wrong
folder, an extension that was never reloaded: nothing tells you, the assistant keeps
answering, just without the rules. The [`verification/`](verification/README.md) folder
settles that in three minutes.

**1. Are the files in the right place?**

```bash
bash "$REGLES/scripts/verifier-installation.sh" auto "$PROJET"
```

The script detects which tools are present and checks every expected file, content
included: an `AGENTS.md` that exists but does not contain the rules is reported as such.
Target a specific tool if needed: `claude-code`, `opencode`, `gemini-cli`, `mistral-vibe`,
`kimi-cli`, `continue`, `codex`, `chatgpt`.

**2. Does the assistant really apply the rules?**

```bash
cp "$REGLES"/verification/exemple-a-corriger.* "$PROJET/"
```

These two files, one HTML and one SQL, contain **18 deliberate defects**. Ask your
assistant, from `$PROJET`:

> Review `exemple-a-corriger.html` and `exemple-a-corriger.sql` for eco-design and
> accessibility. List the issues and cite the source criterion for each one.

Compare with [`verification/resultats-attendus.md`](verification/resultats-attendus.md),
which details all 18 defects and their criteria. Benchmark: **10 out of 18 found, at least
3 of them with a criterion cited**, and you are fine. Below 5, or if no criterion is ever
cited, the rules are not loaded.

The most reliable signal is not the number of findings but the **criterion citations**.
Any decent model will say an image is missing its `alt`; only a model with the rules in
context writes "Opquast n°124" or "GR491_Backend_3".

Remember to remove the test files afterwards: `rm "$PROJET"/exemple-a-corriger.*`.

**3. What about generation?** Reviewing is only half the story. Ask for a SQL query or an
image gallery with no further detail: with the rules loaded, the query paginates and
projects its columns, the images come out with `loading="lazy"`, `alt` and dimensions.
That difference is the real proof. Details in
[verification/README.md](verification/README.md).

## Updating, uninstalling

Rules evolve. To resync a project, just redo your tool's copy after a `git pull` in
`$REGLES`: generated files are overwritten identically, except the ones you adapted by
hand (Mistral Vibe's `active_model`, a concatenated `AGENTS.md`). Across several
repositories, see the [deployment guide](docs/guide-deploiement.md) (in French).

To uninstall, delete the copied files. Nothing else is left behind: nothing is written to
your home directory or to the tool's configuration.

## Common problems

| Symptom | Likely cause and fix |
| --- | --- |
| The assistant never cites a criterion | Files in the wrong place: they must sit at the **root** of the open project, not in a subfolder. Run `verifier-installation.sh`. |
| The rules worked, now they don't | The project's own `AGENTS.md` or `CLAUDE.md` overwrote the copy during a merge. Copy again, concatenating this time. |
| Very heavy context per session | Expected outside Continue: single-file formats load every rule each session (34 KB today, exact size with `wc -c versions/opencode/AGENTS.md`). Delete from your copy the sections for languages the project does not use. |
| `Agent file must contain YAML frontmatter with a 'name' field` | An agent `.md` lost its frontmatter during the copy. Copy the whole file again. |
| `Cannot start TUI in TTY-less environment` (Continue) | Non-interactive context: use `cn -p "prompt"` or run from a real terminal. |
| Review with no visible output (Continue) | The fixes may already be applied in your files: check `git diff`. |
| A suggested fix is wrong | Possible and expected: the patch is a proposal, not a truth. Observed case, a `.filter()` called on a Java `List`. Review it like a merge request. |

## Documentation

The guides below are in French.

- 📘 [Developer guide](docs/guide-developpeur.md): install, use day to day, run a review, troubleshoot.
- 📗 [Deployment guide](docs/guide-deploiement.md): roll the rules out to teams (git, Hub, CI), model choices, licences.
- 📙 [Writing a skill](docs/developper-un-skill.md): write a rule or an agent, test them, known pitfalls.
- ✅ [verification/README.md](verification/README.md): check that an assistant really loaded the rules.
- 🔧 [versions/README.md](versions/README.md): generated formats, differences between tools, cases not covered.

## Repository contents

| Path | Role |
| --- | --- |
| `.continue/rules/` | Source rules, targeted by language through `globs`. |
| `.continue/agents/` | Diff review agents (`eco-check`, `accessibilite-check`). |
| `referentiels/` | Sourced extracts (GR491, Opquast) with the identifiers the rules cite. |
| `versions/` | Versions generated for the 7 other assistants. |
| `verification/` | Deliberately non-compliant test files and expected findings, to validate an install. |
| `scripts/generer-versions.py` | Regenerates `versions/` from `.continue/` (single source). |
| `scripts/verifier-installation.sh` | Checks that the rule files are in place in a project. |
| `scripts/verifier-depot.sh` | Repository integrity checks, also run by CI on every PR. |
| `scripts/installer-hooks.sh` | Installs the local git hooks (pre-filter on commit, guardrail on push). |
| `.github/workflows/` | CI: repository integrity, pre-filter on the PR diff. |
| `scripts/eco-audit.sh` | Deterministic grep pre-filter: known patterns, zero model calls, usable as a commit hook. |
| `scripts/scorer-detection.py` | Scores a review report against the corpus's 18 defects, to measure a change to the rules. |
| `docs/` | Developer, deployment and contribution guides. |
| `test-eco` branch | Trap files per language, to validate the agents after every change to the rules. |

## What about green-claude?

[green-claude](https://github.com/Institut-du-Numerique-Responsable/green-claude), another
INR project, answers the same question: getting a coding assistant to respect RGESN and
GR491. The design choices differ on three points.

green-claude is a Claude Code skill: it installs once in `~/.claude/skills/` and targets
that harness only, with hooks specific to that product (local cache, warning during peak
grid hours). This repository starts from a single source and generates it for eight
assistants. A team working in Gemini CLI or Continue has no access to green-claude's
rules; it does have access to these.

On detection, green-claude is ahead. Its `eco-audit.sh` script spots patterns through
deterministic grep: `SELECT *`, `lodash`, `autoplay`. Zero model calls, zero dependency on
model reliability for the easy cases. This repository has no such layer: the `eco-check`
agent hands all detection to the model. On a local model it did find the expected issues,
but it also produced an invalid Java fix (`.filter()` called on a `List`, a method that
does not exist). A pre-filter script of the same kind is still missing here.

On coverage, the roles reverse. green-claude keeps 35 rules out of the 78 RGESN criteria,
with a strong anchor in the Algorithms/AI family and in the frugal use of Claude Code
itself (14 practices inspired by Boris Cherny). This repository covers that last point in
the `usage-sobre-assistant.md` rule, and adds thirteen languages with anti-patterns
specific to each (an N+1 does not look the same in JPA, in Entity Framework or in
ActiveRecord), plus a framework green-claude does not use, Opquast.

A team running both would get the best of the two mechanisms: green-claude's script for a
fast first pass on known patterns, this repository's rules for what grep cannot see.

## Contributing

A new rule, a missing language, a false positive to fix: see
[CONTRIBUTING.md](CONTRIBUTING.md) (in French). Every contribution is tested on the
`test-eco` branch before merging.

## Licence

[CC BY-SA 4.0](LICENSE.md). Incorporating the Opquast rules (themselves CC BY-SA) makes
this licence apply to the whole. Full attributions in [LICENSE.md](LICENSE.md).
