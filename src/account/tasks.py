from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def send_email_async(subject, message, email_from):
    recipient_list = [settings.EMAIL_HOST_USER]  # send e-mail to our own address
    send_mail(subject, message,
              email_from, recipient_list,
              fail_silently=False)
