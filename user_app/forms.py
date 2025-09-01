from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    fullname = forms.CharField(label="First name")

    class Meta:
        model = User
        fields = ("last_name", "fullname", "email", "password1")


class LoginForm(AuthenticationForm):
    '''Simple login form'''

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
        if user.username.startswith('b'):
            raise forms.ValidationError(
                _("Sorry, accounts starting with 'b' aren't welcome here."),
                code='no_b_users',
            )


class EmailAuthenticationForm(AuthenticationForm):
    """Custom authentication form that uses email instead of username"""

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True
        }),
        label='Email'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )

    def clean_username(self):
        """Validate that the email exists in our User model"""
        email = self.cleaned_data.get('username')
        if email:
            if not User.objects.filter(email=email).exists():
                raise ValidationError("No account found with this email address.")
        return email

    def clean(self):
        """Custom authentication logic"""
        username = self.cleaned_data.get('username')  # This is actually email
        password = self.cleaned_data.get('password')

        if username is not None and password:
            # Authenticate using email
            self.user_cache = authenticate(
                self.request,
                username=username,  # Your custom backend should handle this
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct email and password. "
                    "Note that both fields may be case-sensitive."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """Check if user is allowed to login"""
        if not user.is_active:
            raise ValidationError(
                "This account is inactive. Please contact support.",
                code='inactive',
            )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'password1', 'password2')
