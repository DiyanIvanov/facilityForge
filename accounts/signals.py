from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from facilityForge import settings

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject = 'Welcome to FacilityForge!',
            message = f'Hello {instance.username},\n\nThank you for registering at FacilityForge. We are excited to have you on board!',
            from_email = settings.COMPANY_EMAIL,
            recipient_list = [instance.email],
        )

@receiver(post_save, sender=UserModel)
def change_user_password(sender, instance, created, **kwargs):
    if created:
        instance.set_password(instance.password)
        instance.save()
        # Optionally, you can log this action or notify the user
        print(f"Password for {instance.username} has been set to a default value.")
        send_mail(
            subject = 'Your Password Has Been Set',
            message = f'Hello {instance.username},\n\nYour password has been set to a default value. Please log in and change it as soon as possible.',
            from_email = settings.COMPANY_EMAIL,
            recipient_list = [instance.email],
        )