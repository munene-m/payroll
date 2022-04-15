import email
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Employee

@receiver(post_save, sender=User)
def post_save_create_user(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance, email=instance.email )