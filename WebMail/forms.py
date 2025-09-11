from django import forms
from .models import MailAccount

class MailAccountForm(forms.ModelForm):
    class Meta:
        model = MailAccount
        fields = ["email", "username", "password", "imap_host", "imap_port", "smtp_host", "smtp_port", "is_active", "is_default"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }