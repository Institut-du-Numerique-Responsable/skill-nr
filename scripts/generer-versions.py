#!/usr/bin/env python3
"""Génère les versions des règles NR pour Claude Code, Gemini CLI et OpenCode.

Source unique : .continue/rules/*.md (et .continue/agents/*.md pour la revue).
Ne pas éditer les fichiers générés dans versions/ : modifier la source puis relancer :

    python3 scripts/generer-versions.py
"""

import argparse
import json
import re
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
RULES = RACINE / ".continue" / "rules"
AGENTS = RACINE / ".continue" / "agents"
OUT = RACINE / "versions"

# Ordre de concaténation : transverse d'abord, puis principes, puis langages.
ORDRE = [
    "numerique-responsable",
    "usage-sobre-assistant",
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

# Ce commentaire ne doit JAMAIS précéder un frontmatter : les outils n'analysent le bloc
# YAML que s'il ouvre le fichier. Sur un fichier à frontmatter, l'écrire après le `---`.
AVERTISSEMENT = (
    "<!-- Fichier généré par scripts/generer-versions.py, ne pas éditer à la main.\n"
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


def description_regle(slug: str) -> str:
    """Renvoie la description du frontmatter, pour les formats qui l'exigent."""
    texte = (RULES / f"{slug}.md").read_text(encoding="utf-8")
    m = re.search(r"^description:\s*(.+)$", texte, re.M)
    return m.group(1).strip() if m else slug


def globs_separes(globs: str) -> str:
    """Développe `**/*.{js,ts}` en `**/*.js,**/*.ts`.

    Continue accepte l'alternance en accolades ; Cursor et Copilot attendent plutôt
    une liste séparée par des virgules. On développe pour ne dépendre d'aucun des deux
    comportements.
    """
    m = re.match(r"^(.*)\{([^}]+)\}(.*)$", globs)
    if not m:
        return globs
    avant, alternatives, apres = m.groups()
    return ",".join(f"{avant}{a.strip()}{apres}" for a in alternatives.split(","))


def corps_avec_portee(slug: str) -> str:
    """Corps de la règle, avec la mention de portée pour les formats sans globs."""
    globs, corps = lire_regle(slug)
    if globs:
        corps = re.sub(
            r"^(# .+)$",
            rf"\1\n\n> S'applique aux fichiers : `{globs}`",
            corps,
            count=1,
            flags=re.M,
        )
    return corps


def bloc_regles() -> str:
    return "\n\n---\n\n".join(corps_avec_portee(slug) for slug in ORDRE)


PREAMBULE = """# Règles Numérique Responsable : écoconception et accessibilité

Ces règles s'appliquent à tout code que tu écris ou modifies dans ce projet.
Chaque section « S'applique aux fichiers » ne concerne que les fichiers de son
langage : applique-la quand tu travailles sur ce type de fichier, ignore-la sinon.
Cite le critère source (RGESN x.x, GR491_xxx, Opquast n°xxx) quand tu appliques
une règle, pour la montée en compétence de l'équipe.

Référentiels : RGESN v2 (ARCEP/ARCOM/ADEME), GR491 (INR), Opquast (CC BY-SA), RGAA 4.

"""



def contexte_cible(destination: Path) -> str:
    """Socle permanent et références locales, sans import automatique implicite."""
    socle = {"numerique-responsable", "usage-sobre-assistant"}
    references = destination / ".nr" / "regles"
    references.mkdir(parents=True, exist_ok=True)
    index = []
    for slug in ORDRE:
        if slug in socle:
            continue
        (references / f"{slug}.md").write_text(
            AVERTISSEMENT + corps_avec_portee(slug) + "\n", encoding="utf-8")
        globs, _ = lire_regle(slug)
        portee = globs or "architecture et traitements backend"
        index.append(f"- `{portee}` : `.nr/regles/{slug}.md`")
    return (
        AVERTISSEMENT + PREAMBULE
        + "\n\n".join(lire_regle(slug)[1] for slug in ORDRE if slug in socle)
        + "\n\n## Règles spécialisées à lire à la demande\n\n"
        + "Avant de modifier ou relire un fichier, lis les références correspondant "
        "à son langage et à sa couche technique, depuis la racine du projet. "
        "Ne charge pas les autres références. Si un fichier manque, signale "
        "l’installation incomplète. Ces chemins ne sont pas des imports automatiques.\n\n"
        + "\n".join(index) + "\n"
    )

def generer():
    regles = bloc_regles()
    eco = corps_agent("eco-check")
    a11y = corps_agent("accessibilite-check")

    # ---- Claude Code : CLAUDE.md + sous-agents ----
    cc = OUT / "claude-code"
    (cc / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
    (cc / "CLAUDE.md").write_text(contexte_cible(cc), encoding="utf-8")
    (cc / ".claude" / "agents" / "eco-check.md").write_text(
        "---\nname: eco-check\ndescription: Revue écoconception d'un diff selon le RGESN, "
        "le GR491 et Opquast. À utiliser après toute modification de code significative.\n---\n\n"
        + AVERTISSEMENT + eco + "\n",
        encoding="utf-8",
    )
    (cc / ".claude" / "agents" / "accessibilite-check.md").write_text(
        "---\nname: accessibilite-check\ndescription: Revue accessibilité RGAA 4 / WCAG 2.1 AA "
        "d'un diff. À utiliser après toute modification d'interface.\n---\n\n"
        + AVERTISSEMENT + a11y + "\n",
        encoding="utf-8",
    )

    # ---- Gemini CLI : GEMINI.md + commandes ----
    gm = OUT / "gemini-cli"
    (gm / ".gemini" / "commands").mkdir(parents=True, exist_ok=True)
    (gm / "GEMINI.md").write_text(contexte_cible(gm), encoding="utf-8")

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
    (oc / "AGENTS.md").write_text(contexte_cible(oc), encoding="utf-8")
    (oc / ".opencode" / "agent" / "eco-check.md").write_text(
        "---\ndescription: Revue écoconception d'un diff selon le RGESN, le GR491 et Opquast\n"
        "mode: subagent\n---\n\n" + AVERTISSEMENT + eco + "\n",
        encoding="utf-8",
    )
    (oc / ".opencode" / "agent" / "accessibilite-check.md").write_text(
        "---\ndescription: Revue accessibilité RGAA 4 / WCAG 2.1 AA d'un diff\n"
        "mode: subagent\n---\n\n" + AVERTISSEMENT + a11y + "\n",
        encoding="utf-8",
    )

    # ---- Mistral Vibe : AGENTS.md + agents TOML + prompts ----
    mv = OUT / "mistral-vibe"
    (mv / ".vibe" / "agents").mkdir(parents=True, exist_ok=True)
    (mv / ".vibe" / "prompts").mkdir(parents=True, exist_ok=True)
    (mv / "AGENTS.md").write_text(contexte_cible(mv), encoding="utf-8")

    def agent_vibe(nom: str, display: str, description: str) -> str:
        return (
            "# Généré par scripts/generer-versions.py, ne pas éditer à la main.\n"
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

    # ---- Kimi CLI : AGENTS.md + agents YAML + prompts ----
    ki = OUT / "kimi-cli"
    (ki / ".kimi" / "agents").mkdir(parents=True, exist_ok=True)
    (ki / "AGENTS.md").write_text(contexte_cible(ki), encoding="utf-8")

    def agent_kimi_yaml(nom: str) -> str:
        return (
            "# Généré par scripts/generer-versions.py, ne pas éditer à la main.\n"
            "version: 1\n"
            "agent:\n"
            '  extend: "default"\n'
            f"  system_prompt_path: ./{nom}.md\n"
        )

    (ki / ".kimi" / "agents" / "eco-check.yaml").write_text(agent_kimi_yaml("eco-check"), encoding="utf-8")
    (ki / ".kimi" / "agents" / "accessibilite-check.yaml").write_text(
        agent_kimi_yaml("accessibilite-check"), encoding="utf-8"
    )
    (ki / ".kimi" / "agents" / "eco-check.md").write_text(AVERTISSEMENT + eco + "\n", encoding="utf-8")
    (ki / ".kimi" / "agents" / "accessibilite-check.md").write_text(AVERTISSEMENT + a11y + "\n", encoding="utf-8")

    # ---- Kilo Code : skills découverts à la demande + sous-agents ----
    # Format vérifié contre l’archive fournie et la documentation Kilo.
    kl = OUT / "kilo"
    (kl / ".kilo" / "agents").mkdir(parents=True, exist_ok=True)
    for slug in ORDRE:
        destination = kl / ".kilo" / "skills" / slug
        destination.mkdir(parents=True, exist_ok=True)
        description = "À utiliser pour écrire ou relire du code. " + description_regle(slug)
        if slug == "usage-sobre-assistant":
            description = "À utiliser pendant une session de développement : sobriété du contexte, qualité et mesure."
        corps = corps_avec_portee(slug)
        if slug == "usage-sobre-assistant":
            corps = corps.split("## Repères par outil", 1)[0].rstrip() + (
                "\n\n## Repères Kilo Code\n\n"
                "Les skills sont découverts au démarrage, puis lus à la demande selon leur description. "
                "Pour une tâche sans lien, ouvre une nouvelle session. Demande explicitement "
                "l’utilisation du skill utile si nécessaire.\n"
            )
        (destination / "SKILL.md").write_text(
            f"---\nname: {slug}\ndescription: {json.dumps(description, ensure_ascii=False)}\n"
            "license: CC-BY-SA-4.0\n---\n\n" + AVERTISSEMENT + corps + "\n",
            encoding="utf-8",
        )

    def agent_kilo(description: str, corps: str) -> str:
        # Frontmatter en tête de fichier, l'avertissement ensuite : Kilo n'analyse le
        # bloc YAML que s'il ouvre le fichier.
        return (
            f"---\ndescription: {description}\nmode: subagent\n---\n\n"
            + AVERTISSEMENT + corps + "\n"
        )

    (kl / ".kilo" / "agents" / "eco-check.md").write_text(
        agent_kilo("Revue écoconception d'un diff selon le RGESN, le GR491 et Opquast", eco),
        encoding="utf-8",
    )
    (kl / ".kilo" / "agents" / "accessibilite-check.md").write_text(
        agent_kilo("Revue accessibilité RGAA 4 / WCAG 2.1 AA d'un diff", a11y),
        encoding="utf-8",
    )

    # ---- Cursor : une règle .mdc par fichier source, ciblée par globs ----
    # Comme Continue, Cursor charge une règle seulement si un fichier correspondant est
    # dans le contexte : pas de bloc unique de 34 Ko à chaque session.
    cu = OUT / "cursor"
    (cu / ".cursor" / "rules").mkdir(parents=True, exist_ok=True)
    (cu / ".cursor" / "commands").mkdir(parents=True, exist_ok=True)
    for slug in ORDRE:
        globs, corps = lire_regle(slug)
        entete = [
            "---",
            f"description: {description_regle(slug)}",
        ]
        if globs:
            entete.append(f"globs: {globs_separes(globs)}")
            entete.append("alwaysApply: false")
        else:
            entete.append("alwaysApply: true")
        entete.append("---")
        (cu / ".cursor" / "rules" / f"{slug}.mdc").write_text(
            "\n".join(entete) + "\n\n" + AVERTISSEMENT + corps + "\n", encoding="utf-8"
        )
    for nom, corps in (("eco-check", eco), ("accessibilite-check", a11y)):
        (cu / ".cursor" / "commands" / f"{nom}.md").write_text(
            AVERTISSEMENT + corps + "\n\nApplique cette revue aux changements en cours.\n",
            encoding="utf-8",
        )

    # ---- GitHub Copilot : instructions ciblées par applyTo + prompts de revue ----
    co = OUT / "copilot"
    (co / ".github" / "instructions").mkdir(parents=True, exist_ok=True)
    (co / ".github" / "prompts").mkdir(parents=True, exist_ok=True)
    for slug in ORDRE:
        globs, corps = lire_regle(slug)
        cible = globs_separes(globs) if globs else "**"
        (co / ".github" / "instructions" / f"{slug}.instructions.md").write_text(
            "---\n"
            f'applyTo: "{cible}"\n'
            f"description: {description_regle(slug)}\n"
            "---\n\n" + AVERTISSEMENT + corps + "\n",
            encoding="utf-8",
        )
    for nom, corps, desc in (
        ("eco-check", eco, "Revue écoconception du diff courant (RGESN, GR491, Opquast)"),
        ("accessibilite-check", a11y, "Revue accessibilité RGAA 4 du diff courant"),
    ):
        (co / ".github" / "prompts" / f"{nom}.prompt.md").write_text(
            "---\n"
            "mode: agent\n"
            f"description: {desc}\n"
            "---\n\n" + AVERTISSEMENT + corps
            + "\n\nApplique cette revue aux changements en cours dans l'espace de travail.\n",
            encoding="utf-8",
        )

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




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="vérifier sans modifier les sorties")
    args = parser.parse_args()
    if args.check:
        original = OUT
        with tempfile.TemporaryDirectory(prefix="nr-generation-") as dossier:
            OUT = Path(dossier)
            generer()
            attendus = {p.relative_to(OUT): p.read_bytes() for p in OUT.rglob("*") if p.is_file()}
            actuels = {p.relative_to(original): p.read_bytes() for p in original.rglob("*")
                       if p.is_file() and p.relative_to(original) != Path("README.md")}
            ecarts = sorted(str(p) for p in attendus.keys() | actuels.keys()
                            if attendus.get(p) != actuels.get(p))
            if ecarts:
                print("Sorties divergentes :\n" + "\n".join(ecarts))
                raise SystemExit(1)
            print("Versions générées à jour.")
    else:
        generer()
        print("Versions générées.")
