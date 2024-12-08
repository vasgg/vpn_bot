FROM python:3.12-alpine AS base

WORKDIR /app
COPY . .
RUN --mount=from=ghcr.io/astral-sh/uv:0.5.1,source=/uv,target=/bin/uv uv pip install --system -Ue .

FROM base AS bot_image
RUN chmod +x /app/run.sh
CMD ["/app/run.sh"]

FROM base AS task_image
RUN crontab ./src/cron_remainder/crontab
CMD ["crond", "-f"]