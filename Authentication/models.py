import random
import hashlib
from datetime import timedelta
from django.utils.timezone import now
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OTPVerification(models.Model):
    """Model for tracking OTP each user requests."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp_verification")

    otp_hash = models.CharField(max_length=128)  # Store hashed OTP
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    attempts = models.IntegerField(default=0)  # Track failed attempts

    def save(self, *args, **kwargs):
        """Generate OTP and hash it before saving"""
        if not self.otp_hash:
            otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
            self.otp_hash = hashlib.sha256(otp.encode()).hexdigest()  # Store hash for security
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=5)  # OTP expires in 5 minutes
        super().save(*args, **kwargs)

    def is_valid(self, otp):
        """Check if the OTP is correct and not expired"""
        if now() > self.expires_at:
            return False, "OTP expired"

        if self.attempts >= 3:  # Limit OTP entry attempts
            return False, "Maximum OTP attempts exceeded"

        if self.otp_hash == hashlib.sha256(otp.encode()).hexdigest():
            return True, "OTP verified"
        else:
            self.attempts += 1  # Increment failed attempts
            self.save(update_fields=["attempts"])
            return False, "Invalid OTP"

    def __str__(self):
        return f"OTP for {self.user.email} (expires: {self.expires_at})"
