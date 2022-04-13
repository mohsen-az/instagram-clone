build:
	docker-compose up --build -d --remove-orphans

up:
	docker-compose up -d

down:
	docker-compose down

show-logs:
	docker-compose logs

migrate:
	docker-compose exec instagram python manage.py migrate

makemigrations:
	docker-compose exec instagram python manage.py makemigrations

superuser:
	docker-compose exec instagram python manage.py createsuperuser

collectstatic:
	docker-compose exec instagram python manage.py collectstatic --no-input --clear

down-v:
	docker-compose down -v

run-test:
	docker-compose exec instagram python manage.py test
