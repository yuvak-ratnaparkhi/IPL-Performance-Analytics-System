-- ==========================================
-- View 6 : Team Season Performance
-- ==========================================

CREATE OR REPLACE VIEW vw_team_season_performance AS

SELECT
    season,
    team_name,
    matches_played,
    matches_won,
    win_percentage,

    RANK() OVER (
        PARTITION BY season
        ORDER BY matches_won DESC
    ) AS season_rank

FROM
(
    SELECT
        season,
        team_name,
        COUNT(*) AS matches_played,

        SUM(
            CASE
                WHEN winner = team_name THEN 1
                ELSE 0
            END
        ) AS matches_won,

        ROUND(
            SUM(
                CASE
                    WHEN winner = team_name THEN 1
                    ELSE 0
                END
            )::NUMERIC / COUNT(*) * 100,
            2
        ) AS win_percentage

    FROM
    (
        SELECT
            season,
            team1 AS team_name,
            winner
        FROM matches_clean

        UNION ALL

        SELECT
            season,
            team2 AS team_name,
            winner
        FROM matches_clean
    ) teams

    GROUP BY
        season,
        team_name
) season_stats;



-- ==========================================
-- Validation Query
-- ==========================================

SELECT *
FROM vw_team_season_performance
ORDER BY season, matches_won DESC;

SELECT *
FROM vw_season_summary;