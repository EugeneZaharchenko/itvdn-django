from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=150)
    photo = models.ImageField(upload_to='profile_pics')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
