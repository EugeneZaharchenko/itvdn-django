from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address."
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional."
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional."
    )

    class Meta:
        model = User
        # ✅ Only essential fields for signup
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        """Ensure email uniqueness"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email.lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user
