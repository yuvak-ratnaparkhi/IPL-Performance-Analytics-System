-- ==========================================
-- View 1 : Team Performance 
-- ==========================================

CREATE OR REPLACE VIEW vw_team_performance AS 

SELECT 
    winner AS team_name,
    COUNT(*) AS matches_won
FROM matches_clean 
WHERE winner IS NOT NULL
    AND winner <> 'NA'   --<> = NOT EQUAL TO 
GROUP BY winner;


-- ==========================================
-- Validation Query
-- ==========================================

SELECT * 
FROM vw_team_performance
ORDER BY matches_won DESC;




