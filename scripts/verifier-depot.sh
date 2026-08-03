#!/usr/bin/env bash
# Contrôles d'intégrité du dépôt. Mêmes contrôles en local et en CI :
#
#   bash scripts/verifier-depot.sh
#
# Chaque contrôle est indépendant : le script les exécute tous et sort en 1 si l'un
# d'eux échoue, pour qu'une PR remonte tous ses problèmes d'un coup plutôt qu'un par
# exécution.

set -u
cd "$(dirname "$0")/.." || exit 2

ECHECS=0
titre() { printf '\n\033[1m== %s\033[0m\n' "$1"; }
ok()    { printf '  \033[32m✓\033[0m %s\n' "$1"; }
ko()    { printf '  \033[31m✗\033[0m %s\n' "$1"; ECHECS=$((ECHECS + 1)); }

# --- 1. Les versions générées correspondent-elles à la source ? -----------------
# Le piège numéro un du dépôt : modifier .continue/ sans relancer le générateur.
titre "Versions générées à jour"
if python3 scripts/generer-versions.py >/dev/null 2>&1; then
  if git diff --quiet -- versions/; then
    ok "versions/ correspond à .continue/"
  else
    ko "versions/ diverge de .continue/ : lancez python3 scripts/generer-versions.py et committez"
    git --no-pager diff --stat -- versions/ | sed 's/^/      /'
  fi
else
  ko "scripts/generer-versions.py a échoué"
fi

