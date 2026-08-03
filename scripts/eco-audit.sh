#!/usr/bin/env bash
# Pré-filtre écoconception déterministe : grep sur des motifs connus, zéro appel modèle.
#
#   bash scripts/eco-audit.sh [options] [fichiers...]
#
#   sans fichier            audite les fichiers indexés (git diff --cached), sinon
#                           tous les fichiers suivis
#   --tout                  ajoute les motifs à faible précision (bruyants, réservés à
#                           un audit ponctuel, pas à un hook)
#   --avertir               n'échoue jamais (code 0), pour un premier déploiement
#   --installer-hook        installe .git/hooks/pre-commit qui appelle ce script
#   --motifs                affiche la table des motifs et sort
#
# Ce script ne remplace ni un linter ni la revue par un agent : il attrape les motifs
# évidents avant qu'un modèle soit sollicité, de façon reproductible et sans faux
# correctif. Ce qu'il ne voit pas (sobriété fonctionnelle, rétention effective,
# pertinence d'une dépendance) reste du ressort des règles et des agents.
#
# Par défaut, seuls les constats « Élevé » font échouer la commande.

set -u

TOUT=0
AVERTIR=0

# Table des motifs, champs séparés par « § » (le caractère ne doit apparaître ni dans
# une regex ni dans un message) :
#
#   EXTENSIONS § NIVEAU § PRÉCISION § REGEX § EXCLUSION § MESSAGE § CRITÈRE
#
# PRÉCISION : « haute » = actif par défaut, « basse » = seulement avec --tout.
# EXCLUSION : regex facultative ; une ligne qui y correspond n'est pas signalée
#             (grep n'a pas d'assertion négative portable).
# Contraintes de portabilité : ERE POSIX uniquement, pas de lookahead, pas de « \b »
# (absent de certains grep). Les identifiants cités existent dans referentiels/.
lire_motifs() {
  cat <<'TABLE'
html,htm,jsx,tsx,vue,svelte§Élevé§haute§<img[ >]§alt=.*(loading|width)§Image : vérifier alt, width/height, loading="lazy" et format moderne§RGAA 1.1, GR491_UXUI_8
html,htm,jsx,tsx,vue,svelte§Élevé§haute§<(video|audio)[^>]*autoplay§§Média en lecture automatique§Opquast n°124, Opquast n°125
html,htm,jsx,tsx,vue,svelte§Élevé§haute§<iframe§loading=§Iframe tierce chargée d'office : façade cliquable ou loading="lazy"§GR491_Contenus_3, GR491_Frontend_9
html,htm,jsx,tsx,vue,svelte§Élevé§haute§<(div|span)[^>]*onclick§§Élément cliquable non natif : inatteignable au clavier, utiliser <button>§RGAA 7.1, GR491_UXUI_4
html,htm,jsx,tsx,vue,svelte§Moyen§haute§<input§type=["'](hidden|submit|button)|aria-label|<label§Champ de formulaire : vérifier le label associé§RGAA 11.1
html,htm§Moyen§haute§<link[^>]*rel=["'](stylesheet|preload)["'][^>]*href=["']https?://§§Feuille de style ou police distante : héberger localement, sous-ensemble de caractères§GR491_Frontend_9, GR491_UXUI_8
html,htm,js,jsx,ts,tsx,mjs,cjs§Élevé§haute§(jquery|lodash|moment)(\.min)?\.js§§Librairie lourde là où les API natives suffisent§GR491_Frontend_9
html,htm,js,jsx,ts,tsx,mjs,cjs§Élevé§haute§setInterval[[:space:]]*\(§§Scrutation périodique : rafraîchissement à la demande, WebSocket ou SSE§GR491_Frontend_10, GR491_Backend_3
css,scss§Moyen§haute§@import[[:space:]]§§@import en cascade : sérialise les téléchargements§Opquast n°229
css,scss§Moyen§basse§animation(-name)?[[:space:]]*:§§Animation : n'animer que transform et opacity, respecter prefers-reduced-motion§GR491_Contenus_3
sql,pks,pkb,prc,fnc,trg§Élevé§haute§select[[:space:]]+\*§§SELECT * : lister les colonnes réellement lues§GR491_Backend_3
sql,pks,pkb,prc,fnc,trg§Élevé§haute§(where|and|or)[^;]*(upper|lower|year|trunc|to_char|cast|convert)[[:space:]]*\(§§Prédicat non sargable : fonction sur une colonne, l'index ne peut pas servir§GR491_Backend_4
sql,pks,pkb,prc,fnc,trg§Élevé§haute§like[[:space:]]+'%§§LIKE avec joker initial : parcours complet de la table§GR491_Backend_4
sql,pks,pkb,prc,fnc,trg§Moyen§haute§offset[[:space:]]+[0-9:$]§§Pagination par OFFSET : coût croissant, préférer une pagination par curseur§GR491_Backend_1
sql,pks,pkb,prc,fnc,trg§Moyen§haute§create[[:space:]]+table§§Nouvelle table : prévoir une politique de rétention et de purge§GR491_Backend_1, GR491_Backend_5
sql,pks,pkb,prc,fnc,trg§Moyen§basse§select[[:space:]]+distinct§§DISTINCT masquant souvent une jointure trop large§GR491_Backend_3
js,jsx,ts,tsx,mjs,cjs§Élevé§haute§(from[[:space:]]+["'](lodash|moment)["']|require\(["'](lodash|moment)["']\))§§Librairie entière importée : API natives ou import ciblé§GR491_Frontend_9
js,jsx,ts,tsx,mjs,cjs§Élevé§basse§import[[:space:]]+\*[[:space:]]+as[[:space:]]+§§Import global : empêche le tree-shaking§GR491_Frontend_9
js,jsx,ts,tsx,mjs,cjs§Moyen§haute§fs\.[a-zA-Z]+Sync[[:space:]]*\(§§API synchrone : bloque la boucle d'événements§GR491_Backend_4
js,jsx,ts,tsx,mjs,cjs§Moyen§haute§addEventListener\([[:space:]]*["'](scroll|resize|mousemove|input|pointermove)["']§debounce|throttle§Événement à haute fréquence sans debounce ni throttle§GR491_Frontend_10
java§Élevé§haute§\.findAll\([[:space:]]*\)§§findAll() sans pagination sur un volume non borné§GR491_Backend_1
java§Élevé§haute§\.parallelStream\(\)§§parallelStream() injustifié : coût de parallélisation supérieur au gain§GR491_Backend_4
java§Moyen§haute§static[[:space:]]+(final[[:space:]]+)?(Map|HashMap|ConcurrentHashMap)§§Cache statique non borné : prévoir taille maximale et expiration§GR491_Backend_1
java§Moyen§basse§@OneToMany§JOIN FETCH|EntityGraph§Association lazy : vérifier l'absence de N+1, utiliser JOIN FETCH§GR491_Backend_4
cs§Élevé§haute§\.(Result[^a-zA-Z]|Wait\(\))§§Attente bloquante sur une tâche : mobilise un thread pour rien§GR491_Backend_4
cs§Élevé§haute§new[[:space:]]+HttpClient[[:space:]]*\(§§HttpClient instancié par requête : épuise les sockets, utiliser IHttpClientFactory§GR491_Backend_2
cs§Moyen§haute§\.Include\(§AsNoTracking§Lecture EF Core : vérifier AsNoTracking() et la projection des colonnes§GR491_Backend_3
cs§Moyen§basse§\.ToList\(\)§§Matérialisation possiblement prématurée d'un IQueryable§GR491_Backend_3
py§Élevé§haute§for[[:space:]]+[a-zA-Z_]+[[:space:]]+in[[:space:]]+[a-zA-Z_]+\.objects\.(all|filter)\(§§Requête N+1 sur un queryset parcouru : select_related / prefetch_related§GR491_Backend_4
py§Élevé§haute§\.objects\.all\(\)§§Queryset non borné matérialisé : paginer§GR491_Backend_1
py§Élevé§haute§\.iterrows\(\)§§pandas : boucle ligne à ligne au lieu d'une opération vectorisée§GR491_Backend_4
py§Moyen§haute§(\.read\(\)|\.readlines\(\))§§Fichier lu intégralement en mémoire : préférer un flux§GR491_Backend_4
py§Moyen§basse§requests\.(get|post|put|patch|delete)\(§Session\(\)§Connexion HTTP non réutilisée : utiliser requests.Session§GR491_Backend_2
php§Élevé§haute§foreach[[:space:]]*\([[:space:]]*\$[a-zA-Z_]+->§§Association parcourue en boucle : risque de N+1, précharger avec with()§GR491_Backend_4
php§Moyen§haute§file_get_contents[[:space:]]*\(§§Fichier ou URL chargé intégralement en mémoire§GR491_Backend_4
php§Moyen§basse§(in_array\(|array_search\()§§Recherche linéaire répétée : indexer par clé§GR491_Backend_4
rb§Élevé§haute§\.all\.(each|map|select)§§Table entière chargée en mémoire : find_each ou pagination§GR491_Backend_1
rb§Moyen§haute§\.count[[:space:]]*>[[:space:]]*0§§Comptage complet là où exists? suffit§GR491_Backend_3
rb§Moyen§basse§\.map\(&:§§Objets complets chargés pour une seule colonne : pluck§GR491_Backend_3
rs§Élevé§haute§(std::thread::sleep|\.block_on\()§§Appel bloquant dans un contexte async§GR491_Backend_4
rs§Moyen§basse§\.clone\(\)§§clone() de confort : vérifier qu'un emprunt ne suffit pas§GR491_Backend_4
c,h§Élevé§haute§for[[:space:]]*\([^;]*;[^;]*strlen[[:space:]]*\(§§strlen() dans la condition de boucle : parcours répété§GR491_Backend_4
c,h§Élevé§haute§while[[:space:]]*\([[:space:]]*(1|true)[[:space:]]*\)§§Attente active : consomme un cœur en continu§GR491_Backend_4
cpp,cc,cxx,hpp,hh§Élevé§haute§while[[:space:]]*\([[:space:]]*(1|true)[[:space:]]*\)§§Attente active : consomme un cœur en continu§GR491_Backend_4
cpp,cc,cxx,hpp,hh§Moyen§haute§\([[:space:]]*std::(string|vector<[^>]*>)[[:space:]]+[a-zA-Z_]+[,)]§const &|string_view§Objet lourd passé par valeur : préférer const& ou string_view§GR491_Backend_4
TABLE
}

usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; }

FICHIERS=()
EXPLICITE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --tout) TOUT=1 ;;
    --avertir) AVERTIR=1 ;;
    --motifs)
      lire_motifs | awk -F'§' '{printf "  [%-5s/%s] %-30s %s\n", $2, $3, $1, $6}'; exit 0 ;;
    --installer-hook)
      RACINE=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "Pas dans un dépôt git."; exit 2; }
      HOOK="$RACINE/.git/hooks/pre-commit"
      if [ -e "$HOOK" ]; then echo "$HOOK existe déjà : ajoutez-y l'appel à la main."; exit 2; fi
      cat > "$HOOK" <<'HOOKEOF'
#!/usr/bin/env bash
# Installé par scripts/eco-audit.sh --installer-hook
exec bash "$(git rev-parse --show-toplevel)/scripts/eco-audit.sh"
HOOKEOF
      chmod +x "$HOOK"
      echo "Hook installé : $HOOK"
      echo "Il bloque le commit sur un constat « Élevé ». Contourner : git commit --no-verify"
      exit 0 ;;
    -h|--aide|--help) usage; exit 0 ;;
    -*) echo "Option inconnue : $1"; usage; exit 2 ;;
    *) FICHIERS+=("$1"); EXPLICITE=1 ;;
  esac
  shift
done

# Sélection automatique : index git, sinon fichiers suivis. Les fichiers pièges de
# verification/ sont volontairement non conformes : ils ne sont audités que si on les
# passe explicitement en argument.
if [ "$EXPLICITE" -eq 0 ]; then
  if git rev-parse --git-dir >/dev/null 2>&1; then
    while IFS= read -r f; do
      case "$f" in verification/exemple-a-corriger.*) continue ;; esac
      [ -n "$f" ] && [ -f "$f" ] && FICHIERS+=("$f")
    done < <(git diff --cached --name-only --diff-filter=ACM)
    if [ ${#FICHIERS[@]} -eq 0 ]; then
      while IFS= read -r f; do
        case "$f" in verification/exemple-a-corriger.*) continue ;; esac
        [ -f "$f" ] && FICHIERS+=("$f")
      done < <(git ls-files)
    fi
  fi
  if [ ${#FICHIERS[@]} -eq 0 ]; then echo "Aucun fichier à auditer."; exit 0; fi
fi

ELEVES=0
MOYENS=0

for fichier in "${FICHIERS[@]}"; do
  ext="${fichier##*.}"
  [ "$ext" = "$fichier" ] && continue
  while IFS='§' read -r exts niveau precision regex exclusion message critere; do
    [ -z "${exts:-}" ] && continue
    [ "$precision" = "basse" ] && [ "$TOUT" -eq 0 ] && continue
    case ",$exts," in *",$ext,"*) ;; *) continue ;; esac
    while IFS= read -r trouve; do
      [ -z "$trouve" ] && continue
      num="${trouve%%:*}"
      contenu="${trouve#*:}"
      if [ -n "${exclusion:-}" ] && printf '%s' "$contenu" | grep -qEi -- "$exclusion"; then
        continue
      fi
      printf '%s:%s [%s] %s\n    → %s\n' "$fichier" "$num" "$niveau" "$message" "$critere"
      if [ "$niveau" = "Élevé" ]; then ELEVES=$((ELEVES + 1)); else MOYENS=$((MOYENS + 1)); fi
    done < <(grep -nEi -- "$regex" "$fichier" 2>/dev/null)
  done < <(lire_motifs)
done

TOTAL=$((ELEVES + MOYENS))
echo
if [ "$TOTAL" -eq 0 ]; then
  echo "Pré-filtre écoconception : aucun motif connu sur ${#FICHIERS[@]} fichier(s)."
  exit 0
fi
echo "Pré-filtre écoconception : $TOTAL constat(s) sur ${#FICHIERS[@]} fichier(s) — $ELEVES élevé(s), $MOYENS moyen(s)."
echo "Motifs déterministes seulement : ni exhaustif, ni preuve de non-conformité. La revue par agent reste utile."

[ "$AVERTIR" -eq 1 ] && exit 0
[ "$ELEVES" -gt 0 ] && exit 1
exit 0
