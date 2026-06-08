-- ==========================================
-- View 1 : Team Performance 
-- ==========================================


CREATE OR REPLACE VIEW vw_team_performance AS 

SELECT 
    team_name,

    COUNT(*) AS matches_played,

    SUM (
        CASE
            WHEN winner = team_name THEN 1
            ELSE 0
        END
    )AS matches_won,

    SUM(
        CASE
            WHEN winner IS NOT NULL
                AND winner <> 'NA'
                AND winner <> team_name
            THEN 1
            ELSE 0
        END
    ) AS matches_lost,

    ROUND (
        SUM (
            CASE 
                WHEN winner = team_name THEN 1 
                ELSE 0
            END
        ) :: NUMERIC / COUNT(*) * 100,
        2
    ) AS win_percentage

FROM 
(
    SELECT team1 AS team_name, winner
    FROM matches_clean

    UNION ALL 

    SELECT team2 AS team_name, winner
    FROM matches_clean
) teams

GROUP BY team_name;


-- ==========================================
-- Validation Query
-- ==========================================

SELECT * 
FROM vw_team_performance
ORDER BY matches_won DESC;





SELECT * 
FROM vw_team_performance 
LIMIT 5;