# CODEMAP : skill-nr

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

- `referentiels/rgesn.md` : 78 critères RGESN 2024, 9 thématiques, extraits du PDF Arcep (URL dans l'en-tête du fichier ; le site officiel sert du HTML anti-bot, il faut un user-agent pour récupérer le PDF). Niveaux de priorité VOLONTAIREMENT absents : tableaux sur deux colonnes, extraction non fiable (4.3 fantôme en Prioritaire, 4.13 dans aucun tableau). Vérifié en CI.
- `referentiels/gr491.md` : extraction PARTIELLE et assumée, 47 recommandations sur 61, 6 familles sur 8 (Stratégie et Spécifications hors périmètre code). L'en-tête le dit explicitement depuis le 2026-08-03.
- `referentiels/opquast-ecoconception.md` : 35 règles Opquast (CC BY-SA), filtre écoconception × conception/développement/éditorial
- `docs/guide-developpeur.md`, `docs/guide-deploiement.md`, `docs/developper-un-skill.md`
- `continue/` : clone amont (gitignoré), utile pour la doc : `continue/docs/`

- `versions/{claude-code,cursor,copilot,gemini-cli,opencode,mistral-vibe,kimi-cli,kilo,chatgpt}/` : GÉNÉRÉS par `scripts/generer-versions.py` depuis .continue/ (ne jamais éditer à la main). Cursor (.mdc avec globs) et Copilot (.instructions.md avec applyTo) sont les DEUX SEULES déclinaisons, avec Continue, à cibler par type de fichier : pas de bloc de 34 Ko par session. `globs_separes()` développe `**/*.{a,b}` en liste à virgules, ces deux formats ne garantissant pas les accolades. Kilo Code (kilo.ai, ex-Kilo Code VS Code) est un cas intermédiaire : règles découpées en fichiers `.kilo/rules/*.md` MAIS aucun ciblage par type de fichier, il faut les lister une par une dans `instructions` de `kilo.jsonc` (non listée = jamais chargée) ; sous-agents `.kilo/agents/*.md`, frontmatter `description` + `mode: subagent` EN TÊTE de fichier (l'avertissement généré vient après, sinon le YAML n'est pas lu) ; `.kilocode/rules/` legacy encore accepté ; AGENTS.md lu nativement aussi. Codex et ZCode (GLM) réutilisent tels quels le AGENTS.md d'opencode/kimi-cli (standard partagé), pas de dossier dédié. DeepSeek non retenu (pas de harnais/format stabilisé, cf. versions/README.md).
- `verification/` : kit de validation d'installation. `exemple-a-corriger.{html,sql}` = 18 écarts volontaires (13 HTML + 5 SQL), `resultats-attendus.md` = grille avec critères et barème (12/18, calé sur mesure), `README.md` = protocole en 3 étapes. Ne jamais corriger ces fichiers.
- `.github/workflows/verification.yml` : CI sur PR et push main. Job `integrite` = `scripts/verifier-depot.sh` ; job `ecoconception` (PR seulement) = eco-audit sur le diff de la PR, en `--avertir` (informatif), commente la PR via github-script avec un marqueur HTML pour mettre à jour le commentaire au lieu d'en empiler. JAMAIS EXÉCUTÉ EN CONDITIONS RÉELLES sur une PR à ce jour (livré directement sur main).
- `scripts/verifier-depot.sh` : 10 contrôles (dont RGESN). Le contrôle de dérive EXCLUT `versions/README.md`, rédigé à la main bien que situé dans versions/ : sans l'exclusion il échoue à chaque modification de cette doc. Le tester en modifiant une RÈGLE sans régénérer, pas en éditant un fichier généré (le contrôle régénère avant de comparer, donc il écrase l'édition). d'intégrité (dérive versions/, ORDRE, frontmatter, identifiants existants, liens, syntaxe, corpus 12/18 mini, pré-filtre sur le dépôt). Testé par injection de fautes. Exit 1 si un contrôle échoue.
- `scripts/installer-hooks.sh` : pose pre-commit (eco-audit) et pre-push (refus de main + verifier-depot) dans .git/hooks. Corps des hooks en heredocs quotés, PAS en chaînes simples (les apostrophes françaises cassent le quoting).
- Dépôt public avec branche `main` protégée : pull request, approbation et contrôle d'intégrité obligatoires. Les hooks locaux donnent un retour plus rapide avant la CI.
- `scripts/eco-audit.sh` : pré-filtre déterministe grep, zéro appel modèle. Table de motifs embarquée, champs séparés par « § » (PAS « | » : les regex en contiennent). Contraintes : ERE POSIX, pas de lookahead, pas de `\b` (colonne EXCLUSION à la place des assertions négatives). Calibré sur 600 fichiers du clone Continue : 3 constats Élevé. Motifs bruyants (`import * as`, `.ToList()`, `.clone()`, `fs.*Sync` en Moyen) derrière `--tout`. Ignore `verification/exemple-a-corriger.*` en sélection auto, sinon le hook bloque tout commit ici. Trouve 12 des 18 écarts du corpus.
- MESURE DU 2026-08-03 (qwen3-coder local, règles Continue chargées, dossier isolé) : modèle 16/18 détectés mais 1/18 tracé au bon critère et `RGESN 6.8` inventé (thématique 6 = 7 critères) ; pré-filtre 12/18 et 12/18 tracés. Barème passé de « 10/18 + 3 critères cités » à « 12/18 », la citation seule ne prouvant rien.
- PIÈGE : `git checkout -- versions/` (réflexe pendant les tests du contrôle de dérive) ANNULE AUSSI `versions/README.md`, qui est écrit à la main. Édition perdue une fois le 2026-08-03.
- PIÈGE DE MESURE : lancer la revue DEPUIS le dépôt donne au modèle `verification/resultats-attendus.md`, donc les réponses (premier essai : 18/18 avec formulations recopiées mot pour mot). Toujours mesurer dans un dossier isolé = `.continue/` + les deux fichiers pièges, rien d'autre.
- `scripts/scorer-detection.py` : score un rapport (fichier ou stdin) contre `verification/attendus.json`. Rapprochement textuel par motifs, donc généreux : sert à comparer deux états des règles, pas à noter dans l'absolu. `--seuil N` pour la CI. Un critère ne compte que si l'écart est aussi détecté.
- `verification/attendus.json` : source machine des 18 écarts (motifs de rapprochement + critères). `resultats-attendus.md` reste la version lisible ; le scorer avertit si les comptes divergent.
- `scripts/verifier-installation.sh` : contrôle présence + contenu des fichiers de règles dans un projet cible (`bash scripts/verifier-installation.sh [outil] [chemin]`, `auto` par défaut). Détecte le cas fréquent d'un `AGENTS.md`/`CLAUDE.md` du projet ayant écrasé la copie. Codes : 0 ok, 1 fichier manquant, 2 outil inconnu.
- `README.md` (français, canonique) : porte la procédure d'installation complète par outil (section `## Installation`) ; `versions/README.md` n'en garde que le résumé et les spécificités de format. `README.en.md` = traduction anglaise à maintenir en parallèle (ancres anglaises propres, switcher 🇬🇧/🇫🇷 dans les deux). Les règles elles-mêmes restent en français, c'est assumé et expliqué dans README.en.md.
- `docs/index.html` (+ robots.txt, sitemap.xml) : page vitrine GitHub Pages, thème repris de green-claude (bleu #0a7190/#5ecbe0), déployée sur docs/ de main

## Points durs (ne pas redécouvrir)

- CLI `cn` v1.5.47 : pas de `cn login`/Hub ; la commande de revue est `cn review --review-agents <fichier>` ; applique les fixes au working tree ; rapport visible seulement en TTY
- Modèle : Ollama local `qwen3-coder` via `~/.continue/config.yaml` (usage local, sans API payante)
- Branche `test-eco` : fichiers pièges `exemples/` (HTML, SQL, Java, C#) pour tester les agents
