# AGENTS.md

This file provides guidance to Claude Code, Codex, GitHub Copilot, and other coding agents
working in this repository.

## About This Project

`game-room-web` is the SweetRPG platform's Game Room frontend: a server-rendered Flask app
(`src/`). It talks to `game-room-api` (previously `shelf-api`, before that `library-api` - see
`sweetrpg/platform`'s `rename-shelf-to-game-room-service` OpenSpec change) for domain data. An
earlier Vue single-page app under `web/` was removed - this is a server-rendered Flask frontend
now, not a Flask API behind a separate SPA.

## Localization

User-facing strings come from `src/translations/<code>/LC_MESSAGES/messages.po` via Flask-Babel,
never hardcoded in templates (`{{ _('...') }}` in Jinja, `_('...')` in view/blueprint code).
Lives under `src/` (not the repo root) so the Dockerfile's `COPY src /app` actually ships it -
the app's `root_path` can't be trusted to find a repo-root `translations/` directory (see
`application/i18n.py`'s `TRANSLATIONS_DIR`, resolved from `__file__`). English is the
default/fallback locale; add a new locale by creating a new catalog under `src/translations/<code>/`
(compile with `pybabel compile`) and adding its code to `SUPPORTED_LOCALES` in
`application/i18n.py`. Locale resolution per request: `locale` query parameter, then `locale`
cookie override, then `Accept-Language`, then English. Catalog msgids are the English source
strings (the `en` catalog's `msgstr` repeats the `msgid`); strings with `%(...)s` interpolation
are kept verbatim, and both the `.po` and its compiled `.mo` are committed. CI runs
`scripts/check-template-strings.sh` (`locale-lint` job), which fails on literal text between
HTML tags that isn't a whitelisted brand string or wrapped in a gettext call - see the
`web-frontend-localization` spec in `sweetrpg/platform` (`openspec/specs/web-frontend-localization/spec.md`).

## Committing Code

[Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <description>`.

## Branches and Workflow

Git-flow (see `docs/git-flow.md` in `sweetrpg/platform`): `develop` is the integration branch,
`master` reflects the latest release. Feature/fix branches off `develop`, PR back into `develop`.

## Running Checks Locally

Python 3.14, managed via [uv](https://docs.astral.sh/uv/), which is the required Python tool
on this platform (`pyproject.toml` + committed `uv.lock`; do not use `pip`/`tox` directly).

```bash
uv sync --group test   # create .venv and install deps
uv run pytest          # run tests
uv lock --upgrade      # update dependencies
```