# --- 2. Toutes les règles sont-elles prises par le générateur ? -----------------
# ORDRE est une liste en dur : une règle absente serait silencieusement perdue.
titre "Aucune règle oubliée par le générateur"
MANQUANTES=0
for f in .continue/rules/*.md; do
  slug=$(basename "$f" .md)
  grep -q "\"$slug\"" scripts/generer-versions.py || { ko "règle absente de ORDRE : $slug"; MANQUANTES=1; }
done
[ "$MANQUANTES" -eq 0 ] && ok "les $(ls .continue/rules/*.md | wc -l | tr -d ' ') règles sont dans ORDRE"

# --- 3. Frontmatter des règles et des agents ------------------------------------
titre "Frontmatter valide"
FM=0
for f in .continue/rules/*.md .continue/agents/*.md; do
  head -1 "$f" | grep -q '^---$' || { ko "$f : pas de frontmatter"; FM=1; }
  grep -q '^name:' "$f" || { ko "$f : champ name manquant"; FM=1; }
  grep -q '^description:' "$f" || { ko "$f : champ description manquant"; FM=1; }
done
[ "$FM" -eq 0 ] && ok "name et description présents partout"

# --- 4. Les critères cités existent-ils vraiment ? ------------------------------
# C'est la promesse centrale du dépôt : un identifiant inventé la casse.
titre "Identifiants de critères vérifiables"
grep -rhoE 'GR491_[A-Za-z]+_[0-9]+' .continue/ versions/ verification/ scripts/ README.md README.en.md docs/ 2>/dev/null | sort -u > /tmp/nr-cites.txt
grep -oE 'GR491_[A-Za-z]+_[0-9]+' referentiels/gr491.md | sort -u > /tmp/nr-reels.txt
INEXISTANTS=$(comm -23 /tmp/nr-cites.txt /tmp/nr-reels.txt)
if [ -n "$INEXISTANTS" ]; then
  echo "$INEXISTANTS" | while read -r i; do ko "GR491 inexistant dans referentiels/ : $i"; done
  ECHECS=$((ECHECS + 1))
else
  ok "$(wc -l < /tmp/nr-cites.txt | tr -d ' ') identifiants GR491 cités, tous présents dans referentiels/"
fi
grep -rhoE 'RGESN [0-9]+\.[0-9]+' .continue/ versions/ verification/ scripts/ README.md README.en.md docs/ 2>/dev/null | sed 's/RGESN //' | sort -u > /tmp/nr-rgesn-cites.txt
grep -oE '^- \*\*RGESN [0-9]+\.[0-9]+' referentiels/rgesn.md | sed 's/^- \*\*RGESN //' | sort -u > /tmp/nr-rgesn-reels.txt
RGESN_KO=$(comm -23 /tmp/nr-rgesn-cites.txt /tmp/nr-rgesn-reels.txt)
if [ -n "$RGESN_KO" ]; then
  echo "$RGESN_KO" | while read -r i; do ko "RGESN $i inexistant dans referentiels/rgesn.md"; done
  ECHECS=$((ECHECS + 1))
else
  ok "$(wc -l < /tmp/nr-rgesn-cites.txt | tr -d ' ') identifiants RGESN cités, tous présents (référentiel : $(wc -l < /tmp/nr-rgesn-reels.txt | tr -d ' ') critères)"
fi
grep -rhoE 'Opquast n°[0-9]+' .continue/ verification/ scripts/ README.md 2>/dev/null | grep -oE '[0-9]+' | sort -u > /tmp/nr-opq-cites.txt
grep -oE '^- [0-9]+ :' referentiels/opquast-ecoconception.md | grep -oE '[0-9]+' | sort -u > /tmp/nr-opq-reels.txt
OPQ=$(comm -23 /tmp/nr-opq-cites.txt /tmp/nr-opq-reels.txt)
if [ -n "$OPQ" ]; then
  echo "$OPQ" | while read -r i; do ko "Opquast n°$i absent de l'extraction"; done
  ECHECS=$((ECHECS + 1))
else
  ok "numéros Opquast cités tous présents dans l'extraction"
fi

# --- 5. Liens relatifs -----------------------------------------------------------
titre "Liens relatifs"
CASSES=0
for f in $(git ls-files '*.md' | grep -v '^continue/'); do
  d=$(dirname "$f")
  while read -r l; do
    p="${l%%#*}"; [ -z "$p" ] && continue
    [ -e "$d/$p" ] || { ko "$f → $l"; CASSES=1; }
  done < <(grep -o '](\([^)#h][^)]*\))' "$f" | sed 's/](//;s/)$//')
done
[ "$CASSES" -eq 0 ] && ok "aucun lien relatif cassé"

# --- 6. Syntaxe des scripts ------------------------------------------------------
titre "Syntaxe des scripts"
SYN=0
for s in scripts/*.sh; do bash -n "$s" || { ko "$s"; SYN=1; }; done
for s in scripts/*.py; do python3 -m py_compile "$s" 2>/dev/null || { ko "$s"; SYN=1; }; done
rm -rf scripts/__pycache__
[ "$SYN" -eq 0 ] && ok "bash -n et py_compile passent"

# --- 7. Corpus de vérification cohérent ------------------------------------------
titre "Corpus de vérification"
N_JSON=$(python3 -c "import json;print(len(json.load(open('verification/attendus.json'))['ecarts']))")
N_MD=$(grep -oE 'totalisent \*\*[0-9]+ écarts\*\*' verification/resultats-attendus.md | grep -oE '[0-9]+')
if [ "$N_JSON" = "$N_MD" ]; then
  ok "attendus.json et resultats-attendus.md annoncent $N_JSON écarts"
else
  ko "attendus.json ($N_JSON écarts) et resultats-attendus.md ($N_MD) divergent"
fi
SCORE=$(bash scripts/eco-audit.sh verification/exemple-a-corriger.html verification/exemple-a-corriger.sql \
        | python3 scripts/scorer-detection.py --json | python3 -c "import json,sys;print(json.load(sys.stdin)['detectes'])")
if [ "$SCORE" -ge 10 ]; then
  ok "le pré-filtre détecte $SCORE/$N_JSON écarts du corpus (seuil : 10)"
else
  ko "le pré-filtre ne détecte que $SCORE/$N_JSON écarts : régression des motifs"
fi

# --- 8. Pré-filtre sur le dépôt lui-même -----------------------------------------
# Le dépôt applique les règles qu'il promeut (les pièges de verification/ exclus).
titre "Pré-filtre écoconception sur le dépôt"
if bash scripts/eco-audit.sh >/tmp/nr-audit.txt 2>&1; then
  ok "$(tail -2 /tmp/nr-audit.txt | head -1)"
else
  ko "constats élevés sur le dépôt lui-même"
  cat /tmp/nr-audit.txt | sed 's/^/      /'
fi

printf '\n'
if [ "$ECHECS" -eq 0 ]; then
  echo "Tous les contrôles passent."
  exit 0
fi
echo "$ECHECS contrôle(s) en échec."
exit 1
