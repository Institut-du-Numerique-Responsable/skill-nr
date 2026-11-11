<!-- Fichier généré par scripts/generer-versions.py, ne pas éditer à la main.
     Source : .continue/rules/ -->

# Règles Numérique Responsable : écoconception et accessibilité

Ces règles s'appliquent à tout code que tu écris ou modifies dans ce projet.
Chaque section « S'applique aux fichiers » ne concerne que les fichiers de son
langage : applique-la quand tu travailles sur ce type de fichier, ignore-la sinon.
Cite le critère source (RGESN x.x, GR491_xxx, Opquast n°xxx) quand tu appliques
une règle, pour la montée en compétence de l'équipe.

Référentiels : RGESN v2 (ARCEP/ARCOM/ADEME), GR491 (INR), Opquast (CC BY-SA), RGAA 4.

# Principes de numérique responsable (transverses)

Ces principes s'appliquent à toute contribution, quel que soit le langage ou la couche technique.

## Accessibilité (RGAA / WCAG)

- Tout HTML produit doit être sémantique (balises appropriées, hiérarchie de titres cohérente, `alt` pertinents, labels de formulaires associés).
- Contraste suffisant, navigation clavier complète, focus visible, pas d'information portée uniquement par la couleur.
- Vise la conformité RGAA 4 ; signale tout écart que tu ne peux pas corriger dans le périmètre de la tâche.

## Durabilité et pérennité

- Compatibilité large : le service doit fonctionner sur des appareils anciens et des connexions lentes (RGESN : ne pas contribuer à l'obsolescence des terminaux).
- Prévois une dégradation gracieuse quand une fonctionnalité avancée n'est pas disponible.
- Documente ce que tu produis pour en permettre la maintenance (README, commentaires sur les contraintes non évidentes).

## Protection des données et sobriété des collectes

- Minimisation : ne collecte et ne conserve que les données strictement nécessaires à la fonctionnalité (RGPD, article 5).
- Pas de traceur ou de mesure d'audience ajouté sans demande explicite et sans base légale identifiée.
- Aucun secret (clé, jeton, mot de passe) en dur dans le code ou les fichiers versionnés.

## Posture de l'assistant

- Quand une demande entre en tension avec ces principes (fonctionnalité superflue, collecte excessive, dépendance lourde), réalise la tâche demandée si elle est légitime mais mentionne explicitement la tension et propose une alternative plus sobre.
- Dans tes réponses, cite le critère concerné quand tu appliques une règle (ex. « RGESN 6.1 », « RGAA 1.1 ») pour faciliter la montée en compétence de l'équipe.

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
  disponible : proportionne l'effort à la complexité réelle de la tâche. Compare les modèles sur une même tâche et un niveau de qualité explicite ;
  aucun ratio de consommation ne peut être déduit de leur taille seule.
- Pour l'automatisation récurrente (CI, scripts), démarre sans contexte projet superflu
  et mets en cache les réponses à des requêtes identiques quand c'est possible.

## Qualité et mesure

- Arrête les vérifications quand les critères d’acceptation sont satisfaits, sauf nouveau
  risque ou changement. Compte aussi les essais échoués et les corrections.
- Ne sacrifie ni exactitude, sécurité, accessibilité, maintenabilité ni clarté pour
  économiser du contexte ou du calcul.
- Si le client expose les métriques, relève les tokens d’entrée, de sortie et de cache,
  le coût et les appels sur une tâche comparable. Sinon indique « indisponible ».
  Ne convertis pas des tokens en énergie ou en carbone sans mesure adaptée.
- Après une tâche outillée, rapporte brièvement les optimisations appliquées, les tests,
  leurs résultats et les limites ; aucun pourcentage d’économie sans référence comparable.

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

## Règles spécialisées à lire à la demande

Avant de modifier ou relire un fichier, lis les références correspondant à son langage et à sa couche technique, depuis la racine du projet. Ne charge pas les autres références. Si un fichier manque, signale l’installation incomplète. Ces chemins ne sont pas des imports automatiques.

- `**/*.{js,ts,py,java,go,rb,rs,php,sql,kt,cs,c,cc,cpp}` : `.nr/regles/ecoconception-backend.md`
- `**/*.{html,css,scss,js,jsx,ts,tsx,vue,svelte}` : `.nr/regles/ecoconception-frontend.md`
- `**/*.{html,css,scss,js,jsx,ts,tsx,vue,svelte,cshtml,jsp,twig,razor}` : `.nr/regles/qualite-web-opquast.md`
- `**/*.{sql,pks,pkb,prc,fnc,trg}` : `.nr/regles/ecoconception-sql.md`
- `**/*.{js,jsx,ts,tsx,mjs,cjs}` : `.nr/regles/ecoconception-javascript.md`
- `**/*.java` : `.nr/regles/ecoconception-java.md`
- `**/*.cs` : `.nr/regles/ecoconception-csharp.md`
- `**/*.py` : `.nr/regles/ecoconception-python.md`
- `**/*.php` : `.nr/regles/ecoconception-php.md`
- `**/*.rb` : `.nr/regles/ecoconception-ruby.md`
- `**/*.rs` : `.nr/regles/ecoconception-rust.md`
- `**/*.{c,h}` : `.nr/regles/ecoconception-c.md`
- `**/*.{cpp,cc,cxx,hpp,hh}` : `.nr/regles/ecoconception-cpp.md`
