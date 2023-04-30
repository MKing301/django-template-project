from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
from django.contrib import messages
from django.db.models.signals import post_save #Import a post_save signal when a user is created
from django.contrib.auth.models import User # Import the built-in User model, which is a sender
from django.dispatch import receiver # Import the receiver
from .models import Profile


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    messages.success(request, "You have successfully logged out!")


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
