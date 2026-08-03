# Vérifier que les règles sont bien en place

Copier des fichiers ne suffit pas à savoir si l'assistant les lit vraiment. Un mauvais
emplacement, un `AGENTS.md` écrasé par celui du projet, une extension non rechargée : rien
ne le signale, l'assistant répond normalement, simplement sans les règles.

Cette vérification se fait en deux étapes : les fichiers sont-ils là (mécanique), et
l'assistant s'en sert-il (comportement).

## Étape 1 : les fichiers sont en place

Depuis la racine du projet où vous avez installé les règles :

```bash
bash /chemin/vers/regles-ecoconception-ia/scripts/verifier-installation.sh
```

Le script détecte les outils présents et contrôle chaque fichier attendu. Pour cibler un
outil précis, ou vérifier un projet distant :

```bash
bash scripts/verifier-installation.sh claude-code /chemin/vers/mon-projet
bash scripts/verifier-installation.sh opencode    /chemin/vers/mon-projet
```

Outils reconnus : `continue`, `claude-code`, `gemini-cli`, `opencode`, `mistral-vibe`,
`kimi-cli`, `codex`, `chatgpt`. Le script sort en code 1 si un fichier manque.

Il contrôle aussi le contenu, pas seulement le nom : un `AGENTS.md` qui existe mais ne
contient pas les règles est signalé comme tel. C'est le cas le plus fréquent, quand le
projet avait déjà son propre `AGENTS.md` et que la copie l'a écrasé ou l'inverse.

## Étape 2 : l'assistant applique bien les règles

Copiez les deux fichiers de test dans le projet à tester, puis demandez une relecture.

```bash
cp /chemin/vers/regles-ecoconception-ia/verification/exemple-a-corriger.* .
```

Ouvrez votre assistant dans ce projet et demandez :

> Relis `exemple-a-corriger.html` et `exemple-a-corriger.sql` sous l'angle écoconception
> et accessibilité. Liste les écarts et cite le critère source pour chacun.

Ou lancez directement l'agent de revue de votre outil :

| Outil | Commande |
| --- | --- |
| Continue | `cn review --review-agents .continue/agents/eco-check.md` |
| Claude Code | « lance l'agent eco-check sur ces deux fichiers » |
| Gemini CLI | `/eco-check` |
| OpenCode | mentionner l'agent `eco-check` |
| Mistral Vibe | `vibe --agent eco-check` |
| Kimi CLI | `kimi --agent-file .kimi/agents/eco-check.yaml` |

Comparez ensuite la réponse à [`resultats-attendus.md`](resultats-attendus.md), qui liste
les 18 écarts volontaires des deux fichiers avec leurs critères.

Pour ne pas comparer à la main, passez le rapport au scorer :

```bash
cn review --review-agents .continue/agents/eco-check.md | python3 scripts/scorer-detection.py
python3 scripts/scorer-detection.py rapport-colle.txt        # ou depuis un fichier
```

Il rapproche le rapport de `attendus.json` et sort le nombre d'écarts détectés, le
nombre de critères cités, et lesquels manquent. Le rapprochement est textuel, donc
généreux : le chiffre absolu vaut moins que son évolution entre deux états des règles.
C'est ce qui permet de dire « cette reformulation fait passer la détection de 11 à 15
sur 18 » au lieu de s'en remettre à une impression.

**Barème** : 10 écarts sur 18 relevés, dont au moins 3 avec un critère cité (RGESN, GR491,
Opquast, RGAA), c'est une installation qui fonctionne. En dessous de 5, ou si aucun critère
n'est jamais cité, les règles ne sont pas chargées : reprenez l'étape 1.

Le signe le plus fiable n'est pas le nombre d'écarts, c'est la **citation des critères**.
N'importe quel modèle correct dira qu'une image manque d'`alt` ; seul un modèle qui a les
règles en contexte écrira « Opquast n°124 » ou « GR491_Backend_3 ».

## Étape 3 : la prévention, pas seulement la revue

Le plus important n'est pas la revue de diff mais ce que l'assistant écrit spontanément.
Dans le projet équipé, demandez, sans autre précision :

> Écris-moi une requête SQL qui liste les commandes des clients d'une région.

> Écris-moi un composant HTML de galerie d'images.

Sans les règles, vous obtiendrez typiquement un `SELECT *` sans pagination et des `<img>`
nues. Avec les règles chargées, la requête projette ses colonnes et pagine, les images
arrivent en `loading="lazy"` avec `width`/`height` et `alt`, et l'assistant mentionne le
critère qu'il applique. Cette différence-là est la vraie preuve d'installation.

## Après le test

Les fichiers de test sont volontairement non conformes : ne les corrigez pas et ne les
laissez pas dans votre projet.

```bash
rm exemple-a-corriger.html exemple-a-corriger.sql
```

Si vous les avez testés depuis ce dépôt et qu'un agent les a modifiés en place (`cn review`
et les agents en mode écriture appliquent leurs correctifs directement) :

```bash
git checkout -- verification/
```
