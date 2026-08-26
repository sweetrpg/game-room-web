# AGENTS.md

This file provides guidance to Claude Code, Codex, GitHub Copilot, and other coding agents
working in this repository.

## About This Project

`game-room-web` is the SweetRPG platform's Game Room frontend: a Flask backend (`src/`) serving
a Vue single-page app (`web/`). It talks to `game-room-api` (previously `shelf-api`, before that
`library-api` - see `sweetrpg/platform`'s `rename-shelf-to-game-room-service` OpenSpec change)
for domain data.

## Committing Code

[Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <description>`.

## Branches and Workflow

Git-flow (see `docs/git-flow.md` in `sweetrpg/platform`): `develop` is the integration branch,
`master` reflects the latest release. Feature/fix branches off `develop`, PR back into `develop`.

## Running Checks Locally

Backend (Flask, Python 3.14 minimum per platform convention):

```bash
pip install -r requirements/dev.txt
make coverage
make flake8
```

Frontend (Vue, under `web/`):

```bash
cd web
yarn install
yarn test:unit
```
