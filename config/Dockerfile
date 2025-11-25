
FROM python:3.11-slim

# نصب پکیج های سیستمی مورد نیاز برای psycopg2 و Pillow
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev

# تنظیم پوشه کاری
WORKDIR /usr/src/app

# کپی کردن requirements.txt و نصب پکیج های پایتون
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن بقیه فایل های پروژه
COPY . .

# دستور اجرا
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:$PORT"]

