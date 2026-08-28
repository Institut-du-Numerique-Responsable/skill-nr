#!/usr/bin/env bash

set -eu

RACINE=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

printf '1.2.3\n' > "$TMP/VERSION"

VERSION_FILE="$TMP/VERSION" bash "$RACINE/scripts/verifier-version-release.sh" v1.2.3 >/dev/null

if VERSION_FILE="$TMP/VERSION" bash "$RACINE/scripts/verifier-version-release.sh" v1.2.4 >/dev/null 2>&1; then
  echo "Échec : un tag différent de VERSION a été accepté."
  exit 1
fi

if VERSION_FILE="$TMP/VERSION" bash "$RACINE/scripts/verifier-version-release.sh" release-1.2.3 >/dev/null 2>&1; then
  echo "Échec : un tag hors format vX.Y.Z a été accepté."
  exit 1
fi

echo "Test release : format et concordance du tag vérifiés."
