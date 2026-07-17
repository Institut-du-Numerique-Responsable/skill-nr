-- Rapport des clients actifs
SELECT *
FROM clients c
JOIN operations o ON o.client_id = c.id
WHERE UPPER(c.nom) LIKE '%DUPONT%'
  AND YEAR(o.date_operation) = 2026
ORDER BY o.date_operation DESC;

-- Historique complet pour l'export mensuel
SELECT * FROM operations;

-- Archivage : recopie ligne à ligne
DECLARE cur CURSOR FOR SELECT id FROM operations WHERE date_operation < '2020-01-01';
OPEN cur;
FETCH NEXT FROM cur INTO @id;
WHILE @@FETCH_STATUS = 0
BEGIN
    INSERT INTO operations_archive SELECT * FROM operations WHERE id = @id;
    DELETE FROM operations WHERE id = @id;
    FETCH NEXT FROM cur INTO @id;
END;
