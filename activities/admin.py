from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'sub_branch', 'date', 'day', 'time', 'duration', 'notes', 'created_at', 'updated_at']
    list_filter = ['date', 'day', 'created_at']
    search_fields = ['sub_branch__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
