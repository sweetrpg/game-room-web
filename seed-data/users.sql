
INSERT INTO users (
  "email", "nickname", "name", "avatar_url"
)
VALUES
('dm@sweetrpg.com', 'system', 'System', '')
;

INSERT INTO identities (
  "user_id", "source", "subject"
)
VALUES
((SELECT "id" FROM users WHERE "nickname" = 'system'), 'system', 'system')
;

INSERT INTO roles (
  "name"
)
VALUES
('admin'),
('user')
;

INSERT INTO "permissions" (
  "role_id", "name"
)
VALUES
((SELECT "id" FROM "roles" WHERE "name" = 'user'), 'basic'),
((SELECT "id" FROM "roles" WHERE "name" = 'admin'), 'list_users'),
((SELECT "id" FROM "roles" WHERE "name" = 'admin'), 'modify_user'),
((SELECT "id" FROM "roles" WHERE "name" = 'admin'), 'add_game_system'),
((SELECT "id" FROM "roles" WHERE "name" = 'admin'), 'modify_game_system')
;

INSERT INTO "user_roles" (
"user_id", "role_id", "enabled"
)
VALUES
((SELECT "id" FROM users WHERE "nickname" = 'system'),
 (SELECT "id" FROM roles WHERE "name" = 'admin'),
 true)
;
