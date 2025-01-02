install:
	pip install -r requirements.txt --no-cache-dir

django-prepare: ./home_api/manage.py
	makemigrations
	migrate
	collectstatic --noinput

django-dev: ./home_api/manage.py
	python home_api/manage.py runserver 8001
	
docker: django-prepare
	docker-compose up -d --build