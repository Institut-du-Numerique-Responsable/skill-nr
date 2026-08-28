#!/usr/bin/env bash

set -eu

RACINE=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

printf '<img src="test.webp">\n' > "$TMP/--help.html"
printf 'SELECT * FROM produits;\n' > "$TMP/fichier avec espaces.sql"
printf 'SELECT * FROM commandes;\n' > "$TMP/[motif].sql"

RAPPORT=$(cd "$TMP" && bash "$RACINE/scripts/eco-audit.sh" --avertir -- \
  "--help.html" "fichier avec espaces.sql" "[motif].sql")

printf '%s\n' "$RAPPORT" | grep -Fq -- '--help.html:1 [Élevé]'
printf '%s\n' "$RAPPORT" | grep -Fq -- 'fichier avec espaces.sql:1 [Élevé]'
printf '%s\n' "$RAPPORT" | grep -Fq -- '[motif].sql:1 [Élevé]'

echo "Test eco-audit : noms de fichiers sûrs."
