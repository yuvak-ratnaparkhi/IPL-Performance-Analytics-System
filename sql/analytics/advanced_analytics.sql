-- =====================================================
-- Query 1: Top Run Scorer In Every Season
-- =====================================================

WITH batter_runs AS (
    SELECT
        m.season_year,
        d.batter,
        SUM(d.batsman_runs) AS runs
    FROM deliveries_clean d
    JOIN matches_clean m
        ON d.match_id = m.id
    GROUP BY
        m.season_year,
        d.batter
),

ranked_batters AS (
    SELECT
        season_year,
        batter,
        runs,
        RANK() OVER (
            PARTITION BY season_year
            ORDER BY runs DESC
        ) AS batter_rank
    FROM batter_runs
)

SELECT
    season_year,
    batter,
    runs
FROM ranked_batters
WHERE batter_rank = 1
ORDER BY season_year;


-- =====================================================
-- Query 2: Official Top Wicket Taker In Every Season
-- =====================================================

WITH bowler_wickets AS (
    SELECT
        m.season_year,
        d.bowler,
        COUNT(*) AS wickets
    FROM deliveries_clean d
    JOIN matches_clean m
        ON d.match_id = m.id
    WHERE d.dismissal_kind IN (
        'bowled',
        'caught',
        'caught and bowled',
        'hit wicket',
        'lbw',
        'stumped'
    )
    GROUP BY
        m.season_year,
        d.bowler
),

ranked_bowlers AS (
    SELECT
        season_year,
        bowler,
        wickets,
        RANK() OVER (
            PARTITION BY season_year
            ORDER BY wickets DESC
        ) AS bowler_rank
    FROM bowler_wickets
)

SELECT
    season_year,
    bowler,
    wickets
FROM ranked_bowlers
WHERE bowler_rank = 1
ORDER BY season_year;



-- =====================================================
-- Query 3: Team Rankings By Season
-- =====================================================

WITH team_wins AS (
    SELECT
        season_year,
        winner,
        COUNT(*) AS wins
    FROM matches_clean
    WHERE winner IS NOT NULL
      AND winner <> 'NA'
    GROUP BY
        season_year,
        winner
),

ranked_teams AS (
    SELECT
        season_year,
        winner,
        wins,
        DENSE_RANK() OVER (
            PARTITION BY season_year
            ORDER BY wins DESC
        ) AS team_rank
    FROM team_wins
)

SELECT
    season_year,
    winner AS team_name,
    wins,
    team_rank
FROM ranked_teams
ORDER BY
    season_year,
    team_rank;


-- =====================================================
-- Query 4: Top 5 Run Scorers Per Season
-- =====================================================

WITH player_runs AS (
    SELECT
        m.season_year,
        d.batter,
        SUM(d.batsman_runs) AS runs,
        ROW_NUMBER() OVER (
            PARTITION BY m.season_year
            ORDER BY SUM(d.batsman_runs) DESC
        ) AS rank
    FROM deliveries_clean d
    JOIN matches_clean m
        ON d.match_id = m.id
    GROUP BY
        m.season_year,
        d.batter
)

SELECT
    season_year,
    batter,
    runs
FROM player_runs
WHERE rank <= 5
ORDER BY
    season_year,
    rank;



-- =====================================================
-- Query 5: Best Batting Partnerships
-- =====================================================

SELECT
    batter,
    non_striker,
    SUM(total_runs) AS partnership_runs
FROM deliveries_clean
GROUP BY
    batter,
    non_striker
ORDER BY partnership_runs DESC
LIMIT 10;



-- OR Here , 


SELECT
    LEAST(batter, non_striker) AS player1,
    GREATEST(batter, non_striker) AS player2,
    SUM(total_runs) AS partnership_runs
FROM deliveries_clean
GROUP BY
    LEAST(batter, non_striker),
    GREATEST(batter, non_striker)
ORDER BY partnership_runs DESC
LIMIT 10;


-- =====================================================
-- Query 6: Chase Success Analysis
-- =====================================================

SELECT
    toss_decision,
    COUNT(*) AS matches,
    SUM(
        CASE
            WHEN winner = toss_winner
            THEN 1
            ELSE 0
        END
    ) AS wins
FROM matches_clean
GROUP BY toss_decision;


-- =====================================================
-- Query 7: Most Successful Teams By Venue
-- =====================================================

SELECT
    venue,
    winner,
    COUNT(*) AS wins
FROM matches_clean
WHERE winner IS NOT NULL
    AND winner <> 'NA'
GROUP BY
    venue,
    winner
ORDER BY wins DESC
LIMIT 20;


-- =====================================================
-- Query 8: Toss Impact Analysis
-- =====================================================

SELECT
    COUNT(*) AS total_matches,
    SUM(
        CASE
            WHEN toss_winner = winner
            THEN 1
            ELSE 0
        END
    ) AS toss_and_match_wins,
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN toss_winner = winner
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS win_percentage
FROM matches_clean;


-- =====================================================
-- Query 9: Most Successful Team At Each Venue
-- Business Question:
-- Which team has won the most matches at each IPL venue?
-- =====================================================

WITH venue_wins AS (
    SELECT
        venue,
        winner,
        COUNT(*) AS wins,
        ROW_NUMBER() OVER (
            PARTITION BY venue
            ORDER BY COUNT(*) DESC
        ) AS rank
    FROM matches_clean
    WHERE winner IS NOT NULL
      AND winner <> 'NA'
    GROUP BY
        venue,
        winner
)

SELECT
    venue,
    winner AS most_successful_team,
    wins
FROM venue_wins
WHERE rank = 1
ORDER BY wins DESC;

-- check dataset for dismissal kinds and fielder nulls

-- SELECT DISTINCT dismissal_kind 
-- FROM deliveries_clean 
-- ORDER BY dismissal_kind;


-- venue variation 

-- SELECT DISTINCT venue
-- FROM matches_clean 
-- ORDER BY venue;
