-- ==========================================
-- View 4 : Player Bowling Statistics
-- ==========================================

CREATE OR REPLACE VIEW vw_player_bowling_stats AS 

SELECT 
    bowler,
    COUNT(*) FILTER (
        WHERE dismissal_kind IN 
        (
            'bowled',
            'caught',
            'caught and bowled',
            'lbw',
            'stumped',
            'hit wicket'
        ) 
    ) AS total_wickets,

    COUNT(*) AS balls_bowled,

    SUM (total_runs) AS runs_conceded,

    ROUND (SUM 
        (total_runs) :: NUMERIC / COUNT(*) * 6, 
        2
    ) AS economy_rate

FROM deliveries_clean 
GROUP BY bowler;


-- ==========================================
-- Validation Query
-- ==========================================

SELECT *
FROM vw_player_bowling_stats 
ORDER BY total_wickets DESC
LIMIT 10;