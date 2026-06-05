-- ==========================================
-- View 5 : Venue Statistics
-- ==========================================

CREATE OR REPLACE VIEW vw_venue_statistics AS

SELECT
    m.venue,
    COUNT(DISTINCT m.id) AS matches_hosted,

    SUM(d.total_runs) AS total_runs_scored,

    ROUND (
        SUM(d.total_runs) :: NUMERIC /
        COUNT(DISTINCT m.id), 
        2
    ) AS average_runs_per_match

FROM matches_clean m

JOIN deliveries_clean d 
    ON m.id = d.match_id

GROUP BY m.venue;


-- ==========================================
-- Validation Query
-- ==========================================

SELECT * 
FROM vw_venue_statistics
ORDER BY matches_hosted DESC;