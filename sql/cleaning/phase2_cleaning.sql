-- =====================================================
-- IPL Performance Analytics System
-- Phase 2: Data Cleaning & Preprocessing
-- =====================================================

-- =====================================================
-- STEP 1: Create Clean Tables
-- =====================================================

DROP TABLE IF EXISTS matches_clean;

CREATE TABLE matches_clean AS
SELECT *
FROM matches_raw;


DROP TABLE IF EXISTS deliveries_clean;

CREATE TABLE deliveries_clean AS
SELECT *
FROM deliveries_raw;


-- =====================================================
-- STEP 2: Verify Row Counts
-- =====================================================

SELECT COUNT(*) AS matches_count
FROM matches_clean;

SELECT COUNT(*) AS deliveries_count
FROM deliveries_clean;


-- =====================================================
-- STEP 3: Null Value Analysis (Matches)
-- =====================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(city) AS null_city,
    COUNT(*) - COUNT(player_of_match) AS null_player_of_match,
    COUNT(*) - COUNT(winner) AS null_winner,
    COUNT(*) - COUNT(method) AS null_method
FROM matches_clean;


-- =====================================================
-- STEP 4: Null Value Analysis (Deliveries)
-- =====================================================

SELECT
    COUNT(*) - COUNT(extras_type) AS null_extras_type,
    COUNT(*) - COUNT(player_dismissed) AS null_player_dismissed,
    COUNT(*) - COUNT(dismissal_kind) AS null_dismissal_kind,
    COUNT(*) - COUNT(fielder) AS null_fielder
FROM deliveries_clean;


-- =====================================================
-- STEP 5: Duplicate Match ID Check
-- =====================================================

SELECT
    id,
    COUNT(*)
FROM matches_clean
GROUP BY id
HAVING COUNT(*) > 1;


-- =====================================================
-- STEP 6: Duplicate Delivery Check
-- =====================================================

SELECT
    match_id,
    inning,
    over_num,
    ball,
    COUNT(*)
FROM deliveries_clean
GROUP BY
    match_id,
    inning,
    over_num,
    ball
HAVING COUNT(*) > 1;


-- =====================================================
-- STEP 7: Team Name Audit
-- =====================================================

SELECT DISTINCT team1
FROM matches_clean
ORDER BY team1;


-- Create Clean Tables

CREATE TABLE matches_clean AS
SELECT * FROM matches_raw;

CREATE TABLE deliveries_clean AS
SELECT * FROM deliveries_raw;

-- Team Standardization : matches_clean
-- =====================================================
-- STEP 1: 
-- =====================================================
-- 1. DELHI CAPITALS
UPDATE matches_clean
SET team1 = 'Delhi Capitals'
WHERE team1 = 'Delhi Daredevils';

UPDATE matches_clean
SET team2 = 'Delhi Capitals'
WHERE team2 = 'Delhi Daredevils';

UPDATE matches_clean
SET toss_winner = 'Delhi Capitals'
WHERE toss_winner = 'Delhi Daredevils';

UPDATE matches_clean
SET winner = 'Delhi Capitals'
WHERE winner = 'Delhi Daredevils';


-- Team Standardization : deliveries_clean

-- =====================================================
-- STEP 1: Update batting_team
-- =====================================================


UPDATE deliveries_clean
SET batting_team = 'Delhi Capitals'
WHERE batting_team = 'Delhi Daredevils';

UPDATE deliveries_clean
SET batting_team = 'Punjab Kings'
WHERE batting_team = 'Kings XI Punjab';

UPDATE deliveries_clean
SET batting_team = 'Royal Challengers Bengaluru'
WHERE batting_team = 'Royal Challengers Bangalore';

UPDATE deliveries_clean
SET batting_team = 'Rising Pune Supergiants'
WHERE batting_team = 'Rising Pune Supergiant';


-- =====================================================
-- STEP 2: Update bowling_team
-- =====================================================


UPDATE deliveries_clean
SET bowling_team = 'Delhi Capitals'
WHERE bowling_team = 'Delhi Daredevils';

UPDATE deliveries_clean
SET bowling_team = 'Punjab Kings'
WHERE bowling_team = 'Kings XI Punjab';

UPDATE deliveries_clean
SET bowling_team = 'Royal Challengers Bengaluru'
WHERE bowling_team = 'Royal Challengers Bangalore';

UPDATE deliveries_clean
SET bowling_team = 'Rising Pune Supergiants'
WHERE bowling_team = 'Rising Pune Supergiant';


-- Validation Queries

-- 

SELECT DISTINCT team1 FROM matches_clean  ORDER BY team1;
SELECT DISTINCT team2 FROM matches_clean  ORDER BY team2;
SELECT DISTINCT toss_winner FROM matches_clean  ORDER BY toss_winner;
SELECT DISTINCT winner FROM matches_clean  ORDER BY winner;

-- 

SELECT DISTINCT batting_team FROM deliveries_clean ORDER BY batting_team;
SELECT DISTINCT bowling_team FROM deliveries_clean ORDER BY bowling_team;