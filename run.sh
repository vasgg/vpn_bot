#! /usr/bin/env bash
set -e

alembic upgrade head
bot-run
