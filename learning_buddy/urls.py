from django.contrib import admin
from django.urls import path, include
from .health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('curriculum.urls')),
    path('api/', include('activities.urls')),
    path('api/', include('analytics.urls')),
]
