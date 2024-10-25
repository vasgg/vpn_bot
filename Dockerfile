FROM python:3.12-slim

RUN pip install uv
COPY requirements.txt /app/requirements.txt
RUN uv pip install --system -r /app/requirements.txt

WORKDIR /app
COPY . /app

RUN uv pip install --system -Ue .
RUN chmod +x /app/run.sh
CMD ["bash", "-c", "/app/run.sh"]
