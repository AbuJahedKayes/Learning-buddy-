from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomainViewSet, BranchViewSet, SubBranchViewSet, TopicViewSet

router = DefaultRouter()
router.register(r'domains', DomainViewSet, basename='domain')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'sub-branches', SubBranchViewSet, basename='subbranch')
router.register(r'topics', TopicViewSet, basename='topic')

urlpatterns = [
    path('', include(router.urls)),
]
