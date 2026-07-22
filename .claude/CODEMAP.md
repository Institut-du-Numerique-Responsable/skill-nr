# CODEMAP : regles-ecoconception-ia

Skills Continue (continue.dev) pour l'écoconception / numérique responsable. Tout est en français.

## Fichiers actifs (chargés par Continue)

- `.continue/rules/numerique-responsable.md` : transverse (alwaysApply) : RGAA, RGPD, durabilité
- `.continue/rules/usage-sobre-assistant.md` : transverse (alwaysApply) : sobriété de la session IA elle-même (contexte, rewind/compact, proportionner la puissance), inspiré de green-claude/boris.json
- `.continue/rules/ecoconception-frontend.md` : HTML/CSS/JS navigateur (globs web)
- `.continue/rules/ecoconception-backend.md` : principes API/données tous langages + section Node.js
- `.continue/rules/ecoconception-{sql,java,csharp,python,php,ruby,rust,c,cpp,javascript}.md` : anti-patterns par langage (globs) ; sql couvre aussi PL/SQL ; javascript couvre JS+TS navigateur et Node (la section Node a été retirée de backend)
- `LICENSE.md` (CC BY-SA 4.0, attributions Opquast/GR491) + `CONTRIBUTING.md` : préparation publication GitHub
- `.continue/rules/qualite-web-opquast.md` : 35 règles Opquast écoconception (globs web)
- `.continue/agents/eco-check.md` : agent revue écoconception (cn review) ; frontmatter name obligatoire
- `.continue/agents/accessibilite-check.md` : agent revue RGAA

## Référence et doc

- `referentiels/gr491.md` : 61 recommandations GR491 extraites avec IDs (cités par les règles)
- `referentiels/opquast-ecoconception.md` : 35 règles Opquast (CC BY-SA), filtre écoconception × conception/développement/éditorial
- `docs/guide-developpeur.md`, `docs/guide-deploiement.md`, `docs/developper-un-skill.md`
- `continue/` : clone amont (gitignoré), utile pour la doc : `continue/docs/`

- `versions/{claude-code,gemini-cli,opencode,mistral-vibe,kimi-cli,chatgpt}/` : GÉNÉRÉS par `scripts/generer-versions.py` depuis .continue/ (ne jamais éditer à la main). Codex et ZCode (GLM) réutilisent tels quels le AGENTS.md d'opencode/kimi-cli (standard partagé), pas de dossier dédié. DeepSeek non retenu (pas de harnais/format stabilisé, cf. versions/README.md).
- `docs/index.html` (+ robots.txt, sitemap.xml) : page vitrine GitHub Pages, thème repris de green-claude (bleu #0a7190/#5ecbe0), déployée sur docs/ de main

## Points durs (ne pas redécouvrir)

- CLI `cn` v1.5.47 : pas de `cn login`/Hub ; la commande de revue est `cn review --review-agents <fichier>` ; applique les fixes au working tree ; rapport visible seulement en TTY
- Modèle : Ollama local `qwen3-coder` via `~/.continue/config.yaml` (usage local, sans API payante)
- Branche `test-eco` : fichiers pièges `exemples/` (HTML, SQL, Java, C#) pour tester les agents
