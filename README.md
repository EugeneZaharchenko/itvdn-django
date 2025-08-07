docker build -t django-study-project .

docker run -p 8000:8000 django-study-project

uv sync
uv run python manage.py runserver

### Docker compose start
1. Stop db container
2. docker compose up
