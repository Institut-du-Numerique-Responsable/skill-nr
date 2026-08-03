## Ce que change cette PR

<!-- Une ou deux phrases. Quel écart de sobriété ou d'accessibilité est mieux couvert après ? -->

## Type

- [ ] Nouvelle règle ou consigne
- [ ] Nouveau langage
- [ ] Correction d'un faux positif / faux négatif
- [ ] Documentation
- [ ] Outillage (scripts, CI)

## Critères source

<!-- Obligatoire pour toute consigne. Les identifiants doivent exister dans referentiels/ :
     la CI le vérifie et échoue sinon. Ex. GR491_Backend_3, Opquast n°124, RGAA 7.1 -->

## Vérifications

- [ ] `bash scripts/verifier-depot.sh` passe en local
- [ ] `python3 scripts/generer-versions.py` relancé si `.continue/` a changé
- [ ] Testé sur la branche `test-eco` (pièges par langage), ou sur `verification/`

### Effet mesuré sur la détection

<!-- Si la PR touche aux règles ou aux agents, donnez le score avant/après :

     cn review --review-agents .continue/agents/eco-check.md verification/exemple-a-corriger.* \
       | python3 scripts/scorer-detection.py

     Avant : ..  / 18      Après : ..  / 18
     Une règle qui n'améliore aucun score mérite d'être discutée : chaque ligne
     ajoutée coûte du contexte à toutes les sessions. -->
