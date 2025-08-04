from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings



@shared_task
def send_ticket_notification(ticket_id, username, user_email, ticket_title):
    send_mail(
        subject='Welcome to FacilityForge!',
        message=f'Hello {username},\n\n Your ticket "{ticket_title}" with ID {ticket_id} has been successfully created. We will get back to you shortly.',
        from_email=settings.COMPANY_EMAIL,
        recipient_list=[user_email],
    )


