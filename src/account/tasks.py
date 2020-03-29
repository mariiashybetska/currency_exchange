from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

@shared_task
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def send_email_async(subject, message, email_from, recipient_list):

    send_mail(subject, message,
              email_from, recipient_list,
              fail_silently=False)


@shared_task
def send_activation_code_async(email_to, code):
    path = reverse('account:activate', arg=(code, ))
    send_mail(
        'Your activation code',
        f'http://127.0.0.1:8000{path}',
        'mshybetskaya@gmail.com',
        [email_to],
        fail_silently=False,
    )


@shared_task
def send_sms_code(phone, code):
    print(phone, code)