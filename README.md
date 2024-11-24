# Smart Home API
This is an API for managing smart home devices designed to work with Garmin and the app [HttpClient](https://apps.garmin.com/apps/da241207-e929-4cdf-9662-11ab17ffd70d).

## Development
Prepare the environment by installing Poetry, then run `poetry install` and `poetry shell`. Change the directory to `/home_api`. To start Django, run `python3 manage.py runserver`.

## Tests
Run tes in `home_api` directory.
```bash
pytest
# for coverage
pytest --cov
```

## Deployment
Create a `.env` file in the root directory as follows:
```
SECRET_KEY=unsafe
CSRF_ORIGIN=http://localhost:8000
```
Before you build the Docker image, run:
```bash
python3 manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate
```
and then `docker compose up -d`.

Some Garmin models require an HTTPS connection. In this case, I am using a Cloudflare tunnel with forced HTTPS connection.
![Diagram](gl.drawio.png)
