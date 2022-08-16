from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings
from django.core.mail import send_mail


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            profile2user=user,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
        # subject = "Welcome to ePica"
        # message = "We are glad you are here!"
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [profile.email],
        #     fail_silently=False,
        # )


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.profile2user
    if not created:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.email = profile.email
        user.save()


def delete_user(sender, instance, **kwargs):
    user = instance.profile2user
    user.delete()


post_save.connect(create_profile, sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender=Profile)
