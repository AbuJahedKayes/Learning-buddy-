from rest_framework import serializers
from .models import Domain, Branch, SubBranch, Topic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'sub_branch', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SubBranchSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    
    class Meta:
        model = SubBranch
        fields = ['id', 'branch', 'name', 'description', 'topics', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class BranchSerializer(serializers.ModelSerializer):
    sub_branches = SubBranchSerializer(many=True, read_only=True)
    
    class Meta:
        model = Branch
        fields = ['id', 'domain', 'name', 'description', 'sub_branches', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class DomainSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    
    class Meta:
        model = Domain
        fields = ['id', 'user', 'name', 'description', 'branches', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
