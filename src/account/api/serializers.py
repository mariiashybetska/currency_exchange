from django.conf import settings

from rest_framework import serializers

from account.models import Contact
from account.tasks import send_email_async


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'created',
            'email',
            'title',
            'body',
        )

    def create(self, validated_data):
        send_email_async.delay(
            validated_data['title'],
            validated_data['body'],
            settings.EMAIL_HOST_USER,
            [validated_data['email'], ]
        )
        return super().create(validated_data)


