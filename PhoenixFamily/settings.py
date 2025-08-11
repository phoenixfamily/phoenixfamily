import os
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-at+z71p&8n4sf$r_5=ux5jb=ha2!h7^pp&2s470qb8&4+3^-ig'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DOMAIN = 'phoenixfamily.co'
SITE_NAME = 'PhoenixFamily'
SITE_URL = "https://phoenixfamily.co"

SITE_ID = 1

META_SITE_PROTOCOL = "https"
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_SCHEMAORG_PROPERTIES = True

CSRF_TRUSTED_ORIGINS = ["https://phoenixfamily.co", "https://www.phoenixfamily.co"]

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'phoenixfamily.co',
    'www.phoenixfamily.co'

]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # برای فورس کردن HTTPS

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',  # برای ساخت Sitemap
    'django.contrib.humanize',  # برای نمایش بهتر اعداد و تاریخ‌ها
    'rest_framework',
    'django_user_agents',  # helper package that allow to work with User/views
    'Home',
    'About',
    'Blog',
    'Contact',
    'Product',
    'User',
    'Authentication',
    'Seo',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',  # for get device info (User/Views)
    'django.middleware.gzip.GZipMiddleware',

]

ROOT_URLCONF = 'PhoenixFamily.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',  # فعال‌سازی پردازشگر i18n
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Seo.context_processors.seo_context',  # افزودن این خط

            ],
        },
    },
]

WSGI_APPLICATION = 'PhoenixFamily.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phoenixf_PhoenixFamily',  # نام دیتابیس
        'USER': 'phoenixf_db',  # نام کاربری دیتابیس
        'PASSWORD': 'Y^R+cB{MA1n%',  # رمز عبور دیتابیس
        'HOST': 'localhost',  # آدرس سرور MySQL (یا آدرس دلخواه)
        'PORT': '3306',  # پورت MySQL (پورت پیش‌فرض: 3306)
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

SEO = {
    'default': {
        'title': _('Phoenix Family | Board Games, Entertainment Apps & More!'),
        'description': _(
            'Discover Phoenix Family – your ultimate destination for family entertainment! From online entertainment to'
            ' entertainment apps and best board games for adults, fun awaits!'),
        'keywords': [
            _('phoenix family'),
            _('family entertainment'),
            _('entertainment online'),
            _('entertainment apps'),
            _('family board games'),
            _('board game online'),
            _('board game apps'),
            _('game apps'),
            _('best entertainment apps'),
            _('best board games for adults'),
        ],
        'robots': 'index, follow',  # یا 'noindex, nofollow' برای جلوگیری از ایندکس
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentication via JWT

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Token expires in 1 day
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token expires in 7 days
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian')),
    ('ar', _('Arabic')),
    ('tr', _('Turkish')),
    ('ru', _('Russian')),
    ('hi', _('Hindi')),
    ('ja', _('Japanese')),
    ('ko', _('Korean')),
    # ('zh-hans', _('Simplified Chinese')),  # چینی ماندارین ساده‌شده

]

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOCALE_PATHS = [
    BASE_DIR / 'locale',  # مسیر پوشه‌ی locale
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = '/home/phoenixf/public_html/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # اگر فایل استاتیکی دارید که در مسیر پروژه هستند.
]

MEDIA_ROOT = '/home/phoenixf/public_html/media/'
MEDIA_URL = '/media/'

ROBOTS_FILE_PATH = '/home/abbaslot/public_html/robots.txt/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.phoenixfamily.co'
EMAIL_PORT = 465  # پورت SMTP
EMAIL_USE_TLS = False  # TLS غیرفعال است
EMAIL_USE_SSL = True  # SSL فعال است
EMAIL_HOST_USER = 'customer@phoenixfamily.co'
EMAIL_HOST_PASSWORD = 'n.Y?8&eg0$60'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
COMPANY_EMAIL = 'info@phoenixfamily.co'

AUTH_USER_MODEL = 'User.User'
