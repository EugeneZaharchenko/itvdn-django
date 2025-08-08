docker build -t django-study-project .

### Db local management
docker pull postgres:15
docker volume create django_data
docker run -d \
  --name django_postgres \
  -e POSTGRES_DB= \
  -e POSTGRES_USER= \
  -e POSTGRES_PASSWORD= \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15

docker run -p 8000:8000 django-study-project

### Install project dependencies
uv sync --group dev \
uv run python manage.py runserver

### Docker compose start
1. Stop db container
2. docker compose up
