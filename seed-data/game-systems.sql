
INSERT INTO game_systems (
  "creator_id", "created_at", "updated_at",
  "key", "name", "full_name", "edition", "details", "locked", "order"
)
VALUES
(
  (SELECT "id" FROM users WHERE nickname = 'system'),
  CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
  'none', 'None', 'No game system', '0', '', false, 0
),
(
  (SELECT "id" FROM users WHERE nickname = 'system'),
  CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
  'simple', 'Simple', 'Simple game system', '0', '', false, 1
),
(
  (SELECT "id" FROM users WHERE nickname = 'system'),
  CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
  'dnd5', 'D&D 5e', 'Dungeons & Dragons, 5th Edition', '5', '', true, NULL
);
