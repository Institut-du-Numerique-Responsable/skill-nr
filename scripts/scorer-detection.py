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
    r"GR491_[A-Za-z]+_\d+|Opquast\s*n°\s*\d+|RGESN\s*\d+(?:\.\d+)?|RGAA\s*\d+(?:\.\d+)?|RGPD",
    re.IGNORECASE,
)


def charger_referentiels():
    """Identifiants réellement existants, lus dans referentiels/.

    Un modèle qui a les règles en contexte cite des critères ; un modèle qui ne les a
    pas en invente de plausibles, souvent en séquence (RGESN 6.1, 6.2, 6.3…). La
    présence d'une citation ne prouve donc rien : sa vérifiabilité, si.
    """
    reels = set()
    rgesn = RACINE / "referentiels" / "rgesn.md"
    if rgesn.exists():
        reels |= {f"RGESN {m}" for m in re.findall(r"^- \*\*RGESN (\d+\.\d+)", rgesn.read_text(encoding="utf-8"), re.M)}
    gr491 = RACINE / "referentiels" / "gr491.md"
    if gr491.exists():
        reels |= set(re.findall(r"GR491_[A-Za-z]+_\d+", gr491.read_text(encoding="utf-8")))
    opquast = RACINE / "referentiels" / "opquast-ecoconception.md"
    if opquast.exists():
        reels |= {f"Opquast n°{m}" for m in re.findall(r"^- (\d+) :", opquast.read_text(encoding="utf-8"), re.M)}
    return reels


def normaliser(citation: str) -> str:
    c = " ".join(citation.split())
    c = re.sub(r"Opquast\s*n°\s*", "Opquast n°", c, flags=re.IGNORECASE)
    return c


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
    criteres = sorted(set(normaliser(m.group(0)) for m in MOTIF_CRITERE.finditer(rapport)))
    reels = charger_referentiels()
    # RGAA et RGPD ne sont pas extraits dans referentiels/ : non vérifiables ici.
    verifiables = [c for c in criteres if c.startswith(("RGESN", "GR491", "Opquast"))]
    inexistants = sorted(c for c in verifiables if c not in reels)
    detectes = [r for r in resultats if r["detecte"]]
    return {
        "total": len(ecarts),
        "detectes": len(detectes),
        "criteres_cites": len(criteres),
        "liste_criteres": criteres,
        "exacts": sum(1 for r in resultats if r["critere_cite"]),
        "citations_inexistantes": inexistants,
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
        if score["citations_inexistantes"]:
            print()
            print(f"  ⚠ {len(score['citations_inexistantes'])} identifiant(s) cité(s) qui n'existent pas :")
            print(f"      {', '.join(score['citations_inexistantes'])}")
            print("      Le modèle invente des références. Citer n'est pas tracer :")
            print("      c'est la vérifiabilité de la citation qui compte, pas sa présence.")
        print()
        # Repères calés sur une mesure réelle (qwen3-coder local, règles Continue
        # chargées) : 16/18 détectés, mais 1 seul écart tracé au bon critère et des
        # identifiants inventés. La détection est donc le signal solide ; la citation
        # ne vaut que si elle est vérifiable.
        if score["detectes"] >= 12 and not score["citations_inexistantes"]:
            print("  Lecture : installation fonctionnelle, citations vérifiables.")
        elif score["detectes"] >= 12:
            print("  Lecture : les règles sont chargées (détection élevée), mais certaines")
            print("  références sont inventées : relire les critères cités avant de s'y fier.")
        elif score["detectes"] < 5:
            print("  Lecture : sous le repère. Les règles ne semblent pas chargées.")
        else:
            print("  Lecture : détection partielle, entre les deux repères.")

    if args.seuil is not None and score["detectes"] < args.seuil:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(principal())
