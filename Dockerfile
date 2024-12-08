FROM python:3.12-alpine as base

WORKDIR /app
COPY . .
RUN --mount=from=ghcr.io/astral-sh/uv:0.5.1,source=/uv,target=/bin/uv uv pip install --system -Ue .

FROM base as bot_image
RUN chmod +x /app/run.sh
CMD ["/app/run.sh"]

FROM base as task_image
RUN crontab crontab
CMD ["crond", "-f"]