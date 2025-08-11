from django import forms
from .models import Contact  # مدل Contact که قبلاً تعریف کرده‌اید


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message', 'file']
