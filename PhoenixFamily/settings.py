import os
from email.policy import default
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

EMAIL_ENCRYPTION_KEY = config("EMAIL_ENCRYPTION_KEY", default="XWl0L1UyZ1R0UzNvaXZBbEpLbFZ2dExXcll0TXc1c1A=")


SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DOMAIN = 'phoenixfamily.ir'
SITE_NAME = 'PhoenixFamily'
SITE_URL = "https://phoenixfamily.ir"

SITE_ID = 1

META_SITE_PROTOCOL = "https"
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_SCHEMAORG_PROPERTIES = True

CSRF_TRUSTED_ORIGINS = ["https://phoenixfamily.ir", "https://www.phoenixfamily.ir"]

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'phoenixfamily.ir',
    'www.phoenixfamily.ir'

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
    'WebMail',

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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]
}


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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
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

# فایل‌های استاتیک (CSS, JS, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # فولدر نهایی برای nginx
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# فایل‌های رسانه‌ای که کاربر آپلود می‌کنه
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "User.User"
