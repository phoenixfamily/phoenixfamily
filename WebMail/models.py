from django.db import models
from cryptography.fernet import Fernet
from PhoenixFamily import settings
from User.models import User
from passlib.hash import sha512_crypt  # pip install passlib

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
    _password = models.BinaryField()  # رمزگذاری سفارشی Django
    dovecot_password = models.CharField(max_length=255, blank=True, null=True)  # hash برای Dovecot
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password: str):
        """Encrypt Django password and generate Dovecot hash"""
        self._password = fernet.encrypt(raw_password.encode())
        # Hash برای Dovecot با SHA512-CRYPT
        self.dovecot_password = sha512_crypt.hash(raw_password)

    def check_dovecot_password(self, raw_password: str) -> bool:
        """برای تست مستقیم از Django"""
        if not self.dovecot_password:
            return False
        return sha512_crypt.verify(raw_password, self.dovecot_password)

    def get_password(self) -> str:
        return fernet.decrypt(self._password).decode()

    def __str__(self):
        return self.email
