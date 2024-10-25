#! /usr/bin/env bash
set -e

alembic upgrade head
echo 'upgraded'
bot-run
