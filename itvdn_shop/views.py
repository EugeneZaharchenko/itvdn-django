import random
import requests

from django.views.generic import (TemplateView, ListView, DetailView, DateDetailView,
                                  WeekArchiveView, DeleteView, CreateView, UpdateView, FormView)
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

response = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")
words = response.text.strip().split('\n')


class Index(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        return {'some_data': [random.choice(words)
                              for i in range(10)]}


class Report(TemplateView):
    template_name = 'main/report.html'


class ListExample(ListView):
    print('Some users')
    # template_name = 'accounts/profile.html'
    # queryset = User.objects.all()
    # context_object_name = "users"


class DetailViewExample(DetailView):
    template_name = 'detail.html'
    model = User


class DateDetailViewExample(DateDetailView):
    template_name = 'date_detail.html'
    model = User
    date_field = "date_joined"


# Example http://127.0.0.1:8000/detail-date/2020/feb/24/2


class WeekArchiveViewExample(WeekArchiveView):
    template_name = 'week_archive.html'
    year = 2020
    model = User
    date_field = "date_joined"
    context_object_name = "week_users_archive"
#     http://127.0.0.1:8000/detail-date/2020/feb/24/2
