from django.contrib import admin
from django.urls import path
from scheduler import views  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),

    #The Dashboard (homepage)
    path('', views.dashboard_view),

    # API Endpoints
    path('api/schedule/', views.get_schedule),
    path('api/generate/', views.generate_schedule),
    path('api/report-days/', views.get_report_days),
    path('api/demo/clear/', views.demo_clear_data),
    path('api/demo/load/', views.demo_load_data),
]