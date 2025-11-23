from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import DataFile
from .forms import DataFileForm
import pandas as pd
import json

# تابع کمکی: منطق اصلی تحلیل داده
def analyze_data(file_obj, col_x=None, col_y=None):
    """
    تحلیل داده‌های یک فایل خاص با ستون‌های مشخص.
    """
    df = pd.read_csv(file_obj.file.path)
    
    # آماده‌سازی لیست ستون‌ها برای دراپ‌داون‌های فرانت‌اند
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    chart_labels = []
    chart_data = []
    chart_title = ""
    
    # اگر ستون‌ها انتخاب نشده باشند، به صورت پیش‌فرض انتخاب می‌شوند
    if not col_x and text_cols:
        col_x = text_cols[0]
    if not col_y and numeric_cols:
        col_y = numeric_cols[0]

    # اگر ستون‌های مورد نیاز برای تحلیل وجود داشته باشند
    if col_x and col_y and col_x in df.columns and col_y in df.columns:
        chart_title = f"نمودار مجموع {col_y} بر حسب {col_x}"

        # تحلیل داده: گروه‌بندی و جمع زدن (Top 10)
        grouped_df = df.groupby(col_x)[col_y].sum().sort_values(ascending=False).head(10)
        
        chart_labels = grouped_df.index.tolist()
        chart_data = grouped_df.values.tolist()
        
    return {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'chart_title': chart_title,
        'numeric_cols': numeric_cols,
        'text_cols': text_cols,
    }


# ویو اصلی: بارگذاری صفحه
def dashboard_view(request):
    form = DataFileForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    file_obj = DataFile.objects.last()
    
    df = None
    table_html = None
    stats_html = None
    error_message = None
    analysis_data = {
        'chart_labels': json.dumps([]),
        'chart_data': json.dumps([]),
        'chart_title': "",
        'numeric_cols': [],
        'text_cols': [],
    }

    if file_obj:
        try:
            # ۱. گرفتن اطلاعات و لیست ستون‌ها
            data = analyze_data(file_obj)
            
            # تبدیل به JSON برای نمایش اولیه
            data['chart_labels'] = json.dumps(data['chart_labels'])
            data['chart_data'] = json.dumps(data['chart_data'])
            analysis_data.update(data)
            
            # ۲. ساخت جدول پیش نمایش و آمار توصیفی
            df = pd.read_csv(file_obj.file.path)
            table_html = df.head(10).to_html(classes='table table-striped table-hover', index=False)
            stats_html = df.describe().T.to_html(classes='table table-bordered table-sm', float_format='%.2f') 

        except Exception as e:
            error_message = f"خطا در پردازش فایل: {e}"

    context = {
        'form': form,
        'file_obj': file_obj,
        'table_html': table_html,
        'stats_html': stats_html,
        'error_message': error_message,
        'analysis_data': analysis_data, # ارسال همه داده‌ها
    }
    
    return render(request, 'dashboard/index.html', context)


# ویو AJAX: دریافت داده بر اساس انتخاب کاربر
def get_chart_data(request):
    file_obj = DataFile.objects.last()
    
    if request.method == 'GET' and file_obj:
        # دریافت ستون‌های انتخابی از درخواست AJAX
        col_x = request.GET.get('col_x')
        col_y = request.GET.get('col_y')
        
        try:
            # تحلیل مجدد با ستون‌های ارسالی کاربر
            data = analyze_data(file_obj, col_x, col_y)
            
            # ارسال پاسخ در قالب JSON به جاواسکریپت
            return JsonResponse({
                'labels': data['chart_labels'],
                'data': data['chart_data'],
                'title': data['chart_title'],
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'No file or invalid request'}, status=400)


# تابع حذف فایل (بدون تغییر)
def delete_file(request, pk):
    file_obj = get_object_or_404(DataFile, pk=pk)
    file_obj.file.delete()
    file_obj.delete()
    return redirect('dashboard')