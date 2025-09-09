from django.urls import path

# from .views import usersignup, activate_account, subscription
from .views import ImageEmailTemplateView, SimpleEmailTemplateView

urlpatterns = [
    path("simple-email/", SimpleEmailTemplateView.as_view(), name="email-test"),
    path("image-email/", ImageEmailTemplateView.as_view(), name="image-email"),
    # path('logout/', auth.LogoutView.as_view(template_name='index.html'),
    #      name='logout'),
    # path(r'signup/', usersignup, name='register_user'),
    # path(
    #     r'activate/<uidb64>/<token>/',
    #     activate_account, name='activate'),
    # path("subscription/", subscription, name="subscription"),
]
