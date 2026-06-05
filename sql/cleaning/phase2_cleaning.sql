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
-- STEP 7: Team Name Standardization
-- =====================================================

-- ---------------------------------
-- DELHI DAREDEVILS → DELHI CAPITALS
-- ---------------------------------

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


-- ---------------------------------
-- KINGS XI PUNJAB → PUNJAB KINGS
-- ---------------------------------

UPDATE matches_clean
SET team1 = 'Punjab Kings'
WHERE team1 = 'Kings XI Punjab';

UPDATE matches_clean
SET team2 = 'Punjab Kings'
WHERE team2 = 'Kings XI Punjab';

UPDATE matches_clean
SET toss_winner = 'Punjab Kings'
WHERE toss_winner = 'Kings XI Punjab';

UPDATE matches_clean
SET winner = 'Punjab Kings'
WHERE winner = 'Kings XI Punjab';


-- ------------------------------------------------
-- ROYAL CHALLENGERS BANGALORE → BENGALURU
-- ------------------------------------------------

UPDATE matches_clean
SET team1 = 'Royal Challengers Bengaluru'
WHERE team1 IN (
    'Royal Challengers Bangalore',
    'Royal Challengers Bangaluru'
);

UPDATE matches_clean
SET team2 = 'Royal Challengers Bengaluru'
WHERE team2 IN (
    'Royal Challengers Bangalore',
    'Royal Challengers Bangaluru'
);

UPDATE matches_clean
SET toss_winner = 'Royal Challengers Bengaluru'
WHERE toss_winner IN (
    'Royal Challengers Bangalore',
    'Royal Challengers Bangaluru'
);

UPDATE matches_clean
SET winner = 'Royal Challengers Bengaluru'
WHERE winner IN (
    'Royal Challengers Bangalore',
    'Royal Challengers Bangaluru'
);


-- ------------------------------------------------
-- RISING PUNE SUPERGIANT → SUPERGIANTS
-- ------------------------------------------------

UPDATE matches_clean
SET team1 = 'Rising Pune Supergiants'
WHERE team1 = 'Rising Pune Supergiant';

UPDATE matches_clean
SET team2 = 'Rising Pune Supergiants'
WHERE team2 = 'Rising Pune Supergiant';

UPDATE matches_clean
SET toss_winner = 'Rising Pune Supergiants'
WHERE toss_winner = 'Rising Pune Supergiant';

UPDATE matches_clean
SET winner = 'Rising Pune Supergiants'
WHERE winner = 'Rising Pune Supergiant';


-- =====================================================
-- STEP 8: Team Standardization (Deliveries)
-- =====================================================

-- ---------------------------------
-- DELHI DAREDEVILS → DELHI CAPITALS
-- ---------------------------------

UPDATE deliveries_clean
SET batting_team = 'Delhi Capitals'
WHERE batting_team = 'Delhi Daredevils';

UPDATE deliveries_clean
SET bowling_team = 'Delhi Capitals'
WHERE bowling_team = 'Delhi Daredevils';


-- ---------------------------------
-- KINGS XI PUNJAB → PUNJAB KINGS
-- ---------------------------------

UPDATE deliveries_clean
SET batting_team = 'Punjab Kings'
WHERE batting_team = 'Kings XI Punjab';

UPDATE deliveries_clean
SET bowling_team = 'Punjab Kings'
WHERE bowling_team = 'Kings XI Punjab';


-- ------------------------------------------------
-- ROYAL CHALLENGERS BANGALORE → BENGALURU
-- ------------------------------------------------

UPDATE deliveries_clean
SET batting_team = 'Royal Challengers Bengaluru'
WHERE batting_team IN (
    'Royal Challengers Bangalore',
    'Royal Challengers Bangaluru'
);

UPDATE deliveries_clean
SET bowling_team = 'Royal Challengers Bengaluru'
WHERE bowling_team IN (
    'Royal Challengers Bangalore',
    'Royal Challengers Bangaluru'
);


-- ------------------------------------------------
-- RISING PUNE SUPERGIANT → SUPERGIANTS
-- ------------------------------------------------

UPDATE deliveries_clean
SET batting_team = 'Rising Pune Supergiants'
WHERE batting_team = 'Rising Pune Supergiant';

UPDATE deliveries_clean
SET bowling_team = 'Rising Pune Supergiants'
WHERE bowling_team = 'Rising Pune Supergiant';


-- =====================================================
-- STEP 9: Validation Queries
-- =====================================================

