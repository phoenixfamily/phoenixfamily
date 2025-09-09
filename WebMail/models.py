from django.db import models
from django.contrib.auth.models import User

class EmailAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    imap_host = models.CharField(max_length=255, default="imap.yourdomain.com")
    imap_port = models.PositiveIntegerField(default=993)
    smtp_host = models.CharField(max_length=255, default="smtp.yourdomain.com")
    smtp_port = models.PositiveIntegerField(default=587)
    use_ssl = models.BooleanField(default=True)

    def __str__(self):
        return self.email
