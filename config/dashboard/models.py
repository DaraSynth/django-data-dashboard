from django.db import models

class DataFile(models.Model):
    # عنوانی برای فایل (اختیاری)
    title = models.CharField(max_length=100, blank=True)
    
    # فیلد اصلی که فایل را ذخیره می‌کند
    file = models.FileField(upload_to='data_files/')
    
    # زمان آپلود شدن فایل
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"File {self.id}"