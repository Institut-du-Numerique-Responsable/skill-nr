# Guide de déploiement : diffuser les skills aux équipes

Ce guide s'adresse à l'équipe qui pilote la démarche numérique responsable.
Trois canaux complémentaires, à activer dans cet ordre. Il détaille le cas Continue
(source de référence du dépôt) ; si votre équipe est sur un autre assistant, le
canal 1 (dépôts de projet) et le canal 3 (CI) s'appliquent à l'identique en pointant
sur le dossier de [versions/](../versions/README.md) correspondant plutôt que
sur `.continue/`.

## 1. Par les dépôts de projet (démarrage, zéro friction)

Continue (extension IDE **et** CLI) charge automatiquement `.continue/rules/*.md` du
dépôt ouvert. Déployer = committer :

1. Ce dépôt (`bpce_skillnr`) fait autorité sur les règles.
2. Copiez le dossier `.continue/` dans chaque dépôt de projet via une merge request
   (revue par l'équipe = adhésion + traçabilité).
3. À chaque évolution des règles ici, resynchronisez les projets (script de copie,
   template de repo, ou MR automatisée).

Tout développeur ayant l'extension Continue bénéficie des règles dès qu'il ouvre le
projet, sans configuration individuelle.

**Avantages** : versionné, relu, fonctionne hors ligne, aucun service externe.
**Limite** : synchronisation multi-dépôts à outiller quand le nombre de projets grandit.

## 2. Par le Hub Continue (passage à l'échelle)

Sur [hub.continue.dev](https://hub.continue.dev) : créer une **organisation** (ex.
`bpce`), publier chaque règle comme *block* (`bpce/ecoconception-sql`, …), définir un
assistant d'organisation qui les référence :

```yaml
rules:
  - uses: bpce/ecoconception-frontend
  - uses: bpce/qualite-web-opquast
```

Les développeurs se connectent une fois dans l'extension IDE et récupèrent l'assistant ;
une mise à jour de block se propage immédiatement à tous.

**Point de vigilance (secteurs réglementés)** : le Hub est un SaaS, à valider avec la
sécurité ; Continue propose des options entreprise/on-premise. Note : la CLI publiée
(v1.5.47) n'a plus d'intégration Hub : ce canal ne concerne que l'extension IDE.

## 3. En CI (le garde-fou)

Les règles orientent la génération ; la CI garantit l'application même sans assistant.
Sur chaque MR (GitLab CI / GitHub Actions) :

```bash
npm i -g @continuedev/cli
cn review --review-agents .continue/agents/eco-check.md
```

La CI a besoin d'un modèle : passerelle LLM interne (endpoint compatible OpenAI dans
`config.yaml`) ou instance Ollama sur le runner. Commencer en mode informatif
(non bloquant), passer en bloquant quand les équipes ont confiance.

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
