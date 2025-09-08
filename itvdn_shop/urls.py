from django.urls import path
from . import views
from itvdn_shop.views import Index, Report, DateDetailViewExample, \
    WeekArchiveViewExample

# Define the app name for namespacing
app_name = 'itvdn_shop'

urlpatterns = [
    path('', Index.as_view(), name='report'),
    path('report/', Report.as_view(), name='report'),
    path('detail-date/<year>/<month>/<day>/<pk>',
         DateDetailViewExample.as_view(), name='detail_date'),
    path('week-archive/<week>/', WeekArchiveViewExample.as_view(), name='week_archive'),
]
