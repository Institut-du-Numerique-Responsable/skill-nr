# Guide développeur — Assistant IA & écoconception

Ce guide s'adresse aux développeurs (SQL, JavaScript, Java, C#) qui utilisent
[Continue](https://continue.dev) avec les skills numérique responsable de ce dépôt.

## Ce que ça change pour vous

Une fois le dossier `.continue/` présent dans votre projet :

1. **Pendant que vous codez avec l'assistant** — les règles d'écoconception sont
   automatiquement injectées dans le contexte de l'IA. Le code généré applique le RGESN,
   le GR491 et Opquast sans que vous ayez rien à demander : requêtes SQL paginées et sans
   `SELECT *`, lectures EF Core avec `AsNoTracking()`, images en lazy loading, etc.
   L'assistant cite le critère qu'il applique (ex. « GR491_Backend_1 », « Opquast n°124 »)
   pour que vous montiez en compétence au passage.
2. **À la revue** — des agents relisent votre diff sous l'angle écoconception et
   accessibilité, et proposent des correctifs.

Les règles sont contextuelles : un fichier `.cs` charge les règles C#, un `.sql` les
règles SQL. Vous ne payez jamais le contexte des langages que vous n'utilisez pas.

## Installation

### Extension IDE (usage quotidien recommandé)

1. Installez l'extension **Continue** depuis le marketplace VS Code ou JetBrains.
2. Connectez-vous (bouton de connexion → compte Continue, offre gratuite) **ou**
   configurez un modèle local (voir ci-dessous).
3. Ouvrez un projet contenant `.continue/rules/` : les règles sont actives
   (icône stylo au-dessus de la barre d'outils de Continue pour les visualiser).

### CLI (revues de diff et automatisation)

```bash
npm install -g @continuedev/cli   # commande `cn`
```

Attention : la CLI publiée (v1.5.47 testée) ne propose pas de connexion au compte
Continue (`cn login` n'existe plus, contrairement à sa doc). Il lui faut un modèle
configuré dans `~/.continue/config.yaml`. Configuration validée avec un modèle local
[Ollama](https://ollama.com) — gratuit et aucune donnée ne quitte le poste :

```yaml
name: BPCE local (Ollama)
version: 0.0.1
schema: v1
models:
  - name: Qwen3 Coder (local)
    provider: ollama
    model: qwen3-coder:latest
    roles: [chat, edit, apply]
```

Prérequis : `ollama pull qwen3-coder` (≈18 Go, machine 32 Go de RAM minimum conseillée).

## Revue écoconception d'un diff

Dans un projet git avec des changements non commités, **dans un vrai terminal** :

```bash
cn review --review-agents .continue/agents/eco-check.md
cn review --review-agents .continue/agents/accessibilite-check.md
```

### À savoir absolument

- **L'agent modifie directement vos fichiers** quand il corrige (pas d'option à activer).
  Travaillez sur un état commité ou stashé pour pouvoir comparer : `git diff` après la
  revue montre exactement ce que l'agent a changé.
- **Relisez les patchs comme n'importe quelle MR.** Le modèle détecte bien les écarts,
  mais ses correctifs peuvent être faux (cas observé : un `.filter()` appelé sur une
  `List` Java, méthode inexistante). Le patch est une proposition, pas une vérité.
- Le rapport détaillé ne s'affiche que dans un terminal interactif (TTY). En script/CI,
  la sortie est réduite.

## Dépannage

| Symptôme | Cause / solution |
| --- | --- |
| `Agent file must contain YAML frontmatter with a 'name' field` | L'agent `.md` doit commencer par un frontmatter avec `name:`. |
| `Cannot start TUI in TTY-less environment` | Vous êtes dans un contexte non interactif : utilisez `cn -p "prompt"` ou lancez depuis un vrai terminal. |
| Revue sans résultat visible | Vérifiez qu'il y a des changements (`git status`), puis regardez `git diff` : les correctifs sont peut-être déjà appliqués dans vos fichiers. |
| Modèle muet / lent | `ollama ps` doit montrer le modèle chargé ; premier appel = chargement en RAM (long). |
| Les règles ne s'activent pas dans l'IDE | Le dossier `.continue/rules/` doit être à la racine du projet ouvert ; vérifiez l'icône stylo dans la barre Continue. |
