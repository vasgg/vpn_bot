#! /usr/bin/env sh
set -e

alembic upgrade head
echo 'upgraded'
bot-run
