import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# مسیر Root Directory پروژه را به sys.path اضافه می‌کند تا Django تنظیمات را پیدا کند.
# اگر فایل wsgi.py در config/wsgi.py باشد، این خط یک پله به بالا (پوشه اصلی django) می‌رود.
# اگر ریشه پروژه شما پوشه config است، این کد صحیح است.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()