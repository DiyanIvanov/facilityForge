from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome(username, email):
    print(f"Sending email to {email}")
    print(f"Sending email to {username}")
    send_mail(
        subject='Welcome to FacilityForge!',
        message=f'Hello {username},\n\nThank you for registering at FacilityForge. We are excited to have you on board!',
        from_email=settings.COMPANY_EMAIL,
        recipient_list=[email],
    )


@shared_task
def send_reset_password_confirmation(username, email):
    send_mail(
        subject='Password Reset Confirmation',
        message=f'Hello {username},\n\nYour password has been successfully reset. If you did not request this change, please contact support immediately.',
        from_email=settings.COMPANY_EMAIL,
        recipient_list=[email],
    )