-- Match Table Validation

SELECT DISTINCT team1
FROM matches_clean
ORDER BY team1;

SELECT DISTINCT team2
FROM matches_clean
ORDER BY team2;

SELECT DISTINCT toss_winner
FROM matches_clean
ORDER BY toss_winner;

SELECT DISTINCT winner
FROM matches_clean
ORDER BY winner;


-- Delivery Table Validation

SELECT DISTINCT batting_team
FROM deliveries_clean
ORDER BY batting_team;

SELECT DISTINCT bowling_team
FROM deliveries_clean
ORDER BY bowling_team;


-- =====================================================
-- STEP 10: Master Team Audit
-- =====================================================

SELECT DISTINCT team_name
FROM (
    SELECT team1 AS team_name FROM matches_clean
    UNION
    SELECT team2 FROM matches_clean
    UNION
    SELECT toss_winner FROM matches_clean
    UNION
    SELECT winner FROM matches_clean
) teams
ORDER BY team_name;


-- =====================================================
-- STEP 11: Venue Standardization
-- =====================================================

-- Arun Jaitley Stadium
UPDATE matches_clean
SET venue = 'Arun Jaitley Stadium'
WHERE venue = 'Arun Jaitley Stadium, Delhi';

-- Brabourne Stadium
UPDATE matches_clean
SET venue = 'Brabourne Stadium'
WHERE venue = 'Brabourne Stadium, Mumbai';

-- Dr DY Patil Sports Academy
UPDATE matches_clean
SET venue = 'Dr DY Patil Sports Academy'
WHERE venue = 'Dr DY Patil Sports Academy, Mumbai';

-- Eden Gardens
UPDATE matches_clean
SET venue = 'Eden Gardens'
WHERE venue = 'Eden Gardens, Kolkata';

-- Himachal Pradesh Cricket Association Stadium
UPDATE matches_clean
SET venue = 'Himachal Pradesh Cricket Association Stadium'
WHERE venue = 'Himachal Pradesh Cricket Association Stadium, Dharamsala';

-- M Chinnaswamy Stadium
UPDATE matches_clean
SET venue = 'M Chinnaswamy Stadium'
WHERE venue IN (
    'M Chinnaswamy Stadium, Bengaluru',
    'M.Chinnaswamy Stadium'
);

-- MA Chidambaram Stadium
UPDATE matches_clean
SET venue = 'MA Chidambaram Stadium'
WHERE venue IN (
    'MA Chidambaram Stadium, Chepauk',
    'MA Chidambaram Stadium, Chepauk, Chennai'
);

-- Maharashtra Cricket Association Stadium
UPDATE matches_clean
SET venue = 'Maharashtra Cricket Association Stadium'
WHERE venue = 'Maharashtra Cricket Association Stadium, Pune';

-- Punjab Cricket Association IS Bindra Stadium
UPDATE matches_clean
SET venue = 'Punjab Cricket Association IS Bindra Stadium'
WHERE venue IN (
    'Punjab Cricket Association IS Bindra Stadium, Mohali',
    'Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh',
    'Punjab Cricket Association Stadium, Mohali'
);

-- Rajiv Gandhi International Stadium
UPDATE matches_clean
SET venue = 'Rajiv Gandhi International Stadium'
WHERE venue IN (
    'Rajiv Gandhi International Stadium, Uppal',
    'Rajiv Gandhi International Stadium, Uppal, Hyderabad'
);

-- Sawai Mansingh Stadium
UPDATE matches_clean
SET venue = 'Sawai Mansingh Stadium'
WHERE venue = 'Sawai Mansingh Stadium, Jaipur';

-- Wankhede Stadium
UPDATE matches_clean
SET venue = 'Wankhede Stadium'
WHERE venue = 'Wankhede Stadium, Mumbai';

-- Zayed Cricket Stadium
UPDATE matches_clean
SET venue = 'Zayed Cricket Stadium'
WHERE venue = 'Zayed Cricket Stadium, Abu Dhabi';


-- =====================================================
-- STEP 12: Season Standardization
-- =====================================================

UPDATE matches_clean
SET season = '2008'
WHERE season = '2007/08';

UPDATE matches_clean
SET season = '2010'
WHERE season = '2009/10';

UPDATE matches_clean
SET season = '2021'
WHERE season = '2020/21';


-- =====================================================
-- Validation: Verify Season Values
-- =====================================================

SELECT DISTINCT season
FROM matches_clean
ORDER BY season;