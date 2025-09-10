from django.contrib.auth import views as auth
from django.urls import path

from .views import ImageEmailTemplateView, SimpleEmailTemplateView, activate_account, usersignup

urlpatterns = [
    path("simple-email/", SimpleEmailTemplateView.as_view(), name="email-test"),
    path("image-email/", ImageEmailTemplateView.as_view(), name="image-email"),
    path("logout/", auth.LogoutView.as_view(template_name="index.html"), name="logout"),
    path(r"signup/", usersignup, name="register_user"),
    path(r"activate/<uidb64>/<token>/", activate_account, name="activate"),
    # path("subscription/", subscription, name="subscription"),
]
