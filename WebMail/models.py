from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from PhoenixFamily import settings

fernet = Fernet(settings.EMAIL_ENCRYPTION_KEY)

class MailAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='mail_accounts')
    email = models.EmailField(unique=True)
    imap_host = models.CharField(max_length=255, default="imap.yourdomain.com")
    imap_port = models.PositiveIntegerField(default=993)
    smtp_host = models.CharField(max_length=255, default="smtp.yourdomain.com")
    smtp_port = models.PositiveIntegerField(default=587)
    use_ssl = models.BooleanField(default=True)
    username = models.CharField(max_length=255)
    _password = models.BinaryField()  # پسورد رو به صورت باینری ذخیره می‌کنیم (encrypted)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)  # <- اینو اضافه کن
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password: str):
        """Encrypt password before saving"""
        self._password = fernet.encrypt(raw_password.encode())

    def get_password(self) -> str:
        """Decrypt password when needed"""
        return fernet.decrypt(self._password).decode()

    def __str__(self):
        return self.email
