# Règles Numérique Responsable pour Continue

Règles et agents [Continue](https://continue.dev) pour appliquer l'écoconception (RGESN, GR491, Opquast) et le numérique responsable (RGAA, RGPD) directement dans le flux de développement assisté par IA.

**Langages couverts** : SQL/PL-SQL, HTML, CSS, JavaScript, TypeScript, Java, C#, Python, PHP, Ruby, Rust, C, C++ — chaque règle ne s'active que sur les fichiers de son langage (`globs`).

**Deux mécanismes complémentaires** :
- les **règles** (`.continue/rules/`) orientent le code que l'IA génère — prévention ;
- les **agents** (`.continue/agents/`) relisent les diffs sous l'angle écoconception et accessibilité — contrôle.

Licence : CC BY-SA 4.0 (voir [LICENSE.md](LICENSE.md)) · Contributions : [CONTRIBUTING.md](CONTRIBUTING.md)

## Documentation

- [Guide développeur](docs/guide-developpeur.md) — installer, utiliser au quotidien, lancer une revue, dépanner.
- [Guide de déploiement](docs/guide-deploiement.md) — diffuser les skills aux équipes (git, Hub, CI), choix des modèles, licences.
- [Développer un skill](docs/developper-un-skill.md) — écrire une règle ou un agent, les tester, pièges connus.

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `.continue/rules/` | Règles injectées dans le contexte de l'IA (extension IDE et CLI). Elles orientent le code généré : sobriété, accessibilité, protection des données. Ciblées par langage (SQL, JavaScript, Java, C#) via `globs`. |
| `.continue/agents/` | Agents de revue de diff exécutés par `cn review` : écoconception et accessibilité. |
| `referentiels/` | Extractions sourcées des référentiels (GR491, Opquast) avec identifiants cités par les règles. |
| `docs/` | Guides développeur, déploiement et contribution. |
| `continue/` | Clone des sources de Continue (référence et documentation, non versionné ici — voir `.gitignore`). |
| branche `test-eco` | Fichiers pièges (`exemples/`) pour valider les agents après chaque évolution des règles. |

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
- **GR491** (INR) — 8 familles, 61 recommandations, 516 critères ; extraction des recommandations avec identifiants dans `referentiels/gr491.md`.
- **Opquast** — checklist « Assurance qualité numérique » (CC BY-SA) ; les 35 règles taguées écoconception (phases conception/développement/éditorial) sont extraites dans `referentiels/opquast-ecoconception.md` et portées par la règle `.continue/rules/qualite-web-opquast.md`.
- **RGAA 4** — Référentiel général d'amélioration de l'accessibilité.
- **RGPD** — minimisation des données (art. 5).

Les règles `.continue/rules/` citent les identifiants (GR491_xxx, Opquast n°xxx) pour tracer chaque consigne vers sa source.
