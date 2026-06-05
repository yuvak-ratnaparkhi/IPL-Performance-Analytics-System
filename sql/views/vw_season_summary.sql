-- ==========================================
-- View 2 : Season Summary 
-- ==========================================

CREATE OR REPLACE VIEW vw_season_summary AS

SELECT
    season,
    COUNT(DISTINCT id) AS matches_played
FROM matches_clean
GROUP BY season;


-- ==========================================
-- Validation Query
-- ==========================================

SELECT *
FROM vw_season_summary
ORDER BY season;

