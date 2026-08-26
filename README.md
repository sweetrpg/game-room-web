# Game Room Web

[![Unit tests](https://github.com/sweetrpg/game-room-web/actions/workflows/python-ci.yml/badge.svg)](https://github.com/sweetrpg/game-room-web/actions/workflows/python-ci.yml)
[![Coverage](https://github.com/sweetrpg/game-room-web/blob/develop/coverage.svg)](https://github.com/sweetrpg/game-room-web)
[![License](https://img.shields.io/github/license/sweetrpg/game-room-web.svg)](https://img.shields.io/github/license/sweetrpg/game-room-web.svg)
[![Issues](https://img.shields.io/github/issues/sweetrpg/game-room-web.svg)](https://img.shields.io/github/issues/sweetrpg/game-room-web.svg)
[![PRs](https://img.shields.io/github/issues-pr/sweetrpg/game-room-web.svg)](https://img.shields.io/github/issues-pr/sweetrpg/game-room-web.svg)
[![Dependabot](https://badgen.net/github/dependabot/sweetrpg/game-room-web)](https://badgen.net/github/dependabot/sweetrpg/game-room-web)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![Built with love](https://ForTheBadge.com/images/badges/built-with-love.svg)](https://ForTheBadge.com/images/badges/built-with-love.svg)

Flask backend (`src/`) plus a Vue frontend (`web/`) for the SweetRPG Game Room domain -
the party's shared table state (sessions, rosters, and related game-room concerns). See
`AGENTS.md` for backend dependencies and conventions.

## Run locally

Backend (Python 3.14, managed via [uv](https://docs.astral.sh/uv/)):

```bash
uv sync --group test
uv run python src/appserver.py
```

Frontend:

```bash
cd web
yarn install
yarn dev
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and this repo's `AGENTS.md`
for architecture and conventions.

## Documentation

Documentation for this package can be found [here](https://sweetrpg.github.io/game-room-web).
