# Développer un skill : écrire et tester règles et agents

## Deux mécanismes, deux usages

| | Règle (`.continue/rules/*.md`) | Agent (`.continue/agents/*.md`) |
| --- | --- | --- |
| Quand | Pendant la génération de code (chat, edit) | À la revue d'un diff (`cn review`) |
| Effet | Oriente ce que l'IA écrit | Détecte et corrige ce qui a été écrit |
| Portée | Fichiers ciblés par `globs` | Tout le diff |

Règle = prévention, agent = contrôle. Un critère important mérite souvent les deux.

## Anatomie d'une règle

```md
---
name: Écoconception SQL                # obligatoire
description: Une ligne pour l'humain et pour l'IA
globs: "**/*.sql"                      # active la règle sur ces fichiers seulement
# alwaysApply: true                    # sinon : toujours active (règles transverses)
---

# Titre

- Consignes à l'impératif, concrètes, vérifiables.
```

Comportement des propriétés (doc Continue) : sans `globs`, la règle est toujours incluse ;
avec `globs`, elle ne l'est que si un fichier correspondant est dans le contexte ;
`alwaysApply: true` force l'inclusion partout.

## Anatomie d'un agent

```md
---
name: eco-check                        # obligatoire (la CLI refuse le fichier sinon)
description: Revue écoconception d'un diff
---

Tu es un relecteur spécialisé…
1. points de contrôle…
Pour chaque problème : corrige si sûr et local, sinon décris et cite le critère.
Si conforme, dis-le explicitement et termine.
```

L'agent reçoit le diff et un accès aux fichiers. **Ses éditions sont appliquées
directement au working tree** (comportement CLI v1.5.47).

## Règles d'écriture qui marchent

- **Une consigne = un comportement vérifiable.** « Pagine toute requête sur volume non
  borné » plutôt que « optimise les requêtes ».
- **Des seuils chiffrés** quand c'est possible (« < 500 Ko par page », « max 2 familles
  de polices ») : le modèle s'y conforme mieux et la revue peut trancher.
- **Citer l'identifiant source** (GR491_xxx, Opquast n°xxx, RGESN x.x) : traçabilité et
  pédagogie. Les extractions sont dans `referentiels/`.
- **Nommer les anti-patterns du langage** (`SELECT *`, `.Result`, `parallelStream()`,
  `ToList()` prématuré) : la détection est bien meilleure qu'avec des principes généraux.
- **Sobriété des règles elles-mêmes** : chaque ligne consomme du contexte à chaque
  requête. Découper par langage avec `globs`, élaguer ce qui ne change pas le
  comportement du modèle.

## Tester une modification

La branche `test-eco` contient des fichiers pièges (HTML, SQL, Java, C#) couvrant les
écarts que les agents doivent détecter.

```bash
git checkout test-eco -- exemples/       # ramène les pièges dans le working tree
cn review --review-agents .continue/agents/eco-check.md   # dans un vrai terminal
git diff exemples/                        # ce que l'agent a corrigé
git reset -- exemples/ && rm -rf exemples/                # nettoyage (reset, pas checkout :
                                          # checkout laisserait les fichiers indexés)
```

Vérifiez : les écarts attendus sont-ils détectés ? corrigés correctement ? le critère
source est-il cité ? Si vous ajoutez une consigne à une règle, ajoutez le piège
correspondant dans `exemples/` sur `test-eco`.

## Mesurer l'effet, pas seulement le constater

Deux dispositifs de test coexistent, avec des rôles distincts :

- **`verification/`** (sur `main`) valide qu'une **installation** fonctionne chez un
  utilisateur : 18 écarts volontaires, une grille de résultats attendus, un barème.
- **`test-eco`** valide qu'une **évolution des règles** ne régresse pas chez un
  contributeur : des pièges par langage, à enrichir avec chaque nouvelle consigne.

Une règle reformulée peut dégrader la détection sans que personne s'en aperçoive. Le
scorer donne un chiffre avant/après :

```bash
cn review --review-agents .continue/agents/eco-check.md verification/exemple-a-corriger.* \
  | python3 scripts/scorer-detection.py
```

Le rapprochement est textuel, donc généreux : c'est l'écart entre deux mesures qui
compte, pas le chiffre absolu.

Et si votre consigne porte sur un motif repérable par `grep`, ajoutez-le à
`scripts/eco-audit.sh` : ce qui peut être attrapé sans appeler un modèle doit l'être,
c'est le seul étage qui se déclenche à chaque commit sans rien demander.

## Propager le changement aux 9 autres assistants

`.continue/rules/` et `.continue/agents/` sont la source unique : toute modification
doit être répercutée dans `versions/` (Claude Code, Cursor, GitHub Copilot, Gemini
CLI, OpenCode, Mistral Vibe, Kimi CLI, Codex, ChatGPT) avant de commiter. La CI
échoue si vous l'oubliez.

```bash
python3 scripts/generer-versions.py
```

N'éditez jamais un fichier sous `versions/` directement : il serait écrasé au
prochain lancement du script et divergerait silencieusement de la source à la
prochaine génération faite par quelqu'un d'autre.

## Pièges connus (appris en testant)

- Frontmatter `name:` obligatoire dans les agents, sinon erreur fatale.
- `cn review` (pas `cn check`) : la doc du dépôt amont décrit des commandes qui ne sont
  pas dans le binaire publié ; en cas de doute, `cn --help` fait foi.
- Rapport complet uniquement en TTY ; en non-interactif, fiez-vous à `git diff`.
- Les correctifs du modèle local peuvent être faux : toujours relire (cas observé :
  `.filter()` sur une `List` Java).
