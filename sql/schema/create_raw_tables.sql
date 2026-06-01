-- =========================================
-- IPL Analytics Database Schema
-- Raw Layer Tables
-- =========================================

-- Drop existing tables

DROP TABLE IF EXISTS deliveries_raw;
DROP TABLE IF EXISTS matches_raw CASCADE;

-- =========================================
-- Matches Table
-- =========================================

CREATE TABLE matches_raw (
    id BIGINT PRIMARY KEY,
    season VARCHAR(20),
    city VARCHAR(100),
    date DATE,
    match_type VARCHAR(50),
    player_of_match VARCHAR(150),
    venue TEXT,
    team1 VARCHAR(100),
    team2 VARCHAR(100),
    toss_winner VARCHAR(100),
    toss_decision VARCHAR(20),
    winner VARCHAR(100),
    result VARCHAR(50),
    result_margin VARCHAR(20),
    target_runs VARCHAR(20),
    target_overs VARCHAR(20),
    super_over VARCHAR(10),
    method VARCHAR(100),
    umpire1 VARCHAR(100),
    umpire2 VARCHAR(100)
);

-- =========================================
-- Deliveries Table
-- =========================================

CREATE TABLE deliveries_raw (
    match_id BIGINT,
    inning INT,
    batting_team VARCHAR(100),
    bowling_team VARCHAR(100),
    over_num INT,
    ball INT,
    batter VARCHAR(150),
    bowler VARCHAR(150),
    non_striker VARCHAR(150),
    batsman_runs INT,
    extra_runs INT,
    total_runs INT,
    extras_type VARCHAR(50),
    is_wicket INT,
    player_dismissed VARCHAR(150),
    dismissal_kind VARCHAR(100),
    fielder VARCHAR(150)
);