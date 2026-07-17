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

## Utilisation

### 1. Chat / génération de code avec les règles actives

```bash
cn        # session interactive dans ce répertoire ; les règles .continue/rules/ sont chargées
cn login  # authentification (une seule fois) pour accéder aux modèles via le Hub Continue
```

Il est aussi possible de configurer ses propres clés de modèles dans `~/.continue/config.yaml` (voir la doc `continue/docs/`).

### 2. Vérification d'un diff (revue écoconception / accessibilité)

Dans un projet git contenant des changements :

```bash
cn check --agent .continue/agents/eco-check.md
cn check --agent .continue/agents/accessibilite-check.md
cn check --fix    # applique directement les corrections proposées
```

### 3. Développer un nouveau skill

1. Créer un fichier markdown dans `.continue/rules/` (règle de contexte, avec frontmatter `globs` pour cibler des types de fichiers) ou `.continue/agents/` (agent de vérification).
2. Tester sur un diff réel avec `cn check --agent <fichier>`.
3. Itérer sur la formulation : critères concrets, seuils mesurables, référence au critère RGESN/RGAA.

## Référentiels utilisés

- **RGESN v2** (ARCEP/ARCOM/ADEME, 2024) — Référentiel général d'écoconception de services numériques, 78 critères en 9 thématiques.
- **GR491** (INR) — Guide de référence de conception responsable de services numériques.
- **RGAA 4** — Référentiel général d'amélioration de l'accessibilité.
- **RGPD** — minimisation des données (art. 5).
