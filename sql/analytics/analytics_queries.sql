-- Check if Your Tables Still Exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

-- Count number of records in matches table
SELECT COUNT(*) 
FROM matches_raw;

-- Count number of record in deliveries table
SELECT COUNT(*) 
FROM deliveries_raw;

-- Analytics queries 

-- How many matches were played in each IPL season?

SELECT season, COUNT(*) AS total_matches
FROM matches_raw 
GROUP BY season 
ORDER BY season;

-- Which teams have won the most matches?

SELECT winner, COUNT(*) AS total_wins 
FROM matches_raw 
WHERE winner IS NOT NULL
GROUP BY winner 
ORDER BY total_wins DESC;

-- Which venues hosted the most matches?

SELECT venue, COUNT(*) AS matches_hosted
FROM matches_raw
GROUP BY venue
ORDER BY matches_hosted DESC;

-- How often do teams choose to bat or field after winning the toss?
SELECT toss_decision, COUNT(*) AS total_matches
FROM matches_raw
GROUP BY toss_decision
ORDER BY total_matches DESC;

-- Top 10 run scorers in IPL history

SELECT batter, 
SUM(batsman_runs) AS total_runs 
FROM deliveries_raw
GROUP BY batter 
ORDER BY total_runs DESC
LIMIT 10;

-- Top 10 wicket takers

SELECT bowler,
COUNT(*) AS wickets
FROM deliveries_raw
WHERE is_wicket = 1
GROUP BY bowler 
ORDER BY wickets DESC 
LIMIT 10;


-- Which teams have scored the most runs overall?
SELECT batting_team,
SUM(total_runs) AS total_team_runs
FROM deliveries_raw
GROUP BY batting_team
ORDER BY total_team_runs DESC;

-- How often does toss winner also win the match?

SELECT 
	COUNT(*) AS total_matches, 
		SUM(
			CASE 
				WHEN toss_winner = winner THEN 1  
				ELSE 0
			END 
		) AS toss_match_win
FROM matches_raw;