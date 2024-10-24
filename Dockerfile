FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -Ue .
RUN chmod +x /app/run.sh
CMD ["bash", "-c", "/app/run.sh"]
