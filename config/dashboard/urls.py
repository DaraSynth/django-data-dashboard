from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('delete/<int:pk>/', views.delete_file, name='delete_file'),
    
    # مسیر جدید برای دریافت داده نمودار از طریق AJAX
    path('get_chart_data/', views.get_chart_data, name='get_chart_data'),
]
