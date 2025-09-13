from rest_framework import serializers
from .models import MailAccount

class MailAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = MailAccount
        fields = [
            "id", "email", "destination", "imap_host", "imap_port",
            "smtp_host", "smtp_port", "use_ssl", "username",
            "is_active", "is_default", "created_at", "password"
        ]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        account = MailAccount(**validated_data)
        if password:
            account.set_password(password)
        account.save()
        return account

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
