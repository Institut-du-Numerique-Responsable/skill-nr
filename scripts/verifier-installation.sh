#!/usr/bin/env bash
# Vérifie que les fichiers de règles NR sont bien en place dans un projet.
#
#   bash scripts/verifier-installation.sh [outil] [chemin-du-projet]
#
# Sans argument : détecte les outils présents dans le répertoire courant.
# Outils : continue, claude-code, cursor, copilot, gemini-cli, opencode,
#          mistral-vibe, kimi-cli, kilo, codex, chatgpt.
#
# Ce script contrôle la présence et le contenu des fichiers, pas le comportement
# du modèle : pour ça, voir verification/README.md (étape 2).

set -u

OUTIL="${1:-auto}"
PROJET="${2:-$PWD}"
MARQUEUR="Règles Numérique Responsable"
OK=0
KO=0

vert()  { printf '  \033[32m✓\033[0m %s\n' "$1"; OK=$((OK + 1)); }
rouge() { printf '  \033[31m✗\033[0m %s\n' "$1"; KO=$((KO + 1)); }
info()  { printf '\n\033[1m%s\033[0m\n' "$1"; }

# Vérifie qu'un fichier existe, et qu'il contient le marqueur si demandé.
fichier() {
  local chemin="$PROJET/$1" attendu="${2:-}"
  if [ ! -f "$chemin" ]; then
    rouge "$1 absent"
  elif [ -n "$attendu" ] && ! grep -q "$attendu" "$chemin"; then
    rouge "$1 présent mais ne contient pas « $attendu » (mauvais fichier copié ?)"
  else
    vert "$1"
  fi
}

dossier() {
  if [ -d "$PROJET/$1" ]; then vert "$1/"; else rouge "$1/ absent"; fi
}

verifier_continue() {
  info "Continue"
  dossier ".continue/rules"
  fichier ".continue/rules/numerique-responsable.md" "alwaysApply"
  fichier ".continue/agents/eco-check.md" "name: eco-check"
  fichier ".continue/agents/accessibilite-check.md" "name: accessibilite-check"
  if command -v cn >/dev/null 2>&1; then
    vert "CLI cn installée"
  else
    rouge "CLI cn absente (npm i -g @continuedev/cli)"
  fi
}

verifier_claude_code() {
  info "Claude Code"
  fichier "CLAUDE.md" "$MARQUEUR"
  fichier ".claude/agents/eco-check.md" "name: eco-check"
  fichier ".claude/agents/accessibilite-check.md" "name: accessibilite-check"
}

verifier_gemini() {
  info "Gemini CLI"
  fichier "GEMINI.md" "$MARQUEUR"
  fichier ".gemini/commands/eco-check.toml" "prompt"
  fichier ".gemini/commands/accessibilite-check.toml" "prompt"
}

verifier_opencode() {
  info "OpenCode"
  fichier "AGENTS.md" "$MARQUEUR"
  fichier ".opencode/agent/eco-check.md" "mode: subagent"
  fichier ".opencode/agent/accessibilite-check.md" "mode: subagent"
}

verifier_vibe() {
  info "Mistral Vibe"
  fichier "AGENTS.md" "$MARQUEUR"
  fichier ".vibe/agents/eco-check.toml" "system_prompt_id"
  fichier ".vibe/prompts/eco-check.md" "écoconception"
}

verifier_kimi() {
  info "Kimi CLI"
  fichier "AGENTS.md" "$MARQUEUR"
  fichier ".kimi/agents/eco-check.yaml" "system_prompt_path"
  fichier ".kimi/agents/eco-check.md" "écoconception"
}

verifier_kilo() {
  info "Kilo Code"
  dossier ".kilo/rules"
  fichier ".kilo/rules/numerique-responsable.md" "numérique responsable"
  fichier ".kilo/rules/ecoconception-sql.md" "S'applique aux fichiers"
  # Une règle non listée dans instructions n'est jamais chargée par Kilo.
  fichier "kilo.jsonc" "ecoconception-sql.md"
  fichier ".kilo/agents/eco-check.md" "mode: subagent"
}

