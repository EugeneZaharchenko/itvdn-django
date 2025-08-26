from django.contrib.auth import authenticate, login
from django.views.generic import FormView, TemplateView

from .forms import RegisterForm
from .models import User


class Index(TemplateView):
    template_name = 'index.html'


class CreatUser(FormView):
    form_class = RegisterForm
    template_name = 'signup.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        authenticate(username=user.email, password=user.password)
        login(self.request, user)
        return super(CreatUser, self).form_valid(form)


class AllUsers(TemplateView):
    template_name = "all_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        users = User.objects.all()

        # Create normalized user data
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'email': user.email,  # Your User model uses email, not username
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar': user.avatar,  # Direct field in your User model
                'date_joined': user.date_joined,
                'is_active': user.is_active,
            })

        context['users'] = users_data
        return context
