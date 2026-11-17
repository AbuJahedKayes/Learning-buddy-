from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from curriculum.models import SubBranch

class Activity(models.Model):
    sub_branch = models.ForeignKey(SubBranch, on_delete=models.CASCADE, related_name='activities')
    topics = models.ManyToManyField('curriculum.Topic', related_name='activities')
    date = models.DateField(default=timezone.now, help_text="Date when the activity was performed")
    day = models.CharField(max_length=10, blank=True, help_text="Day of the week")
    time = models.TimeField(null=True, blank=True, help_text="Time of the activity")
    duration = models.IntegerField(validators=[MinValueValidator(1)], help_text="Duration in minutes")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Activities'
        indexes = [
            models.Index(fields=['sub_branch', 'date']),
            models.Index(fields=['date']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        
        # Always update/set day based on date
        if self.date:
            self.day = self.date.strftime('%A')
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sub_branch.name} - {self.date} ({self.duration}min)"
