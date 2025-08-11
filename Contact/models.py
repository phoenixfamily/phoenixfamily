from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)  # فیلد فایل اختیاری
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
