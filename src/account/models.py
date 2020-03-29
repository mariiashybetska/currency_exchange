from django.db import models
from django.contrib.auth.models import AbstractUser

from uuid import uuid4
from datetime import datetime
import random

from account.tasks import send_activation_code_async, send_sms_code


def avatar_path(instance, filename: str) -> str:
    ext = filename.split('.')[-1]
    f = str(uuid4())
    filename = f'{f}.{ext}'
    return '/'.join(['avatar', str(instance.id), filename])


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path,
                               null=True, blank=True,
                               default=None)

    phone = models.CharField(max_length=20,
                             null=True, blank=True)


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=256)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes')
    created = models.DateTimeField(auto_now_add=True)
    code = models.UUIDField(default=uuid4, editable=False, unique=True)
    is_activated = models.BooleanField(default=False)
    timeout = models.DateTimeField

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    def send_activation_code(self):
        send_activation_code_async.delay(self.user.email, self.code)

    # def save(self, *args, **kwargs):
    #     self.code = ...
    #     super.save(*args, **kwargs)


def gen_smsode():
    return random.randint(1000, 32000)


class SMScode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_codes')
    created = models.DateTimeField(auto_now_add=True)
    code = models.PositiveSmallIntegerField(default=gen_smsode)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    def send_sms_code(self):
        send_sms_code.delay(self.user.phone, self.code)
