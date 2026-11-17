from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Activity
from .serializers import ActivitySerializer
from .filters import ActivityFilter
from .permissions import IsOwner

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ActivityFilter
    ordering_fields = ['date', 'duration', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        return Activity.objects.select_related(
            'sub_branch', 'sub_branch__branch', 'sub_branch__branch__domain'
        ).prefetch_related('topics').filter(
            sub_branch__branch__domain__user=self.request.user
        )
