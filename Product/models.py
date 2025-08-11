from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    logo = models.FileField(upload_to='images/', null=True)
    image = models.FileField(upload_to='images/', null=True)
    video = models.FileField(upload_to='videos/', null=True)
    address = models.URLField(verbose_name="ادرس", blank=True, null=True)
    header = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)


class Features(models.Model):
    icon = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE, null=True, blank=True)





