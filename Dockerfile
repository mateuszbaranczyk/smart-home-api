FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/app/home_api"

RUN chmod +x /app/start.sh
ENTRYPOINT ["/app/start.sh"]