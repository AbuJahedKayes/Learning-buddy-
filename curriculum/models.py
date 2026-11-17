from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='domains')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'name']
        ordering = ['name']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"

class Branch(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['domain', 'name']
        ordering = ['name']
        verbose_name_plural = 'Branches'
        indexes = [
            models.Index(fields=['domain', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.domain.name} - {self.name}"

class SubBranch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='sub_branches')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['branch', 'name']
        ordering = ['name']
        verbose_name_plural = 'Sub-Branches'
        indexes = [
            models.Index(fields=['branch', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.branch.name} - {self.name}"

class Topic(models.Model):
    sub_branch = models.ForeignKey(SubBranch, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['sub_branch', 'name']
        ordering = ['name']
        indexes = [
            models.Index(fields=['sub_branch', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.sub_branch.name} - {self.name}"
