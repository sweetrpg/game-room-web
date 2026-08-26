# Contributing

Thanks for considering a contribution to `game-room-web`.

## Branching

This repo follows the sweetrpg platform's git-flow convention:

* `develop` is the integration branch. All feature and fix branches merge here.
* `master` reflects the latest released state. Nothing is committed here directly.
* Branch names: `feature/<description>` for new functionality, `fix/<description>` for bug
  fixes, `hotfix/<description>` for urgent fixes to a released version.

```bash
git checkout develop
git pull
git checkout -b feature/my-change
# ... work, commit ...
git push -u origin feature/my-change
# open a PR: feature/my-change -> develop
```

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>
```

## Running checks locally

Backend (Flask, Python 3.14, managed via [uv](https://docs.astral.sh/uv/) - do not use
`pip`/`tox` directly):

```bash
uv sync --group test   # create .venv and install deps
uv run pytest          # run tests
uv lock --upgrade      # update dependencies
```

Frontend (Vue, under `web/`):

```bash
cd web
yarn install
yarn test:unit
```

## Pull requests

CI runs automatically on PRs targeting `develop`. Once checks pass and the PR is reviewed, it
can be merged (auto-merge is enabled once required checks pass).

## Releases

Versions are tagged from `develop`. See `CHANGELOG.md` for release history.
