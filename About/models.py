from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class FAQ(models.Model):
    icon = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class AboutUs(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    # شماره تلفن (اعتبارسنجی شماره تلفن)
    phone_regex = RegexValidator(
        regex=r'^\+?(\d[\d().\s-]*)?\d{9,15}$',
        message="Phone number must be entered in a valid international format. Examples: '+1234567890', "
                "'+1 (234) 567-8901', or '+44-20-1234-5678'."
    )
    number = models.CharField(unique=True, validators=[phone_regex], max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(verbose_name="linkedin", blank=True, null=True)
    instagram = models.URLField(verbose_name="instagram", blank=True, null=True)
    whatsApp = models.URLField(verbose_name="whatsApp", blank=True, null=True)
    telegram = models.URLField(verbose_name="telegram", blank=True, null=True)
    logo = models.FileField(upload_to='images/', null=True)
    image = models.FileField(upload_to='images/', null=True)
    video = models.FileField(upload_to='videos/', null=True)
    alt = models.CharField(max_length=255, null=True, blank=True)
    context = models.TextField(blank=True, null=True)


