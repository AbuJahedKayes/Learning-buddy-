from django.contrib import admin
from .models import Domain, Branch, SubBranch, Topic

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'name', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'domain__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SubBranch)
class SubBranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'branch', 'name', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'branch__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'sub_branch', 'name', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'sub_branch__name']
    readonly_fields = ['created_at', 'updated_at']
