# Smart Home API
This is an API for managing smart home devices designed to work with Garmin and the app [HttpClient](https://apps.garmin.com/apps/da241207-e929-4cdf-9662-11ab17ffd70d).

For more information go to [wiki](https://github.com/mateuszbaranczyk/smart-home-api/wiki)

## Development
Prepare the environment by installing Poetry, then run `poetry install` and `poetry shell`. Change the directory to `/home_api`. To start Django, run `python3 manage.py runserver`.

## Tests
Run tests in `home_api` directory.
```bash
pytest
# for coverage
pytest --cov
```

## Deployment

Create `docker-compose.yaml` as follows and adjust volume path and env variables.
```yaml
services:
  backend:
    container_name: garlight
    build: .
    environment:
      PORT: 8000
      CSRF_ORIGIN: http://localhost:${PORT}
      SECRET_KEY: T0pS3cReT
      WEATHER_API_KEY: 112mn12sda3mfd
      DEVELOPER: "False"
      DJANGO_SUPERUSER_EMAIL: admin@example.com
      DJANGO_SUPERUSER_USERNAME: admin
      DJANGO_SUPERUSER_PASSWORD: admin
    network_mode: host
    volumes:
      - /code/smart-home-api/database:/app/home_api/database

```

Run docker by:
```bash
docker compose up -d
```

Some Garmin models require an HTTPS connection. In this case, I am using a Cloudflare tunnel with forced HTTPS connection.
![Diagram](gl.drawio.png)
