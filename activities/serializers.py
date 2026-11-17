from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    sub_branch_name = serializers.CharField(source='sub_branch.name', read_only=True)
    topic_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'sub_branch', 'sub_branch_name', 'topics', 'topic_names',
            'date', 'day', 'time', 'duration', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['day', 'created_at', 'updated_at']
    
    def get_topic_names(self, obj):
        return [topic.name for topic in obj.topics.all()]
    
    def validate_date(self, value):
        # Allow up to 1 day in the future to account for timezone differences
        tomorrow = timezone.now().date() + timedelta(days=1)
        if value > tomorrow:
            raise serializers.ValidationError("Activity date cannot be in the future.")
        return value
    
    def validate_duration(self, value):
        if value < 1:
            raise serializers.ValidationError("Duration must be at least 1 minute.")
        if value > 1440:  # 24 hours * 60 minutes
            raise serializers.ValidationError("Total duration cannot exceed 24 hours.")
        return value

    def validate_time(self, value):
        # Django's TimeField already handles standard ISO/HH:MM:SS formats,
        # but we can add a custom check if needed. Since DRF does this automatically,
        # we'll just ensure it's not in the future if a date is today (logic can be added).
        return value
    
    def validate_topics(self, value):
        if not value or len(value) < 1:
            raise serializers.ValidationError("An activity must have at least one topic.")
        return value

    def validate(self, data):
        sub_branch = data.get('sub_branch')
        topics = data.get('topics')

        # During partial updates, we might only have one of these
        if not sub_branch and self.instance:
            sub_branch = self.instance.sub_branch
        
        if sub_branch and topics:
            for topic in topics:
                if topic.sub_branch != sub_branch:
                    raise serializers.ValidationError({
                        "topics": f"Topic '{topic.name}' does not belong to sub-branch '{sub_branch.name}'."
                    })
        
        return data

    def validate_sub_branch(self, value):
        user = self.context['request'].user
        if value.branch.domain.user != user:
            raise serializers.ValidationError("You can only create activities for your own sub-branches.")
        return value
