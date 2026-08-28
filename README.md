<div align="center">

# Règles d'écoconception et de numérique responsable pour assistants IA

**RGESN · GR491 · Opquast · RGAA** appliqués automatiquement par votre assistant de code,
quel qu'il soit.

[![Site](https://img.shields.io/badge/site-skill--nr-0a7190)](https://institut-du-numerique-responsable.github.io/skill-nr/)
[![Version](https://img.shields.io/github/v/release/Institut-du-Numerique-Responsable/skill-nr?display_name=tag&sort=semver)](https://github.com/Institut-du-Numerique-Responsable/skill-nr/releases/latest)
[![Licence](https://img.shields.io/badge/licence-CC%20BY--SA%204.0-2ea44f)](LICENSE.md)
[![Langages couverts](https://img.shields.io/badge/langages-13-1b7a4a)](#langages-couverts)
[![Assistants pris en charge](https://img.shields.io/badge/assistants%20IA-11-1b7a4a)](#assistants-pris-en-charge)
[![RGESN](https://img.shields.io/badge/RGESN-v2%20(78%20crit%C3%A8res)-0b6e4f)](https://ecoresponsable.numerique.gouv.fr/publications/referentiel-general-ecoconception/)
[![GR491](https://img.shields.io/badge/GR491-61%20recommandations-0b6e4f)](https://gr491.isit-europe.org/)
[![Opquast](https://img.shields.io/badge/Opquast-CC%20BY--SA-0b6e4f)](https://checklists.opquast.com/fr/qualite-numerique/)
[![RGAA](https://img.shields.io/badge/RGAA-4-0b6e4f)](https://accessibilite.numerique.gouv.fr/)
[![PR bienvenues](https://img.shields.io/badge/PR-bienvenues-blueviolet)](CONTRIBUTING.md)

🇬🇧 [English version](README.en.md)

</div>

---

Ce dépôt traduit quatre référentiels français de sobriété numérique, **RGESN**,
**GR491**, **Opquast** et **RGAA**, en règles directement exploitables par un assistant
IA de code : pas de PDF à lire, l'assistant applique la règle pendant qu'il écrit,
et une revue de diff automatisée vérifie ce qui a été produit.

Écrites une seule fois, ces règles sont **déclinées automatiquement pour 11 assistants** :
il n'y a pas de version « officielle » et des versions bancales : chaque outil reçoit
le format qu'il attend nativement, généré depuis une source commune.

## Assistants pris en charge

| Assistant | Ce que vous installez | Installation |
| --- | --- | --- |
| [Continue](https://continue.dev) | `.continue/rules/` + `.continue/agents/` (source de référence) | [↓](#continue) |
| [Claude Code](https://claude.com/claude-code) | `CLAUDE.md` + `.claude/agents/` | [↓](#claude-code) |
| [Cursor](https://cursor.com) | `.cursor/rules/*.mdc` (ciblés par `globs`) | [↓](#cursor) |
| [GitHub Copilot](https://github.com/features/copilot) | `.github/instructions/*.instructions.md` (`applyTo`) | [↓](#github-copilot) |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `GEMINI.md` + commandes `/eco-check` | [↓](#gemini-cli) |
| [OpenCode](https://opencode.ai) | `AGENTS.md` + `.opencode/agent/` | [↓](#opencode) |
| [Mistral Vibe](https://docs.mistral.ai/vibe) | `AGENTS.md` + `.vibe/agents/` | [↓](#mistral-vibe) |
| [Kilo Code](https://kilo.ai) | `.kilo/rules/` + `kilo.jsonc` + `.kilo/agents/` | [↓](#kilo-code) |
| [OpenAI Codex](https://developers.openai.com/codex) | `AGENTS.md` (standard partagé) | [↓](#openai-codex-et-zcode-glm) |
| [Kimi CLI](https://github.com/MoonshotAI/kimi-cli) (Moonshot AI) | `AGENTS.md` + `.kimi/agents/` | [↓](#kimi-cli-moonshot-ai) |
| [ChatGPT](https://chatgpt.com) (GPT personnalisé) | instructions condensées + fichiers de connaissances | [↓](#chatgpt-gpt-personnalisé) |

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

Chaque règle ne s'active que sur les fichiers de son langage chez **Continue, Cursor et
GitHub Copilot** (`globs`, `applyTo`) ; les autres assistants reçoivent l'ensemble dans un
fichier unique, avec un repère explicite par section : voir [versions/README.md](versions/README.md#différence-avec-la-version-continue)
pour cette nuance.

## Référentiels utilisés

| Référentiel | Portée | Détail dans ce dépôt |
| --- | --- | --- |
| [RGESN 2024](https://ecoresponsable.numerique.gouv.fr/publications/referentiel-general-ecoconception/) (Arcep/Arcom/ADEME) | 78 critères, 9 thématiques | [referentiels/rgesn.md](referentiels/rgesn.md) |
| [GR491](https://gr491.isit-europe.org/) (INR) | 8 familles, 61 recommandations, 516 critères | [referentiels/gr491.md](referentiels/gr491.md) |
| [Opquast](https://checklists.opquast.com/fr/qualite-numerique/) | 35 règles taguées écoconception (CC BY-SA) | [referentiels/opquast-ecoconception.md](referentiels/opquast-ecoconception.md) |
| [RGAA 4](https://accessibilite.numerique.gouv.fr/) | Accessibilité numérique | agent `accessibilite-check` |

## Installation

Le principe est le même pour tous les outils : **des fichiers à copier à la racine du
projet où vous codez**. Rien à installer sur le poste, rien à configurer dans l'IDE, aucun
service à joindre. L'assistant les lit à l'ouverture du projet.

Un seul préalable, quel que soit l'outil : récupérer ce dépôt une fois quelque part.

```bash
git clone https://github.com/Institut-du-Numerique-Responsable/skill-nr.git
cd skill-nr
```

Dans tout ce qui suit, `$REGLES` désigne ce dossier et `$PROJET` le dépôt de votre
application. Vous pouvez poser les deux variables pour copier-coller les commandes telles
quelles :

```bash
export REGLES=$PWD
export PROJET=~/dev/mon-application
```

Un mot sur ce que vous copiez : `.continue/` est la **source**, tout le reste est généré
à partir d'elle par `scripts/generer-versions.py`. Vous installez donc soit `.continue/`
(Continue), soit un dossier de `versions/` (les autres). Jamais les deux.

### Continue

C'est la version de référence : chaque règle porte des `globs` et ne se charge que sur les
fichiers de son langage. Un fichier `.sql` ouvert ne coûte que les règles SQL.

```bash
cp -r "$REGLES/.continue" "$PROJET/"
```

Puis, côté outil, au choix :

- **Extension IDE** (usage quotidien) : installez Continue depuis le marketplace VS Code
  ou JetBrains, rouvrez `$PROJET`, les règles sont actives. L'icône stylo dans la barre
  Continue liste les règles chargées : c'est là que vous voyez si elles sont bien prises
  en compte.
- **CLI** (revue de diff, CI) :

  ```bash
  npm install -g @continuedev/cli   # fournit la commande `cn`
  cd "$PROJET" && cn                # les règles .continue/rules/ sont chargées d'office
  ```

  La CLI a besoin d'un modèle déclaré dans `~/.continue/config.yaml`. Elle n'a plus de
  connexion au compte Continue (`cn login` n'existe pas en v1.5.47, contrairement à sa
  doc). Configuration validée sur ce dépôt avec Ollama en local, gratuite et sans qu'aucun
  code ne quitte le poste : voir le [guide développeur](docs/guide-developpeur.md).

Revue d'un diff :

```bash
cn review --review-agents .continue/agents/eco-check.md
cn review --review-agents .continue/agents/accessibilite-check.md
```

Deux choses à savoir avant de lancer : l'agent **modifie directement vos fichiers** quand
il corrige, et le rapport détaillé ne s'affiche que dans un vrai terminal interactif.
Travaillez sur un état commité, et relisez les patchs comme n'importe quelle MR.

### Claude Code

```bash
cp "$REGLES/versions/claude-code/CLAUDE.md" "$PROJET/"
cp -r "$REGLES/versions/claude-code/.claude" "$PROJET/"
```

Si le projet a déjà un `CLAUDE.md`, ne l'écrasez pas : ajoutez le contenu à la suite, ou
gardez les règles dans un fichier séparé et référencez-le depuis le vôtre avec
`@regles-nr.md`.

Lancez `claude` dans `$PROJET`. Les deux sous-agents apparaissent dans `/agents` ; pour une
revue, demandez « lance l'agent eco-check sur mes changements ».

### Cursor

Avec Continue et Copilot, c'est l'une des trois déclinaisons où chaque règle est
**ciblée par `globs`** : un fichier `.sql` ouvert ne charge que les règles SQL. Vous ne
payez jamais le contexte des langages que le projet n'utilise pas.

```bash
cp -r "$REGLES/versions/cursor/.cursor" "$PROJET/"
```

Une règle par fichier `.mdc` dans `.cursor/rules/`, plus deux commandes dans
`.cursor/commands/` : tapez `/eco-check` ou `/accessibilite-check` dans le chat. Si le
projet a déjà des règles Cursor, les fichiers cohabitent sans conflit, les noms étant
préfixés `ecoconception-` et `numerique-responsable`.

### GitHub Copilot

```bash
cp -r "$REGLES/versions/copilot/.github" "$PROJET/"
```

Chaque fichier `.instructions.md` porte un `applyTo` qui limite son chargement aux
fichiers concernés, comme les `globs` de Continue. Les deux prompts de revue sont dans
`.github/prompts/` : tapez `/eco-check` dans Copilot Chat.

Attention si le projet a déjà un dossier `.github/` : copiez le contenu plutôt que
d'écraser le dossier entier, sinon vous perdez vos workflows.

```bash
mkdir -p "$PROJET/.github/instructions" "$PROJET/.github/prompts"
cp "$REGLES"/versions/copilot/.github/instructions/* "$PROJET/.github/instructions/"
cp "$REGLES"/versions/copilot/.github/prompts/*      "$PROJET/.github/prompts/"
```

### Gemini CLI

```bash
cp "$REGLES/versions/gemini-cli/GEMINI.md" "$PROJET/"
cp -r "$REGLES/versions/gemini-cli/.gemini" "$PROJET/"
```

C'est la déclinaison la plus confortable pour la revue : les commandes `/eco-check` et
`/accessibilite-check` injectent elles-mêmes le `git diff HEAD` dans le prompt, vous n'avez
rien à coller. Lancez `gemini` dans `$PROJET` et tapez `/eco-check`.

### OpenCode

```bash
cp "$REGLES/versions/opencode/AGENTS.md" "$PROJET/"
cp -r "$REGLES/versions/opencode/.opencode" "$PROJET/"
```

Attention si le projet a déjà un `AGENTS.md` (c'est fréquent, le format est partagé par
plusieurs outils) : concaténez plutôt qu'écraser.

```bash
cat "$REGLES/versions/opencode/AGENTS.md" >> "$PROJET/AGENTS.md"
```

Lancez `opencode` dans `$PROJET`, puis mentionnez l'agent `eco-check` (déclaré en
`mode: subagent`) ou `accessibilite-check` pour une revue.

### Mistral Vibe

```bash
cp "$REGLES/versions/mistral-vibe/AGENTS.md" "$PROJET/"
cp -r "$REGLES/versions/mistral-vibe/.vibe" "$PROJET/"
```

Une étape en plus : ouvrez `.vibe/agents/eco-check.toml` et
`.vibe/agents/accessibilite-check.toml` pour remplacer `active_model` par un modèle
disponible dans votre organisation (la valeur générée, `mistral-medium-latest`, n'est
qu'un défaut raisonnable).

```bash
cd "$PROJET" && vibe --agent eco-check
```

### Kimi CLI (Moonshot AI)

```bash
cp "$REGLES/versions/kimi-cli/AGENTS.md" "$PROJET/"
cp -r "$REGLES/versions/kimi-cli/.kimi" "$PROJET/"
```

Même vigilance que pour OpenCode sur un `AGENTS.md` déjà présent. Les fichiers `.yaml`
pointent vers le `.md` voisin via `system_prompt_path` : gardez les deux ensemble dans
`.kimi/agents/`.

```bash
cd "$PROJET" && kimi --agent-file .kimi/agents/eco-check.yaml
```

### Kilo Code

```bash
cp -r "$REGLES/versions/kilo/.kilo" "$PROJET/"
cp "$REGLES/versions/kilo/kilo.jsonc" "$PROJET/"
```

Si le projet a déjà un `kilo.jsonc`, ne l'écrasez pas : ouvrez-le et ajoutez les entrées
`.kilo/rules/*.md` à sa clé `instructions` (une règle non listée n'est jamais chargée).
Kilo ne cible pas les règles par type de fichier : tout ce que liste `instructions` est
chargé à chaque session, commentez les langages que le projet n'utilise pas.

Lancez Kilo dans `$PROJET`, puis appelez la revue avec `@eco-check` ou
`@accessibilite-check` dans le chat (les deux sont déclarés en `mode: subagent`).

Les anciennes versions de l'extension lisaient `.kilocode/rules/` sans `kilo.jsonc` ;
ce dossier reste pris en charge par compatibilité, un `mv .kilo .kilocode` suffit alors.

### OpenAI Codex et ZCode (GLM)

Ces deux outils lisent nativement `AGENTS.md`, le fichier d'OpenCode leur convient tel
quel. Pas de dossier dédié à copier, pas d'agent de revue déclaré : la revue se demande
en langage naturel.

```bash
cp "$REGLES/versions/opencode/AGENTS.md" "$PROJET/"
```

Cas voisin : **GLM utilisé comme fournisseur de modèle** dans Claude Code, OpenCode ou
Cline. Là il n'y a rien de spécifique à faire, l'installation de l'outil hôte s'applique.

### ChatGPT (GPT personnalisé)

Pas de fichiers dans le projet ici : ChatGPT ne lit pas votre dépôt. On construit un GPT
qui porte les règles, et l'équipe lui soumet son code.

Les instructions d'un GPT sont limitées à environ 8 000 caractères, trop peu pour les
règles complètes. D'où deux étages :

1. **ChatGPT → Explorer les GPT → Créer**. Dans *Instructions*, collez le contenu de
   `versions/chatgpt/instructions-gpt.md` (environ 2,5 Ko : les principes toujours actifs
   et l'index des sections par langage).
2. Dans *Connaissances*, téléversez les 5 fichiers de
   `versions/chatgpt/connaissances/` : les règles complètes, les deux méthodes de revue,
   et les extractions GR491 et Opquast. Le GPT y pioche la section du langage concerné.

Partagez ensuite le GPT par lien interne à l'organisation. La création demande un compte
Plus, Team ou Enterprise. Un *Projet* ChatGPT fonctionne aussi, avec les mêmes deux étages.

## Le garde-fou déterministe

Les règles orientent la génération, les agents relisent à la demande : ni l'un ni l'autre
ne se déclenche tout seul au moment du commit. `scripts/eco-audit.sh` comble ce trou. Il
cherche par `grep` des motifs connus, sans appeler aucun modèle : pas de coût, pas
d'attente, pas de correctif inventé.

```bash
bash scripts/eco-audit.sh                    # fichiers indexés, sinon tout le dépôt
bash scripts/eco-audit.sh src/api.sql        # fichiers précis
bash scripts/eco-audit.sh --installer-hook   # bloque le commit sur un constat élevé
```

Chaque constat sort avec son fichier, sa ligne et son critère source. Seuls les constats
« Élevé » font échouer la commande ; `--avertir` n'échoue jamais, pour un premier
déploiement en équipe.

Le calibrage a été fait sur du code tiers réel : sur 600 fichiers d'un projet open source,
3 constats bloquants, tous fondés. Les motifs trop bruyants pour un hook (`import * as`,
`.ToList()`, `.clone()`) sont derrière `--tout`, réservé aux audits ponctuels. `--motifs`
liste la table complète.

Ce que le script ne voit pas reste du ressort des règles et des agents : il n'attrape
aucune absence (une pagination manquante, une rétention non définie), ni rien qui demande
de comprendre l'intention. Sur les 18 écarts du corpus de vérification, il en trouve 12.
C'est un filtre, pas un juge.

## Vérifier que l'installation fonctionne

Copier des fichiers ne prouve pas que l'assistant les lit. Un `AGENTS.md` écrasé, un
mauvais dossier, une extension non rechargée : rien ne le signale, l'assistant continue de
répondre, simplement sans les règles. Le dossier
[`verification/`](verification/README.md) sert à lever ce doute, en trois minutes.

**1. Les fichiers sont-ils au bon endroit ?**

```bash
bash "$REGLES/scripts/verifier-installation.sh" auto "$PROJET"
```

Le script détecte les outils présents et contrôle chaque fichier attendu, contenu compris :
un `AGENTS.md` qui existe mais ne contient pas les règles est signalé comme tel. Ciblez un
outil précis si besoin : `claude-code`, `opencode`, `gemini-cli`, `mistral-vibe`,
`kimi-cli`, `kilo`, `cursor`, `copilot`, `continue`, `codex`, `chatgpt`.

**2. L'assistant applique-t-il vraiment les règles ?**

```bash
cp "$REGLES"/verification/exemple-a-corriger.* "$PROJET/"
```

Ces deux fichiers, un HTML et un SQL, contiennent **18 écarts volontaires**. Demandez à
votre assistant, dans `$PROJET` :

> Relis `exemple-a-corriger.html` et `exemple-a-corriger.sql` sous l'angle écoconception et
> accessibilité. Liste les écarts et cite le critère source pour chacun.

Comparez à [`verification/resultats-attendus.md`](verification/resultats-attendus.md), qui
détaille les 18 écarts avec leurs critères. Repère mesuré : **12 écarts sur 18**. En dessous
de 5, les règles ne sont pas chargées.

Une mise en garde issue de la mesure : ne prenez pas la citation d'un critère pour une
preuve. Un modèle local avec les règles chargées a trouvé 16 écarts sur 18, mais a cité un
critère qui n'existe pas (thématique 6 du RGESN, qui s'arrête à 6.7) et inventé des
intitulés pour les autres. `scorer-detection.py` vérifie donc chaque identifiant contre
`referentiels/`. Testez aussi dans un dossier isolé : depuis ce dépôt, l'assistant a accès
à la grille de réponses.

Pour éviter la comparaison à la main, passez le rapport au scorer :

```bash
python3 scripts/scorer-detection.py rapport.txt      # ou par un tube
```

Il sort le nombre d'écarts détectés, les critères cités, et ceux qui manquent. Utile
surtout pour **mesurer une évolution des règles** : sans ce chiffre, on empile des
consignes sans savoir si l'observance monte ou baisse.

Le signal le plus fiable n'est pas le nombre d'écarts mais la **citation des critères**.
N'importe quel modèle correct dira qu'une image manque d'`alt` ; seul un modèle qui a les
règles en contexte écrira « Opquast n°124 » ou « GR491_Backend_3 ».

Pensez à retirer les fichiers de test ensuite : `rm "$PROJET"/exemple-a-corriger.*`.

**3. Et en écriture ?** La revue n'est que la moitié du sujet. Demandez une requête SQL ou
une galerie d'images sans autre précision : avec les règles chargées, la requête pagine et
projette ses colonnes, les images arrivent en `loading="lazy"` avec `alt` et dimensions.
Cette différence-là est la vraie preuve. Détail dans
[verification/README.md](verification/README.md).

## Mettre à jour, désinstaller

Les règles évoluent. Pour resynchroniser un projet, refaites simplement la copie de votre
outil après un `git pull` dans `$REGLES` : les fichiers générés sont écrasés à l'identique,
sauf ceux que vous avez adaptés à la main (le `active_model` de Mistral Vibe, un
`AGENTS.md` concaténé). À l'échelle de plusieurs dépôts, voir le
[guide de déploiement](docs/guide-deploiement.md).

Pour désinstaller, supprimez les fichiers copiés. Aucune trace ailleurs : rien n'est écrit
dans votre home ni dans la configuration de l'outil.

## Problèmes fréquents

| Symptôme | Cause probable et remède |
| --- | --- |
| L'assistant ne cite jamais de critère | Fichiers au mauvais endroit : ils doivent être à la **racine** du projet ouvert, pas dans un sous-dossier. Lancez `verifier-installation.sh`. |
| Les règles marchaient, plus maintenant | Un `AGENTS.md` ou `CLAUDE.md` du projet a écrasé la copie lors d'un merge. Recopiez, en concaténant cette fois. |
| Session très lourde en contexte | Normal hors Continue : les formats à fichier unique chargent toutes les règles à chaque session (34 Ko aujourd'hui, taille exacte avec `wc -c versions/opencode/AGENTS.md`). Supprimez de votre copie les sections des langages que le projet n'utilise pas (sous Kilo Code, commentez la ligne correspondante de `kilo.jsonc`). |
| `Agent file must contain YAML frontmatter with a 'name' field` | Un agent `.md` a perdu son frontmatter à la copie. Recopiez le fichier entier. |
| `Cannot start TUI in TTY-less environment` (Continue) | Contexte non interactif : utilisez `cn -p "prompt"` ou lancez depuis un vrai terminal. |
| Revue sans résultat visible (Continue) | Les correctifs sont peut-être déjà appliqués dans vos fichiers : regardez `git diff`. |
| Un correctif proposé est faux | C'est possible et attendu : le patch est une proposition, pas une vérité. Cas observé, un `.filter()` appelé sur une `List` Java. Relisez comme une MR. |

## Documentation

- 📘 [Guide développeur](docs/guide-developpeur.md) : installer, utiliser au quotidien, lancer une revue, dépanner.
- 📗 [Guide de déploiement](docs/guide-deploiement.md) : diffuser les règles aux équipes (git, Hub, CI), choix des modèles, licences.
- 🚀 [Guide de release](docs/guide-release.md) : préparer, vérifier et publier une version.
- 📙 [Développer un skill](docs/developper-un-skill.md) : écrire une règle ou un agent, les tester, pièges connus.
- ✅ [verification/README.md](verification/README.md) : contrôler qu'un assistant a bien chargé les règles.
- 🔧 [versions/README.md](versions/README.md) : formats générés, différences entre outils, cas non retenus.

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `.continue/rules/` | Règles source, ciblées par langage via `globs`. |
| `.continue/agents/` | Agents de revue de diff (`eco-check`, `accessibilite-check`). |
| `referentiels/` | Extractions sourcées (RGESN, GR491, Opquast) avec identifiants cités par les règles, vérifiés en CI. |
| `versions/` | Versions générées pour les 9 autres assistants. |
| `verification/` | Fichiers de test non conformes et écarts attendus, pour valider une installation. |
| `scripts/generer-versions.py` | Régénère `versions/` depuis `.continue/` (source unique). |
| `scripts/verifier-installation.sh` | Contrôle que les fichiers de règles sont en place dans un projet. |
| `scripts/verifier-depot.sh` | Contrôles d'intégrité du dépôt, joués aussi par la CI sur chaque PR. |
| `scripts/installer-hooks.sh` | Pose les hooks git locaux (pré-filtre au commit, garde-fou au push). |
| `.github/workflows/` | CI : intégrité du dépôt, pré-filtre sur le diff de la PR. |
| `scripts/eco-audit.sh` | Pré-filtre déterministe (grep) : motifs connus, zéro appel modèle, utilisable en hook. |
| `scripts/scorer-detection.py` | Score un rapport de revue contre les 18 écarts du corpus, pour mesurer une évolution des règles. |
| `docs/` | Guides développeur, déploiement et contribution. |
| branche `test-eco` | Fichiers pièges par langage pour valider les agents après chaque évolution des règles. |

## Et green-claude ?

[green-claude](https://github.com/Institut-du-Numerique-Responsable/green-claude), un
autre projet de l'INR, répond à la même question : faire respecter le RGESN et le
GR491 par un assistant de code. Les choix de conception diffèrent sur trois points.

green-claude est un skill Claude Code : il s'installe une fois dans
`~/.claude/skills/` et ne vise que ce harnais, avec des hooks propres à ce produit
(cache local, avertissement aux heures de pointe). Ce dépôt part d'une source unique
et la décline pour onze assistants. Une équipe qui travaille sur Gemini CLI ou sur
Continue n'a aucun accès aux règles de green-claude ; elle a accès à celles-ci.

Sur la détection, les deux projets ont maintenant le même étage déterministe. Celui de
green-claude, `eco-audit.sh`, a inspiré le nôtre, qui en reprend les motifs et y ajoute
la couche HTML/CSS que green-claude ne couvre pas, puis rattache chaque constat à un
critère vérifié dans `referentiels/`. Cet étage compte : mesuré sur le corpus de
`verification/`, un modèle local détecte 16 écarts sur 18 mais ne les rattache
correctement qu'une fois sur dix-huit, et invente des identifiants de critères. Le
grep en trouve moins (12 sur 18) et les trace tous. Aucun des deux ne suffit seul.

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
