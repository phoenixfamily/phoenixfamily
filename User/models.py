import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, number, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)

        return self.create_user(number, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_temporary = models.BooleanField(default=True)  # مشخص می‌کند کاربر موقت است یا نه

    # نام
    first_name = models.CharField(max_length=50, blank=True, null=True)
    # نام خانوادگی
    last_name = models.CharField(max_length=50, blank=True, null=True)

    username = models.CharField(max_length=50, unique=True, blank=True, null=True)  # New username field

    # ایمیل
    email = models.EmailField(unique=True, null=True, blank=True)

    # شماره تلفن (اعتبارسنجی شماره تلفن)
    phone_regex = RegexValidator(
        regex=r'^\+?(\d[\d().\s-]*)?\d{9,15}$',
        message="Phone number must be entered in a valid international format. Examples: '+1234567890', "
                "'+1 (234) 567-8901', or '+44-20-1234-5678'."
    )
    number = models.CharField(unique=True, validators=[phone_regex], max_length=15, blank=True, null=True)

    # تاریخ تولد
    birth_date = models.DateField(blank=True, null=True)

    # تصویر پروفایل
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # جنسیت
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    is_staff = models.BooleanField(default=False, verbose_name="مدیر")
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')

    # **New field for email verification**
    is_verified = models.BooleanField(default=False)

    # زمان ایجاد و به‌روزرسانی
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'number', 'birth_date', 'gender']

    objects = CustomAccountManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def assign_username(self):
        """Assigns username after email verification."""
        if not self.username:
            self.username = self.email.split('@')[0]

    def save(self, *args, **kwargs):
        if self.is_verified and not self.username:
            self.assign_username()
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
