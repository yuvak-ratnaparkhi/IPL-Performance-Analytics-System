-- ==========================================
-- View 7 : Team Head To Head Statistics
-- ==========================================


CREATE OR REPLACE VIEW vw_head_to_head AS 

SELECT 
    LEAST(team1, team2) AS team_a,
    GREATEST(team1, team2) AS team_b,

    COUNT(*) AS matches_played,

    SUM (
        CASE
            WHEN winner = LEAST(team1, team2) THEN 1
            ELSE 0
        END
    ) AS team_a_wins,

    SUM (
        CASE 
            WHEN winner = GREATEST(team1, team2) THEN 1
            ELSE 0
        END
    ) AS team_b_wins,

    ROUND (
        SUM (
            CASE 
                WHEN winner = LEAST(team1, team2) THEN 1 
                ELSE 0
            END 
        ) :: NUMERIC / COUNT(*) * 100,
        2
    ) AS team_a_win_percentage,

    ROUND (
        SUM (
            CASE 
                WHEN winner = GREATEST(team1, team2) THEN 1 
                ELSE 0
            END
        ) :: NUMERIC / COUNT(*) * 100, 
        2
    ) AS team_b_win_percentage

FROM matches_clean

WHERE winner IS NOT NULL
    AND winner <> 'NA'

GROUP BY 
    LEAST(team1, team2),
    GREATEST(team1, team2);


-- ==========================================
-- Validation Query
-- ==========================================

SELECT * 
FROM vw_head_to_head
ORDER BY matches_played DESC;

-- Phase 4 Final Verification

SELECT table_name
FROM information_schema.views
WHERE table_schema = 'public'
ORDER BY table_name;