# AGENTS.md

This file provides guidance to Claude Code, Codex, GitHub Copilot, and other coding agents
working in this repository.

## About This Project

`game-room-web` is the SweetRPG platform's Game Room frontend: a server-rendered Flask app
(`src/`). It talks to `game-room-api` (previously `shelf-api`, before that `library-api` - see
`sweetrpg/platform`'s `rename-shelf-to-game-room-service` OpenSpec change) for domain data. An
earlier Vue single-page app under `web/` was removed - this is a server-rendered Flask frontend
now, not a Flask API behind a separate SPA.

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
