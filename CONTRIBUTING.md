# Contribuer

Merci de vouloir améliorer ces règles Numérique Responsable. Elles sont écrites une
fois au format Continue et déclinées pour dix assistants : une contribution profite
donc à tous les outils d'un coup.

## Le flux

Tout passe par une branche et une pull request, y compris pour les mainteneurs.

```bash
bash scripts/installer-hooks.sh          # une fois par clone
git switch -c regle/mon-sujet
# ... vos modifications ...
bash scripts/verifier-depot.sh           # les contrôles de la CI, en local
git push -u origin regle/mon-sujet
gh pr create
```

Les hooks installés refusent un push direct sur `main` et lancent le pré-filtre
écoconception avant chaque commit. Ils donnent un retour rapide en local ; la branche
`main` est également protégée sur GitHub et exige une pull request approuvée ainsi que
la réussite du contrôle d'intégrité.

La CI rejoue les mêmes contrôles sur chaque PR (`.github/workflows/verification.yml`)
et commente le résultat du pré-filtre sur les fichiers modifiés.

Les échanges de revue doivent être résolus avant fusion. Les mainteneurs privilégient
le squash merge et suppriment la branche une fois la PR fusionnée.

## Proposer une règle ou un agent

1. Lisez [docs/developper-un-skill.md](docs/developper-un-skill.md) : anatomie des règles
   et des agents, principes d'écriture, pièges connus.
2. Une consigne = un comportement vérifiable, avec l'identifiant du critère source
   (GR491_xxx, Opquast n°xxx, RGESN x.x). Pas de généralités (« optimiser », « alléger »)
   sans anti-pattern nommé ou seuil chiffré.
3. Ciblez le bon fichier : règle par langage (`ecoconception-<langage>.md` avec `globs`),
   principe transverse (`ecoconception-backend.md`, `numerique-responsable.md`),
   ou point de contrôle de revue (`.continue/agents/eco-check.md`).

## Tester avant de soumettre

La branche `test-eco` contient des fichiers pièges par langage :

```bash
git checkout test-eco -- exemples/
cn review --review-agents .continue/agents/eco-check.md   # dans un vrai terminal
git diff exemples/          # vérifier détection et qualité des correctifs
git reset -- exemples/ && rm -rf exemples/   # reset et non checkout : sinon l'index
                                             # garde des suppressions fantômes
```

Toute nouvelle consigne dans une règle doit s'accompagner du piège correspondant
dans `exemples/` (commité sur `test-eco`).

### Mesurer l'effet de votre changement

Une règle reformulée peut améliorer ou dégrader la détection sans qu'on s'en aperçoive.
Le corpus de `verification/` et son scorer donnent un chiffre avant/après :

```bash
cn review --review-agents .continue/agents/eco-check.md verification/exemple-a-corriger.* \
  | python3 scripts/scorer-detection.py
```

Indiquez le score avant et après dans la PR. Si votre consigne porte sur un motif
détectable par `grep`, ajoutez-le aussi à `scripts/eco-audit.sh` : ce qui peut être
attrapé sans appeler un modèle doit l'être.

## Conventions

- Tout le contenu est rédigé en **français**, consignes à l'impératif.
- Frontmatter obligatoire : `name` + `description` (+ `globs` pour les règles ciblées).
- Une PR = un sujet (un langage, une thématique, ou une correction).
- Indiquez dans la PR : critère(s) source(s), et le résultat du test sur `test-eco`.

## Licence des contributions

En contribuant, vous acceptez que votre contribution soit distribuée sous la licence
du dépôt (CC BY-SA 4.0, voir [LICENSE.md](LICENSE.md)).