verifier_cursor() {
  info "Cursor"
  dossier ".cursor/rules"
  fichier ".cursor/rules/numerique-responsable.mdc" "alwaysApply: true"
  fichier ".cursor/rules/ecoconception-sql.mdc" "globs:"
  fichier ".cursor/commands/eco-check.md" "écoconception"
}

verifier_copilot() {
  info "GitHub Copilot"
  dossier ".github/instructions"
  fichier ".github/instructions/numerique-responsable.instructions.md" "applyTo:"
  fichier ".github/instructions/ecoconception-sql.instructions.md" "applyTo:"
  fichier ".github/prompts/eco-check.prompt.md" "mode: agent"
}

verifier_codex() {
  info "OpenAI Codex / ZCode (AGENTS.md seul)"
  fichier "AGENTS.md" "$MARQUEUR"
}

verifier_chatgpt() {
  info "ChatGPT (GPT personnalisé)"
  echo "  Rien à vérifier sur disque : les fichiers sont téléversés dans le GPT."
  echo "  Contrôlez dans l'interface du GPT que la section Connaissances contient"
  echo "  les 5 fichiers de versions/chatgpt/connaissances/ et que les Instructions"
  echo "  reprennent versions/chatgpt/instructions-gpt.md."
}

case "$OUTIL" in
  continue)     verifier_continue ;;
  claude-code)  verifier_claude_code ;;
  gemini-cli)   verifier_gemini ;;
  opencode)     verifier_opencode ;;
  mistral-vibe) verifier_vibe ;;
  kimi-cli)     verifier_kimi ;;
  kilo)         verifier_kilo ;;
  cursor)       verifier_cursor ;;
  copilot)      verifier_copilot ;;
  codex)        verifier_codex ;;
  chatgpt)      verifier_chatgpt ;;
  auto)
    printf 'Détection des outils installés dans %s\n' "$PROJET"
    TROUVE=0
    [ -d "$PROJET/.continue/rules" ] && { verifier_continue; TROUVE=1; }
    [ -f "$PROJET/CLAUDE.md" ]       && { verifier_claude_code; TROUVE=1; }
    [ -f "$PROJET/GEMINI.md" ]       && { verifier_gemini; TROUVE=1; }
    [ -d "$PROJET/.opencode" ]       && { verifier_opencode; TROUVE=1; }
    [ -d "$PROJET/.vibe" ]           && { verifier_vibe; TROUVE=1; }
    [ -d "$PROJET/.kimi" ]           && { verifier_kimi; TROUVE=1; }
    [ -d "$PROJET/.kilo/rules" ]     && { verifier_kilo; TROUVE=1; }
    [ -d "$PROJET/.cursor/rules" ]   && { verifier_cursor; TROUVE=1; }
    [ -d "$PROJET/.github/instructions" ] && { verifier_copilot; TROUVE=1; }
    if [ "$TROUVE" -eq 0 ] && [ -f "$PROJET/AGENTS.md" ]; then verifier_codex; TROUVE=1; fi
    if [ "$TROUVE" -eq 0 ]; then
      echo "  Aucun fichier de règles trouvé. Copiez d'abord la version de votre outil"
      echo "  depuis versions/ (voir le README)."
      exit 1
    fi
    ;;
  *)
    echo "Outil inconnu : $OUTIL"
    echo "Attendu : continue | claude-code | cursor | copilot | gemini-cli | opencode | mistral-vibe | kimi-cli | kilo | codex | chatgpt"
    exit 2
    ;;
esac

info "Résultat : $OK contrôle(s) au vert, $KO au rouge"
if [ "$KO" -gt 0 ]; then
  echo "  Fichiers manquants : recopiez le dossier versions/<outil>/ à la racine du projet."
  exit 1
fi
echo "  Étape 2 : faites relire verification/exemple-a-corriger.html par votre assistant"
echo "  et comparez à verification/resultats-attendus.md."
