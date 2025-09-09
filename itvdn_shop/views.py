import random

import requests
from django.contrib.auth import get_user_model
from django.views.generic import (
    DateDetailView,
    TemplateView,
    WeekArchiveView,
)

response = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")
words = response.text.strip().split("\n")

User = get_user_model()


class Index(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        return {"some_data": [random.choice(words) for i in range(10)]}


class Report(TemplateView):
    template_name = "main/report.html"


class DateDetailViewExample(DateDetailView):
    template_name = "date_detail.html"
    model = User
    date_field = "date_joined"


# Example http://127.0.0.1:8000/detail-date/2020/feb/24/2


class WeekArchiveViewExample(WeekArchiveView):
    template_name = "week_archive.html"
    year = 2020
    model = User
    date_field = "date_joined"
    context_object_name = "week_users_archive"

#     http://127.0.0.1:8000/week-archive/08/
