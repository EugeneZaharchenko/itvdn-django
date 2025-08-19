from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# 1️⃣ Автоматично створюємо профіль після створення користувача
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"✅ Profile created for user {instance.username}")

# 2️⃣ Логування перед оновленням профілю
@receiver(pre_save, sender=Profile)
def log_profile_update(sender, instance, **kwargs):
    if instance.pk:  # Якщо профіль вже існує
        old_profile = Profile.objects.get(pk=instance.pk)
        if old_profile.bio != instance.bio or old_profile.photo != instance.photo:
            print(f"✏️ Profile of {instance.user.username} will be updated")
