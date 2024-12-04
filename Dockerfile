FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN --mount=from=ghcr.io/astral-sh/uv:0.5.1,source=/uv,target=/bin/uv uv pip install --system -Ue .
RUN chmod +x /app/run.sh
CMD ["bash", "-c", "/app/run.sh"]
