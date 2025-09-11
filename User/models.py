import uuid
import random
import string

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email=None, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        return self.create_user(email=email, password=password, **other_fields)

    def create_user(self, email=None, password=None, **other_fields):
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_temporary = models.BooleanField(default=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    # یوزرنیم اجباری و یونیک
    username = models.CharField(max_length=10, unique=True, blank=True, null=True)

    email = models.EmailField(unique=True, null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?(\d[\d().\s-]*)?\d{9,15}$',
        message="Phone number must be entered in a valid format."
    )
    number = models.CharField(unique=True, validators=[phone_regex], max_length=15, blank=True, null=True)

    birth_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    is_staff = models.BooleanField(default=False, verbose_name="مدیر")
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomAccountManager()

    def __str__(self):
        return self.username or f"User-{self.id}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def generate_username(self, length=10):
        """Generates a random unique username (letters+digits, length=10)."""
        chars = string.ascii_lowercase + string.digits
        while True:
            random_username = ''.join(random.choices(chars, k=length))
            if not User.objects.filter(username=random_username).exists():
                return random_username

    def save(self, *args, **kwargs):
        if not self.username:  # فقط اگر یوزرنیم خالی بود
            self.username = self.generate_username()
        super().save(*args, **kwargs)


class UserDeviceInfo(models.Model):
    # نوع دستگاه (موبایل، تبلت، دسکتاپ)
    DEVICE_TYPES = [
        ('Mobile', 'Mobile'),
        ('Tablet', 'Tablet'),
        ('Desktop', 'Desktop'),
        ('Unknown', 'Unknown'),
    ]
    # مدل دستگاه (مثلاً iPhone 13 Pro)
    device_model = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, default='Unknown')

    # سیستم‌عامل و نسخه (مثلاً Android 12)
    operating_system = models.CharField(max_length=50, blank=True, null=True)
    os_version = models.CharField(max_length=50, blank=True, null=True)

    # مرورگر و نسخه (مثلاً Chrome 119)
    browser = models.CharField(max_length=50, blank=True, null=True)
    browser_version = models.CharField(max_length=50, blank=True, null=True)

    # آدرس IP کاربر
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    # منطقه جغرافیایی (کشور و شهر)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    # زمان ایجاد (برای ردیابی زمان)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_device_info')

    def __str__(self):
        return f"{self.device_type} - {self.device_model or 'Unknown'}"

    class Meta:
        verbose_name = "User Device Info"
        verbose_name_plural = "User Device Infos"


class UserActivityLog(models.Model):
    # اطلاعات کاربر (اگر کاربر احراز هویت شده باشد)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_activity_log')

    # صفحه بازدید شده
    visited_page = models.URLField()

    # زمان ورود به صفحه
    entry_time = models.DateTimeField(default=now)

    # زمان خروج از صفحه
    exit_time = models.DateTimeField(null=True, blank=True)

    # لینک‌های کلیک‌شده در صفحه
    clicked_links = models.TextField(null=True, blank=True)

    # کلیدواژه‌های جستجو شده
    search_keywords = models.TextField(null=True, blank=True)

    # محصولات یا خدمات مشاهده‌شده
    viewed_items = models.TextField(null=True, blank=True)

    # خطاهای رخ‌داده
    error_messages = models.TextField(null=True, blank=True)

    # زمان ایجاد و به‌روزرسانی
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def duration_on_page(self):
        """محاسبه مدت زمان حضور در صفحه"""
        if self.exit_time:
            return (self.exit_time - self.entry_time).total_seconds()
        return None

    def __str__(self):
        return f"Activity by {self.user or 'Anonymous'} on {self.visited_page}"

    class Meta:
        verbose_name = "User Activity Log"
        verbose_name_plural = "User Activity Logs"
