import os
from pathlib import Path
from dotenv import load_dotenv # برای خواندن فایل .env
import dj_database_url # برای خواندن URL دیتابیس

# بارگذاری متغیرها در محیط لوکال
load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent

# --- تنظیمات امنیتی ---
# خواندن از متغیر محیطی یا استفاده از مقدار .env
SECRET_KEY = os.environ.get('SECRET_KEY')

# خواندن DEBUG و ALLOWED_HOSTS
DEBUG = os.environ.get('DEBUG_VALUE', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')


# --- نصب و راه‌اندازی اپلیکیشن‌ها ---
INSTALLED_APPS = [
    # WhiteNoise باید اولین باشد
    'whitenoise.runserver_nostatic', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # اپلیکیشن‌های من
    'dashboard', 
]

# ... سایر تنظیمات (MIDDLEWARE و TEMPLATES و WSGI بدون تغییر) ...

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # اضافه کردن WhiteNoise برای مدیریت فایل‌های استاتیک
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- تنظیمات TEMPLATES (ضروری) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # به جنگو می‌گوید که پوشه templates را در ریشه پروژه پیدا کند.
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ...

# --- تنظیمات دیتابیس ---
if DEBUG:
    # در محیط لوکال از SQLite استفاده می‌کنیم
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # در محیط Production از URL دیتابیس سرور استفاده می‌کنیم (PostgreSQL)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }

# ... سایر تنظیمات (AUTH_PASSWORD_VALIDATORS و LANGUAGE و TIME_ZONE بدون تغییر) ...

ROOT_URLCONF = 'config.urls'
# --- تنظیمات فایل‌های استاتیک و مدیا ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# تنظیمات WhiteNoise
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# تنظیمات مدیا (فایل‌های آپلود شده توسط کاربر)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
