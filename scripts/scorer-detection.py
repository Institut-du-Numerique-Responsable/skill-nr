#!/usr/bin/env python3
"""Score un rapport de revue contre les écarts attendus de verification/.

    python3 scripts/scorer-detection.py rapport.txt
    cn review --review-agents .continue/agents/eco-check.md | python3 scripts/scorer-detection.py
    bash scripts/eco-audit.sh verification/exemple-a-corriger.* | python3 scripts/scorer-detection.py

Le rapport peut venir de n'importe quel assistant : le script cherche, pour chaque
écart de verification/attendus.json, si le texte contient l'un de ses motifs.

À quoi ça sert : comparer deux états des règles. « Cette reformulation fait passer
la détection de 11/18 à 15/18 » est une phrase qu'on ne peut pas prononcer sans
mesure. Le chiffre absolu vaut moins que son évolution.

Ce que ça ne mesure pas : la justesse des correctifs proposés, et le fait qu'un
motif trouvé le soit pour la bonne raison. Le rapprochement est textuel, donc
généreux. À nombre de constats égal, un score qui monte reste un bon signal.

Options :
    --json          sortie machine, pour la CI
    --seuil N       code de sortie 1 si moins de N écarts détectés (défaut : aucun seuil)
    --détail        liste aussi les motifs qui ont déclenché chaque détection
"""

import argparse
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
ATTENDUS = RACINE / "verification" / "attendus.json"
TABLE_LISIBLE = RACINE / "verification" / "resultats-attendus.md"

# Un critère cité est le signal le plus fiable qu'un modèle a bien les règles en
# contexte : n'importe quel modèle voit un alt manquant, seul un modèle équipé
# écrit « Opquast n°124 ».
MOTIF_CRITERE = re.compile(
    r"GR491_[A-Za-z]+_\d+|Opquast\s*n°\s*\d+|RGESN\s*\d|RGAA\s*\d|RGPD",
    re.IGNORECASE,
)


def charger_attendus():
    donnees = json.loads(ATTENDUS.read_text(encoding="utf-8"))
    ecarts = donnees["ecarts"]
    # Garde-fou : la table lisible et la source machine doivent rester alignées.
    if TABLE_LISIBLE.exists():
        annonces = re.search(r"totalisent \*\*(\d+) écarts\*\*", TABLE_LISIBLE.read_text(encoding="utf-8"))
        if annonces and int(annonces.group(1)) != len(ecarts):
            print(
                f"Avertissement : resultats-attendus.md annonce {annonces.group(1)} écarts, "
                f"attendus.json en contient {len(ecarts)}.",
                file=sys.stderr,
            )
    return ecarts


def scorer(rapport: str, ecarts: list) -> dict:
    resultats = []
    for ecart in ecarts:
        touches = [m for m in ecart["motifs"] if re.search(m, rapport, re.IGNORECASE)]
        resultats.append({
            "id": ecart["id"],
            "fichier": ecart["fichier"],
            "libelle": ecart["libelle"],
            "detecte": bool(touches),
            "motifs_touches": touches,
            "criteres_attendus": ecart["criteres"],
            # Un critère ne compte que si l'écart correspondant a été détecté : sinon
            # un identifiant cité pour un autre constat gonflerait le score.
            "critere_cite": bool(touches) and any(
                re.search(re.escape(c), rapport, re.IGNORECASE) for c in ecart["criteres"]
            ),
        })
    criteres = sorted(set(m.group(0) for m in MOTIF_CRITERE.finditer(rapport)))
    detectes = [r for r in resultats if r["detecte"]]
    return {
        "total": len(ecarts),
        "detectes": len(detectes),
        "criteres_cites": len(criteres),
        "liste_criteres": criteres,
        "exacts": sum(1 for r in resultats if r["critere_cite"]),
        "resultats": resultats,
    }


def principal():
    parseur = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parseur.add_argument("rapport", nargs="?", help="fichier du rapport ; à défaut, entrée standard")
    parseur.add_argument("--json", action="store_true", help="sortie machine")
    parseur.add_argument("--seuil", type=int, default=None, help="échoue sous ce nombre d'écarts détectés")
    parseur.add_argument("--détail", "--detail", dest="detail", action="store_true")
    args = parseur.parse_args()

    texte = Path(args.rapport).read_text(encoding="utf-8") if args.rapport else sys.stdin.read()
    if not texte.strip():
        print("Rapport vide : rien à scorer.", file=sys.stderr)
        return 2

    score = scorer(texte, charger_attendus())

    if args.json:
        print(json.dumps(score, ensure_ascii=False, indent=2))
    else:
        for r in score["resultats"]:
            marque = "✓" if r["detecte"] else "·"
            exact = " [critère cité]" if r["critere_cite"] else ""
            print(f"  {marque} {r['id']:>2}. {r['libelle']}{exact}")
            if args.detail and r["motifs_touches"]:
                print(f"        motifs : {', '.join(r['motifs_touches'])}")
        print()
        print(f"  Écarts détectés   : {score['detectes']}/{score['total']}")
        print(f"  Critères cités    : {score['criteres_cites']} distincts"
              + (f" ({', '.join(score['liste_criteres'][:6])}…)" if score["criteres_cites"] else ""))
        print(f"  Écarts tracés au bon critère : {score['exacts']}/{score['total']}")
        print()
        if score["detectes"] >= 10 and score["criteres_cites"] >= 3:
            print("  Lecture : au-dessus du repère d'installation fonctionnelle (10/18, 3 critères).")
        elif score["detectes"] < 5 or score["criteres_cites"] == 0:
            print("  Lecture : sous le repère. Les règles ne semblent pas chargées.")
        else:
            print("  Lecture : entre les deux repères. Détection partielle.")

    if args.seuil is not None and score["detectes"] < args.seuil:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(principal())
