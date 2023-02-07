# volindo-challenge

To run project run locally with Docker and docker-compose:

    docker-compose up-d
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser

Access to:

    http://localhost:8001/              # API
    http://localhost:8001/admin         # Admin


