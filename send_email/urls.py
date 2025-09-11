from django.contrib.auth import views as auth
from django.shortcuts import redirect
from django.urls import path

from .views import ImageEmailTemplateView, SimpleEmailTemplateView, activate_account, usersignup, subscription
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/email-signup/', permanent=False), name='home'),
    path("simple-email/", SimpleEmailTemplateView.as_view(), name="email-test"),
    path("image-email/", ImageEmailTemplateView.as_view(), name="image-email"),
    path("logout/", auth.LogoutView.as_view(template_name="index.html"), name="logout"),
    path("email-signup/", usersignup, name="email-signup"),
    path(r"activate/<uidb64>/<token>/", activate_account, name="activate"),
    path("subscription/", subscription, name="subscription"),
]
