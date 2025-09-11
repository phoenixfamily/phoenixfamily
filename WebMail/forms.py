# webmail/forms.py
from django import forms
from .models import MailAccount

class MailAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = MailAccount
        fields = ["email", "username", "password", "imap_host", "imap_port", "smtp_host", "smtp_port", "use_ssl", "is_active", "is_default"]

    def save(self, commit=True):
        account = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            account.set_password(raw_password)
        if commit:
            account.save()
        return account
