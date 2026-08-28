#!/usr/bin/env bash
# Vérifie qu'un tag de release suit vX.Y.Z et correspond exactement à VERSION.

set -eu

RACINE=$(cd "$(dirname "$0")/.." && pwd)
VERSION_FILE=${VERSION_FILE:-"$RACINE/VERSION"}
TAG=${1:-${GITHUB_REF_NAME:-}}

if [ -z "$TAG" ]; then
  echo "Tag absent. Usage : $0 vX.Y.Z" >&2
  exit 2
fi

if ! printf '%s' "$TAG" | grep -qE '^v[0-9]+\.[0-9]+\.[0-9]+$'; then
  echo "Tag invalide : $TAG (format attendu : vX.Y.Z)." >&2
  exit 1
fi

VERSION=$(tr -d '[:space:]' < "$VERSION_FILE")
if [ "$TAG" != "v$VERSION" ]; then
  echo "Tag $TAG différent de VERSION ($VERSION)." >&2
  exit 1
fi

echo "Tag $TAG cohérent avec VERSION."
