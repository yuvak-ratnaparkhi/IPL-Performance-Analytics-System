-- =====================================================
-- IPL Performance Analytics System
-- Phase 3.1 - Basic SQL Analytics
-- =====================================================


-- =====================================================
-- Query 1: Total IPL Matches
-- Business Question:
-- How many IPL matches are available?
-- =====================================================

SELECT COUNT(*) AS total_matches
FROM matches_clean;


-- =====================================================
-- Query 2: Matches Played Per Season
-- Business Question:
-- How has IPL match volume changed over time?
-- =====================================================

SELECT
    season_year,
    COUNT(*) AS matches_played
FROM matches_clean
GROUP BY season_year
ORDER BY season_year;


-- =====================================================
-- Query 3: Most Successful Teams
-- Business Question:
-- Which teams have won the most matches?
-- =====================================================

SELECT
    winner,
    COUNT(*) AS matches_won
FROM matches_clean
WHERE winner <> 'NA'
GROUP BY winner
ORDER BY matches_won DESC;


-- =====================================================
-- Query 4: Toss Impact Analysis
-- Business Question:
-- How often does toss winner also win the match?
-- =====================================================

SELECT
    COUNT(*) AS total_matches,
    SUM(
        CASE
            WHEN toss_winner = winner THEN 1
            ELSE 0
        END
    ) AS toss_and_match_wins
FROM matches_clean
WHERE winner <> 'NA';


-- =====================================================
-- Query 5: Toss Win Percentage
-- Business Question:
-- Does winning the toss provide an advantage?
-- =====================================================

SELECT
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN toss_winner = winner THEN 1
                ELSE 0
            END
        )
        /
        COUNT(*),
        2
    ) AS toss_win_percentage
FROM matches_clean
WHERE winner <> 'NA';


-- =====================================================
-- Query 6: Top Venues By Match Count
-- Business Question:
-- Which venues host the most IPL matches?
-- =====================================================

SELECT
    venue,
    COUNT(*) AS matches_hosted
FROM matches_clean
GROUP BY venue
ORDER BY matches_hosted DESC
LIMIT 10;


-- =====================================================
-- Query 7: Player Of The Match Leaders
-- Business Question:
-- Which players have won the most awards?
-- =====================================================

SELECT
    player_of_match,
    COUNT(*) AS awards
FROM matches_clean
GROUP BY player_of_match
ORDER BY COUNT(*) DESC
LIMIT 10;


-- =====================================================
-- Query 8: Highest Run Scorers
-- Business Question:
-- Who are the leading run scorers in IPL history?
-- =====================================================

SELECT
    batter,
    SUM(batsman_runs) AS total_runs
FROM deliveries_clean
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;


-- =====================================================
-- Query 9: Leading Dismissal Contributors
-- Business Question:
-- Which bowlers were involved in the most dismissals
-- across IPL history?
-- =====================================================

SELECT
    bowler,
    COUNT(*) AS dismissals
FROM deliveries_clean
WHERE is_wicket = 1
GROUP BY bowler
ORDER BY dismissals DESC
LIMIT 10;


-- =====================================================
-- Query 10: Average First Innings Score
-- Business Question:
-- What is the average first innings score in IPL history?
-- =====================================================

SELECT
    ROUND(AVG(team_score),2) AS avg_first_innings_score
FROM (
    SELECT
        match_id,
        SUM(total_runs) AS team_score
    FROM deliveries_clean
    WHERE inning = 1
    GROUP BY match_id
) t;