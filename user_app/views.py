from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (TemplateView, DeleteView, CreateView, UpdateView, FormView)

from .forms import EmailAuthenticationForm, SignUpForm
from .forms import RegisterForm
from .models import User


class Index(TemplateView):
    template_name = 'index.html'


class CreateUser(FormView):
    form_class = RegisterForm
    template_name = 'signup.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        authenticate(username=user.email, password=user.password)
        login(self.request, user)
        return super(CreateUser, self).form_valid(form)


class CustomLoginView(LoginView):
    """Custom LoginView using email authentication"""

    form_class = EmailAuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')  # Change to your desired redirect URL

    def get_success_url(self):
        """Redirect to different URLs based on user type"""
        user = self.request.user

        if user.is_staff:
            return reverse_lazy('admin:index')
        else:
            # You can customize this based on your needs
            return reverse_lazy('index')  # or 'home', 'profile', etc.

    def form_valid(self, form):
        """Handle successful login"""
        user = form.get_user()

        # Add welcome message
        messages.success(
            self.request,
            f'Welcome back, {user.get_full_name() or user.get_short_name()}!'
        )

        # You can add additional login logic here
        # For example, update last login, log the event, etc.

        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle failed login attempt"""
        messages.error(
            self.request,
            'Login failed. Please check your email and password.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Add extra context to the template"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign In'
        context['page_header'] = 'Welcome Back'
        return context


class CreateViewExample(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = '/'


class UpdateExample(UpdateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = '/'


class DeleteExample(DeleteView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = '/'


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
