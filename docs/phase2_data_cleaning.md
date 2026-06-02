# Phase 2 - Data Cleaning

## Objectives

- Create cleaned analytical tables
- Standardize team names
- Audit null values
- Validate duplicates
- Validate run values
- Create season_year field

## Cleaning Performed

### Team Standardization

Delhi Daredevils -> Delhi Capitals

Kings XI Punjab -> Punjab Kings

Royal Challengers Bangalore -> Royal Challengers Bengaluru

Rising Pune Supergiant -> Rising Pune Supergiants

### Null Value Audit

city = 0 nulls

player_of_match = 0 nulls

method = 0 nulls

### Validation

No duplicate match IDs

No duplicate deliveries

No negative run values

Valid wicket indicators

## Output

matches_clean

deliveries_clean