---
name: Usage sobre de l'assistant IA
description: Pratiques pour minimiser le coût en tokens et en calcul de la session elle-même, indépendamment du code produit
alwaysApply: true
---

# Usage sobre de l'assistant IA

La sobriété numérique ne s'arrête pas au code produit : la session avec l'assistant a
elle-même un coût en calcul. Le contexte envoyé au modèle est retraité à chaque tour de
conversation. Un contexte obèse ou une conversation-fleuve multiplie ce coût sur tous
les échanges suivants, pas seulement le dernier. Applique ces pratiques à ta propre
conduite de session, pas seulement au code que tu écris.

## Contexte minimal

- Ne charge pas un fichier entier dans le contexte si tu peux le lire à la demande au
  moment où tu en as besoin. Préfère un objectif clair et une capacité à aller chercher
  l'information plutôt qu'un contexte pré-rempli exhaustif.
- Ne relis pas un fichier déjà lu dans la session sauf s'il a pu changer entre-temps.
- Un index du dépôt (type `CODEMAP.md`) évite de redécouvrir la structure du projet à
  chaque session : consulte-le d'abord, ne recartographie pas le code inutilement.

## Corriger sans polluer

- Quand une tentative échoue, ne l'empile pas dans l'historique en enchaînant les
  messages de correction : chaque essai raté reste dans le contexte et est retraité à
  chaque tour suivant. Reviens avant l'erreur si l'outil le permet (rewind, nouvelle
  branche de conversation) plutôt que de corriger par-dessus.
- Pour une tâche sans lien avec ce qui précède, démarre un contexte propre plutôt que de
  poursuivre une conversation déjà longue. Pour une tâche liée, résume l'historique avec
  une consigne ciblée (ce qu'il faut garder, ce qu'il faut jeter) plutôt que de tout
  conserver tel quel.

## Capitaliser plutôt que répéter

- Une leçon apprise en session (une convention, une erreur récurrente, une contrainte du
  projet) se documente dans un fichier de règles versionné. La corriger seulement dans
  la conversation en cours la reperd à la prochaine session.
- Donne-toi un moyen de vérification déterministe (tests, build, commande) plutôt que de
  multiplier les tours de relecture manuelle : une vérification automatisée coûte moins
  cher qu'un aller-retour de plus avec le modèle.

## Proportionner la puissance à la tâche

- N'utilise pas systématiquement le modèle ou le niveau de raisonnement le plus élevé
  disponible : proportionne l'effort à la complexité réelle de la tâche. Un modèle plus
  petit bien choisi consomme un ordre de grandeur de moins pour un résultat équivalent
  sur une tâche simple.
- Pour l'automatisation récurrente (CI, scripts), démarre sans contexte projet superflu
  et mets en cache les réponses à des requêtes identiques quand c'est possible.

## Repères par outil

Les mécanismes exacts diffèrent selon l'assistant utilisé ; le principe (contexte propre,
pas de correction empilée, effort proportionné) reste le même partout.

- **Continue (`cn`)** : `--resume` reprend la dernière session, `--fork <id>` repart
  d'un point antérieur sans réembarquer les tours suivants ; `ls` liste les sessions.
- **Claude Code** : rembobiner avec un double appui sur Échap, `/clear` pour une tâche
  sans lien, `/compact <consigne>` pour résumer une tâche liée, `/effort` pour ajuster
  le niveau de raisonnement.
- **Gemini CLI, OpenCode, Mistral Vibe, ChatGPT** : vérifie la commande équivalente de
  gestion de session/contexte dans la documentation de l'outil ; le principe ci-dessus
  s'applique quel que soit son nom exact.
