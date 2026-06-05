-- ========================================== 
-- View 3 : Player Batting Statitics 
-- ========================================== 

CREATE OR REPLACE VIEW vw_player_batting_stats AS

SELECT 
    batter,
    SUM(batsman_runs) AS total_runs,
    COUNT(*) AS balls_faced,
    ROUND (
        (SUM(batsman_runs) :: NUMERIC / COUNT(*)) * 100, 2
    ) AS strike_rate,

    SUM (
        CASE
            WHEN batsman_runs = 4 THEN 1 
            ELSE 0
        END
        ) AS fours,

    SUM (
        CASE
            WHEN batsman_runs = 6 THEN 1 
            ELSE 0
        END 
    ) AS sixes
FROM deliveries_clean
GROUP BY batter;


-- ==========================================
-- Validation Query
-- ==========================================

SELECT *
FROM vw_player_batting_stats
ORDER BY total_runs DESC
LIMIT 10;
