FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

WORKDIR /app/home_api
ENV PYTHONPATH="."
CMD ["gunicorn", "home_api.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]