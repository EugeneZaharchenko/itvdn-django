"""
URL configuration for itvdn_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from user_app.views import (
    AllUsers,
    CreateUser,
    CreateViewExample,
    CustomLoginView,
    DeleteExample,
    DetailViewExample,
    ListExample,
    UpdateExample,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", CreateUser.as_view(), name="signup"),
    path("all_users/", AllUsers.as_view(), name="all_users"),
    path("detailed_user/<pk>/", DetailViewExample.as_view(), name="detail"),
    path("accounts/", ListExample.as_view(), name="accounts"),
    path("create/", CreateViewExample.as_view(), name="create"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("delete/<pk>/", DeleteExample.as_view(), name="delete"),
    path("update/<pk>/", UpdateExample.as_view(), name="update"),
    path("shop/", include("itvdn_shop.urls")),
    path("", include("send_email.urls")),
    path("", include("reset_password.urls")),
]
if settings.DEBUG:  # Only serve media in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
