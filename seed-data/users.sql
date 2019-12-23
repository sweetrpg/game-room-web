
INSERT INTO users (
  "email", "nickname", "name", "avatar_url"
) VALUES (
  'dm@sweetrpg.com',
  'system',
  'System',
  ''
);

INSERT INTO identities (
  "user_id", "source", "subject"
) VALUES (
  (SELECT "id" FROM users WHERE "nickname" = 'system'),
  'system',
  'system'
);
