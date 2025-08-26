from django.urls import include, path
from rest_framework import routers

from .views import CarViewSet, MakeViewSet, ModelViewSet

app_name = 'rest_api'

router = routers.DefaultRouter()
router.register(r'make', MakeViewSet, basename='make')
router.register(r'model', ModelViewSet, basename='model')
router.register(r'car', CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
