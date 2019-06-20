from rest_framework import serializers
from mail.models import Mail

class MailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mail
        fields = '__all__'
        read_only = ('is_read', 'created_at',)
