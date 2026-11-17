from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Domain, Branch, SubBranch, Topic
from .serializers import DomainSerializer, BranchSerializer, SubBranchSerializer, TopicSerializer
from .permissions import IsOwner

class DomainViewSet(viewsets.ModelViewSet):
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Domain.objects.filter(user=self.request.user).prefetch_related('branches')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        queryset = Branch.objects.select_related('domain').filter(
            domain__user=self.request.user
        ).prefetch_related('sub_branches')
        
        # Filter by domain if provided
        domain_id = self.request.query_params.get('domain')
        if domain_id:
            queryset = queryset.filter(domain_id=domain_id)
        
        return queryset

class SubBranchViewSet(viewsets.ModelViewSet):
    serializer_class = SubBranchSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        queryset = SubBranch.objects.select_related(
            'branch', 'branch__domain'
        ).filter(branch__domain__user=self.request.user).prefetch_related('topics')
        
        # Filter by branch if provided
        branch_id = self.request.query_params.get('branch')
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        
        return queryset

class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = Topic.objects.select_related(
            'sub_branch', 'sub_branch__branch', 'sub_branch__branch__domain'
        ).filter(sub_branch__branch__domain__user=self.request.user)

        # Filter by sub_branch if provided
        sub_branch_id = self.request.query_params.get('sub_branch')
        if sub_branch_id:
            queryset = queryset.filter(sub_branch_id=sub_branch_id)
        
        return queryset
