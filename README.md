# BPCE — Skills Numérique Responsable pour Continue

Développement de règles et d'agents [Continue](https://continue.dev) pour améliorer la mise en œuvre des règles d'écoconception (RGESN, GR491) et de numérique responsable (RGAA, RGPD) dans les projets de développement.

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `.continue/rules/` | Règles injectées dans le contexte de l'IA (extension IDE et CLI). Elles orientent le code généré : sobriété, accessibilité, protection des données. |
| `.continue/agents/` | Agents de vérification exécutés par `cn check` sur un diff : écoconception et accessibilité. |
| `continue/` | Clone des sources de Continue (référence et documentation, non versionné ici — voir `.gitignore`). |

## Prérequis

- Node.js ≥ 18
- CLI Continue : `npm install -g @continuedev/cli` (installée : commande `cn`)
- Optionnel : extension Continue pour VS Code ou JetBrains (marketplace), qui lit les mêmes fichiers `.continue/`

## Configuration du modèle (sans API payante)

La CLI publiée (testée en v1.5.47) ne propose plus `cn login` vers le Hub, contrairement à sa doc.
Elle est configurée ici sur un modèle **local via Ollama** (gratuit, aucune donnée ne sort du poste)
dans `~/.continue/config.yaml` :

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

L'extension IDE (VS Code/JetBrains), elle, garde la connexion Hub et son offre gratuite,
et lit le même `.continue/rules/`.

## Utilisation

### 1. Chat / génération de code avec les règles actives

```bash
cn        # session interactive dans ce répertoire ; les règles .continue/rules/ sont chargées
```

### 2. Revue d'un diff (écoconception / accessibilité)

Dans un projet git contenant des changements non commités (testé et validé le 17/07/2026
avec qwen3-coder local — la commande est `cn review`, pas `cn check` comme l'indique
l'ancienne doc) :

```bash
cn review --review-agents .continue/agents/eco-check.md
cn review --review-agents .continue/agents/accessibilite-check.md --verbose
cn review --fix    # applique directement les corrections proposées
```

Pour rejouer le test de référence : `git checkout test-eco -- exemples/` ramène une page
volontairement non sobre, puis `cn review --review-agents .continue/agents/eco-check.md --verbose`.

### 3. Développer un nouveau skill

1. Créer un fichier markdown dans `.continue/rules/` (règle de contexte, avec frontmatter `globs` pour cibler des types de fichiers) ou `.continue/agents/` (agent de vérification).
2. Tester sur un diff réel avec `cn check --agent <fichier>`.
3. Itérer sur la formulation : critères concrets, seuils mesurables, référence au critère RGESN/RGAA.

## Référentiels utilisés

- **RGESN v2** (ARCEP/ARCOM/ADEME, 2024) — Référentiel général d'écoconception de services numériques, 78 critères en 9 thématiques.
- **GR491** (INR) — Guide de référence de conception responsable de services numériques.
- **RGAA 4** — Référentiel général d'amélioration de l'accessibilité.
- **RGPD** — minimisation des données (art. 5).
