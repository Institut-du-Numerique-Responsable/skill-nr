# Publier une version

Cette procédure publie une version stable `vX.Y.Z`. Le numéro suit le
[versionnement sémantique](https://semver.org/lang/fr/) et sa source de vérité est le
fichier `VERSION`.

## 1. Préparer la version dans une pull request

Depuis une branche dédiée :

1. modifier `VERSION` avec le numéro sans préfixe `v` ;
2. ajouter la section correspondante dans `CHANGELOG.md` ;
3. aligner `version` et `date-released` dans `CITATION.cff` ;
4. aligner `softwareVersion` dans `docs/index.html` et `docs/en/index.html` ;
5. exécuter `bash scripts/verifier-depot.sh` ;
6. ouvrir une pull request et attendre le contrôle `Intégrité du dépôt`, une
   approbation CODEOWNERS et la résolution des échanges.

Le contrôle local échoue si ces métadonnées divergent.

## 2. Créer et vérifier le tag

Après la fusion de la PR, mettre `main` à jour puis créer un tag annoté :

```bash
git switch main
git pull --ff-only
VERSION=$(tr -d '[:space:]' < VERSION)
bash scripts/verifier-version-release.sh "v$VERSION"
git tag -a "v$VERSION" -m "skill-nr $VERSION"
git push origin "v$VERSION"
```

Le hook `pre-push` refuse un tag différent de `VERSION`. GitHub Actions rejoue le
même contrôle sur tout tag `v*`. Ne créez pas la release si ce contrôle échoue ;
supprimez le tag erroné, corrigez les métadonnées par PR, puis recréez-le.

## 3. Publier la release GitHub

Quand le workflow du tag est vert :

```bash
VERSION=$(tr -d '[:space:]' < VERSION)
gh release create "v$VERSION" \
  --verify-tag \
  --title "skill-nr $VERSION" \
  --notes-file CHANGELOG.md
```

Vérifier ensuite que la release est publique, non marquée comme préversion et que le
badge de version du README pointe vers cette release.

## En cas d’erreur

- Avant publication de la release : supprimer uniquement le tag erroné, puis reprendre
  à l’étape 1. Ne jamais déplacer silencieusement un tag déjà publié.
- Après publication : conserver le tag et publier une version corrective avec un
  nouveau numéro.
