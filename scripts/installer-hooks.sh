#!/usr/bin/env bash
# Installe les garde-fous git locaux :
#
#   pre-commit : pré-filtre écoconception sur les fichiers indexés
#   pre-push   : refuse un push direct sur main et lance les contrôles d'intégrité
#
#   bash scripts/installer-hooks.sh
#
# Pourquoi côté client : ces hooks donnent un retour immédiat avant la CI. Ils
# complètent la protection de branche côté GitHub, mais restent locaux à chaque clone
# et peuvent être contournés avec --no-verify.

set -u
cd "$(dirname "$0")/.." || exit 2

RACINE=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "Pas dans un dépôt git."; exit 2; }
HOOKS="$RACINE/.git/hooks"

# Les corps de hook sont dans des heredocs entre quotes : rien n'y est interprété à
# l'installation, tout l'est à l'exécution du hook.
lire_pre_commit() {
  cat <<'HOOK'
#!/usr/bin/env bash
# Posé par scripts/installer-hooks.sh
RACINE=$(git rev-parse --show-toplevel)
if ! bash "$RACINE/scripts/eco-audit.sh"; then
  echo
  echo "Constats élevés du pré-filtre écoconception."
  echo "Corrigez, ou committez avec --no-verify."
  exit 1
fi
HOOK
}

lire_pre_push() {
  cat <<'HOOK'
#!/usr/bin/env bash
# Posé par scripts/installer-hooks.sh
RACINE=$(git rev-parse --show-toplevel)
BRANCHE=$(git rev-parse --abbrev-ref HEAD)

if [ "$BRANCHE" = "main" ]; then
  echo "Push direct sur main."
  echo "Le flux du depot passe par une branche et une pull request :"
  echo "    git switch -c regle/mon-sujet"
  echo "    git push -u origin regle/mon-sujet"
  echo "    gh pr create"
  echo "Pour outrepasser : git push --no-verify"
  exit 1
fi

if ! bash "$RACINE/scripts/verifier-depot.sh"; then
  echo
  echo "Controles en echec : la CI refusera aussi. Corrigez avant de pousser."
  exit 1
fi
HOOK
}

installer() {
  local nom="$1"
  local cible="$HOOKS/$nom"
  if [ -e "$cible" ] && ! grep -q "installer-hooks.sh" "$cible" 2>/dev/null; then
    echo "  ! $nom existe déjà et n'a pas été posé par ce script : laissé intact."
    echo "    Ajoutez-y l'appel à la main si vous le souhaitez."
    return
  fi
  "lire_${nom//-/_}" > "$cible"
  chmod +x "$cible"
  echo "  ✓ $nom"
}

installer pre-commit
installer pre-push

echo
echo "Hooks installés dans .git/hooks/, locaux à ce clone et non versionnés."
echo "Désinstaller : rm .git/hooks/pre-commit .git/hooks/pre-push"
