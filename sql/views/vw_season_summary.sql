-- ==========================================
-- View 2 : Season Summary 
-- ==========================================

CREATE OR REPLACE VIEW vw_season_summary AS

SELECT
    m.season,

    COUNT(DISTINCT m.id) AS matches_played,

    SUM(d.total_runs) AS total_runs,

    SUM(d.is_wicket) AS total_wickets,

    ROUND(
        SUM(d.total_runs) :: NUMERIC 
        / COUNT(DISTINCT m.id),
        2
    ) AS avg_runs_per_match

FROM matches_clean m

JOIN deliveries_clean d
    ON m.id = d.match_id

GROUP BY m.season;


-- ==========================================
-- Validation Query
-- ==========================================

SELECT *
FROM vw_season_summary
ORDER BY season;

