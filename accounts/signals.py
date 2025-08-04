from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.tasks import send_welcome

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_welcome.delay(instance.username, instance.email)
