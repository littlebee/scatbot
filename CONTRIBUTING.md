## Setup

1. install [poetry](https://python-poetry.org/docs/)
2. run `poetry install`

Should be all that this needed to bootstrap a development setup

## Running tests

Run automatically by Github action CI/CD

`poetry run pytest`

## Running lint

Run automatically by commit-hook and CI/CD.

`poetry run flake8`

## Running formatters

Run automatically by commit-hook and CI/CD.

`poetry run black`
