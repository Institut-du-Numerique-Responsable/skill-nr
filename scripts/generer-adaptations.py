#!/usr/bin/env python3
"""Génère les adaptations des règles NR pour Claude Code, Gemini CLI et OpenCode.

Source unique : .continue/rules/*.md (et .continue/agents/*.md pour la revue).
Ne pas éditer les fichiers générés dans adaptations/ — modifier la source puis relancer :

    python3 scripts/generer-adaptations.py
"""

import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
RULES = RACINE / ".continue" / "rules"
AGENTS = RACINE / ".continue" / "agents"
OUT = RACINE / "adaptations"

# Ordre de concaténation : transverse d'abord, puis principes, puis langages.
ORDRE = [
    "numerique-responsable",
    "ecoconception-backend",
    "ecoconception-frontend",
    "qualite-web-opquast",
    "ecoconception-sql",
    "ecoconception-javascript",
    "ecoconception-java",
    "ecoconception-csharp",
    "ecoconception-python",
    "ecoconception-php",
    "ecoconception-ruby",
    "ecoconception-rust",
    "ecoconception-c",
    "ecoconception-cpp",
]

AVERTISSEMENT = (
    "<!-- Fichier généré par scripts/generer-adaptations.py — ne pas éditer à la main.\n"
    "     Source : .continue/rules/ -->\n\n"
)


def lire_regle(slug: str) -> tuple[str, str]:
    """Renvoie (globs, corps sans frontmatter) d'une règle."""
    texte = (RULES / f"{slug}.md").read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", texte, re.S)
    frontmatter = m.group(1) if m else ""
    corps = texte[m.end():].strip() if m else texte.strip()
    g = re.search(r'globs:\s*"?([^"\n]+)"?', frontmatter)
    return (g.group(1).strip() if g else "", corps)


def corps_agent(nom: str) -> str:
    texte = (AGENTS / f"{nom}.md").read_text(encoding="utf-8")
    m = re.match(r"---\n.*?\n---\n", texte, re.S)
    return texte[m.end():].strip() if m else texte.strip()


def bloc_regles() -> str:
    parties = []
    for slug in ORDRE:
        globs, corps = lire_regle(slug)
        if globs:
            corps = re.sub(
                r"^(# .+)$",
                rf"\1\n\n> S'applique aux fichiers : `{globs}`",
                corps,
                count=1,
                flags=re.M,
            )
        parties.append(corps)
    return "\n\n---\n\n".join(parties)


PREAMBULE = """# Règles Numérique Responsable — écoconception et accessibilité

Ces règles s'appliquent à tout code que tu écris ou modifies dans ce projet.
Chaque section « S'applique aux fichiers » ne concerne que les fichiers de son
langage : applique-la quand tu travailles sur ce type de fichier, ignore-la sinon.
Cite le critère source (RGESN x.x, GR491_xxx, Opquast n°xxx) quand tu appliques
une règle, pour la montée en compétence de l'équipe.

Référentiels : RGESN v2 (ARCEP/ARCOM/ADEME), GR491 (INR), Opquast (CC BY-SA), RGAA 4.

"""


