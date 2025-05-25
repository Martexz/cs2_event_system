CREATE VIEW players_by_country AS
SELECT p.player_id, p.nickname, p.country, t.team_name, t.country AS team_country
FROM players p
LEFT JOIN teams t ON p.team_id = t.team_id
ORDER BY p.country;