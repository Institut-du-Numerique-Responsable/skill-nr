# Guide de déploiement : diffuser les skills aux équipes

Ce guide s'adresse à l'équipe qui pilote la démarche numérique responsable.
Trois canaux complémentaires, à activer dans cet ordre. Il détaille le cas Continue
(source de référence du dépôt) ; si votre équipe est sur un autre assistant, le
canal 1 (dépôts de projet) et le canal 3 (CI) s'appliquent à l'identique en pointant
sur le dossier de [versions/](../versions/README.md) correspondant plutôt que
sur `.continue/`. Cursor et GitHub Copilot méritent une mention particulière : comme
Continue, ils ciblent les règles par type de fichier, donc sans le coût de contexte
des formats à fichier unique.

## 1. Par les dépôts de projet (démarrage, zéro friction)

Continue (extension IDE **et** CLI) charge automatiquement `.continue/rules/*.md` du
dépôt ouvert. Déployer = committer :

1. Ce dépôt (`regles-ecoconception-ia`) fait autorité sur les règles.
2. Copiez le dossier `.continue/` dans chaque dépôt de projet via une merge request
   (revue par l'équipe = adhésion + traçabilité).
3. À chaque évolution des règles ici, resynchronisez les projets (script de copie,
   template de repo, ou MR automatisée).

Tout développeur ayant l'extension Continue bénéficie des règles dès qu'il ouvre le
projet, sans configuration individuelle.

**Avantages** : versionné, relu, fonctionne hors ligne, aucun service externe.
**Limite** : synchronisation multi-dépôts à outiller quand le nombre de projets grandit.

## 2. Par le Hub Continue (passage à l'échelle)

Sur [hub.continue.dev](https://hub.continue.dev) : créer une **organisation**, publier
chaque règle comme *block*, définir un assistant d'organisation qui les référence :

```yaml
rules:
  - uses: rule/ecoconception-frontend
  - uses: rule/qualite-web-opquast
```

Dans ces exemples, `rule` tient la place du slug de votre organisation sur le Hub :
remplacez-le par le vôtre. Ce n'est pas un mot-clé réservé, le type de block est déjà
porté par la clé `rules:` au-dessus.

Les développeurs se connectent une fois dans l'extension IDE et récupèrent l'assistant ;
une mise à jour de block se propage immédiatement à tous.

**Point de vigilance (secteurs réglementés)** : le Hub est un SaaS, à valider avec la
sécurité ; Continue propose des options entreprise/on-premise. Note : la CLI publiée
(v1.5.47) n'a plus d'intégration Hub : ce canal ne concerne que l'extension IDE.

## 3. En CI (le garde-fou)

Les règles orientent la génération ; la CI garantit l'application même sans assistant.
Deux étages, à activer dans cet ordre.

**Le pré-filtre déterministe, d'abord.** Il ne demande aucun modèle, ne coûte rien et
ne produit aucun correctif inventé :

```bash
bash scripts/eco-audit.sh --avertir $(git diff --name-only origin/main...HEAD)
```

C'est le seul étage réellement systématique. Ce dépôt l'utilise sur ses propres PR,
voir `.github/workflows/verification.yml` : un job rejoue les contrôles d'intégrité
(`scripts/verifier-depot.sh`), un autre audite le diff et commente la PR. Sur un poste,
`bash scripts/installer-hooks.sh` pose le même contrôle en `pre-commit`.

**La revue par agent, ensuite**, pour ce que le grep ne voit pas :

```bash
npm i -g @continuedev/cli
cn review --review-agents .continue/agents/eco-check.md
```

Elle a besoin d'un modèle : passerelle LLM interne (endpoint compatible OpenAI dans
`config.yaml`) ou instance Ollama sur le runner. Commencer en mode informatif
(non bloquant), passer en bloquant quand les équipes ont confiance. Mesuré sur le
corpus de `verification/` : un modèle local repère 16 écarts sur 18, mais ne rattache
qu'un seul constat au bon critère et invente des identifiants. À traiter comme un
signal à relire, pas comme un verdict.

## Modèles : recommandations par contexte

| Contexte | Modèle | Remarque |
| --- | --- | --- |
| Poste développeur (IDE) | Compte Continue (gratuit) ou passerelle interne | Le plus simple au quotidien |
| Poste développeur (CLI) | Ollama local (`qwen3-coder`) | Validé sur ce projet ; confidentialité totale |
| CI | Passerelle LLM interne de l'organisation | Cible de production ; clé gérée en secret CI |

Un modèle local est aussi un choix d'écoconception : pas de datacenter sollicité pour
chaque complétion, et une inférence dimensionnée au besoin réel.

## Licences des référentiels

- **GR491** (INR) : citation des recommandations avec attribution, voir conditions sur gr491.isit-europe.org.
- **Opquast** : checklist sous licence **CC BY-SA**, attribution présente dans `referentiels/opquast-ecoconception.md`, à conserver dans toute rediffusion.
- **RGESN, RGAA** : référentiels publics de l'État français.
