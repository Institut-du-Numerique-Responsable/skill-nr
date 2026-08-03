-- Fichier de test volontairement non conforme. Ne pas corriger dans ce dépôt :
-- il sert à vérifier qu'un assistant IA a bien chargé les règles.
-- Écarts attendus détaillés dans verification/resultats-attendus.md

-- Export des clients actifs et de leurs commandes de l'année
SELECT *
FROM clients c
JOIN commandes cmd ON cmd.client_id = c.id
JOIN lignes_commande lc ON lc.commande_id = cmd.id
WHERE UPPER(c.nom) LIKE '%DUPONT%'
  AND YEAR(cmd.date_creation) = 2026
ORDER BY cmd.date_creation DESC;

-- Journal de navigation, conservé pour analyse
CREATE TABLE journal_navigation (
    id          BIGINT PRIMARY KEY,
    client_id   BIGINT,
    adresse_ip  VARCHAR(45),
    user_agent  VARCHAR(512),
    url         VARCHAR(2048),
    consulte_le TIMESTAMP
);
