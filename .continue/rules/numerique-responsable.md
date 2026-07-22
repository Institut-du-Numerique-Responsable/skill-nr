---
name: Numérique responsable
description: Principes transverses de numérique responsable, accessibilité, inclusion, durabilité, protection des données
alwaysApply: true
---

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
- Dans tes réponses, cite le critère concerné quand tu appliques une règle (ex. « RGESN 4.x », « RGAA 10.x ») pour faciliter la montée en compétence de l'équipe.