def generer():
    regles = bloc_regles()
    eco = corps_agent("eco-check")
    a11y = corps_agent("accessibilite-check")

    # ---- Claude Code : CLAUDE.md + sous-agents ----
    cc = OUT / "claude-code"
    (cc / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
    (cc / "CLAUDE.md").write_text(AVERTISSEMENT + PREAMBULE + regles + "\n", encoding="utf-8")
    (cc / ".claude" / "agents" / "eco-check.md").write_text(
        AVERTISSEMENT
        + "---\nname: eco-check\ndescription: Revue écoconception d'un diff selon le RGESN, "
        "le GR491 et Opquast. À utiliser après toute modification de code significative.\n---\n\n"
        + eco + "\n",
        encoding="utf-8",
    )
    (cc / ".claude" / "agents" / "accessibilite-check.md").write_text(
        AVERTISSEMENT
        + "---\nname: accessibilite-check\ndescription: Revue accessibilité RGAA 4 / WCAG 2.1 AA "
        "d'un diff. À utiliser après toute modification d'interface.\n---\n\n"
        + a11y + "\n",
        encoding="utf-8",
    )

    # ---- Gemini CLI : GEMINI.md + commandes ----
    gm = OUT / "gemini-cli"
    (gm / ".gemini" / "commands").mkdir(parents=True, exist_ok=True)
    (gm / "GEMINI.md").write_text(AVERTISSEMENT + PREAMBULE + regles + "\n", encoding="utf-8")

    def commande_toml(nom: str, description: str, corps: str) -> str:
        corps_toml = corps.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        return (
            f'description = "{description}"\n\n'
            'prompt = """\n'
            f"{corps_toml}\n\n"
            "Changements à examiner :\n\n"
            "```diff\n!{git diff HEAD}\n```\n"
            '"""\n'
        )

    (gm / ".gemini" / "commands" / "eco-check.toml").write_text(
        commande_toml("eco-check", "Revue écoconception du diff courant (RGESN, GR491, Opquast)", eco),
        encoding="utf-8",
    )
    (gm / ".gemini" / "commands" / "accessibilite-check.toml").write_text(
        commande_toml("accessibilite-check", "Revue accessibilité RGAA 4 du diff courant", a11y),
        encoding="utf-8",
    )

    # ---- OpenCode : AGENTS.md + agents ----
    oc = OUT / "opencode"
    (oc / ".opencode" / "agent").mkdir(parents=True, exist_ok=True)
    (oc / "AGENTS.md").write_text(AVERTISSEMENT + PREAMBULE + regles + "\n", encoding="utf-8")
    (oc / ".opencode" / "agent" / "eco-check.md").write_text(
        AVERTISSEMENT
        + "---\ndescription: Revue écoconception d'un diff selon le RGESN, le GR491 et Opquast\n"
        "mode: subagent\n---\n\n" + eco + "\n",
        encoding="utf-8",
    )
    (oc / ".opencode" / "agent" / "accessibilite-check.md").write_text(
        AVERTISSEMENT
        + "---\ndescription: Revue accessibilité RGAA 4 / WCAG 2.1 AA d'un diff\n"
        "mode: subagent\n---\n\n" + a11y + "\n",
        encoding="utf-8",
    )

    # ---- Mistral Vibe : AGENTS.md + agents TOML + prompts ----
    mv = OUT / "mistral-vibe"
    (mv / ".vibe" / "agents").mkdir(parents=True, exist_ok=True)
    (mv / ".vibe" / "prompts").mkdir(parents=True, exist_ok=True)
    (mv / "AGENTS.md").write_text(AVERTISSEMENT + PREAMBULE + regles + "\n", encoding="utf-8")

    def agent_vibe(nom: str, display: str, description: str) -> str:
        return (
            "# Généré par scripts/generer-adaptations.py — ne pas éditer à la main.\n"
            "# Adapter active_model au modèle disponible dans votre organisation.\n"
            'agent_type = "agent"\n'
            f'display_name = "{display}"\n'
            f'description = "{description}"\n'
            'safety = "safe"\n'
            'active_model = "mistral-medium-latest"\n'
            f'system_prompt_id = "{nom}"\n'
        )

    (mv / ".vibe" / "agents" / "eco-check.toml").write_text(
        agent_vibe("eco-check", "Revue écoconception",
                   "Revue écoconception d'un diff selon le RGESN, le GR491 et Opquast"),
        encoding="utf-8",
    )
    (mv / ".vibe" / "agents" / "accessibilite-check.toml").write_text(
        agent_vibe("accessibilite-check", "Revue accessibilité",
                   "Revue accessibilité RGAA 4 / WCAG 2.1 AA d'un diff"),
        encoding="utf-8",
    )
    (mv / ".vibe" / "prompts" / "eco-check.md").write_text(AVERTISSEMENT + eco + "\n", encoding="utf-8")
    (mv / ".vibe" / "prompts" / "accessibilite-check.md").write_text(AVERTISSEMENT + a11y + "\n", encoding="utf-8")

    # ---- ChatGPT : GPT personnalisé (instructions condensées + connaissances) ----
    cg = OUT / "chatgpt"
    (cg / "connaissances").mkdir(parents=True, exist_ok=True)

    index_langages = "\n".join(
        f"- `{lire_regle(slug)[0] or 'tous les fichiers'}` → section « {slug} »"
        for slug in ORDRE
    )
    instructions = f"""Tu es un assistant de développement spécialisé en écoconception et
numérique responsable (référentiels français : RGESN v2, GR491/INR, Opquast, RGAA 4, RGPD).

Pour TOUT code que tu écris, modifies ou relis, applique les règles du fichier de
connaissances `regles-nr-completes.md` : repère le langage du fichier concerné et
applique la section correspondante. Cite le critère source (RGESN x.x, GR491_xxx,
Opquast n°xxx) quand tu appliques une règle.

Index des sections par type de fichier :
{index_langages}

Principes toujours actifs, quel que soit le langage :
- Sobriété des dépendances : API natives d'abord ; toute librairie ajoutée se justifie.
- Données : ne renvoyer/collecter/stocker que le nécessaire ; pagination systématique
  des collections ; politique de rétention pour tout nouveau stockage ; jamais de secret
  en dur.
- Requêtes : pas de N+1, pas de SELECT *, projections ciblées, index vérifiés.
- Flux : streaming pour les gros volumes, jamais de chargement entier en mémoire.
- Exécution : pas de polling ni d'attente active ; caches bornés et expirants ;
  pas de traitement quadratique sur des collections non bornées.
- Web : HTML sémantique et accessible (RGAA), images lazy + formats modernes, médias
  déclenchés par l'utilisateur, compression et cache HTTP.
- Logs sobres en production ; pas de log en boucle serrée.
- Sobriété fonctionnelle : signale toute fonctionnalité ou complexité superflue et
  propose une alternative plus simple.

Pour une revue de diff : applique la méthode du fichier de connaissances
`revue-ecoconception.md` (et `revue-accessibilite.md` pour l'interface) au diff fourni,
et rends un verdict par point de contrôle avec le critère cité.
"""
    (cg / "instructions-gpt.md").write_text(instructions, encoding="utf-8")
    assert len(instructions) < 8000, "Instructions GPT > 8000 caractères"

    (cg / "connaissances" / "regles-nr-completes.md").write_text(
        AVERTISSEMENT + PREAMBULE + regles + "\n", encoding="utf-8"
    )
    (cg / "connaissances" / "revue-ecoconception.md").write_text(AVERTISSEMENT + eco + "\n", encoding="utf-8")
    (cg / "connaissances" / "revue-accessibilite.md").write_text(AVERTISSEMENT + a11y + "\n", encoding="utf-8")
    for ref in ("gr491.md", "opquast-ecoconception.md"):
        (cg / "connaissances" / ref).write_text(
            (RACINE / "referentiels" / ref).read_text(encoding="utf-8"), encoding="utf-8"
        )

    for f in sorted(OUT.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(RACINE)}  ({f.stat().st_size} o)")


if __name__ == "__main__":
    generer()
