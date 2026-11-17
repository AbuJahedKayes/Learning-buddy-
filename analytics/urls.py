from django.urls import path
from .views import (
    SummaryAnalyticsView,
    DomainAnalyticsView,
    BranchAnalyticsView,
    SubBranchAnalyticsView,
    DailyAnalyticsView,
    StreakAnalyticsView,
    TopicDetailedAnalyticsView
)

urlpatterns = [
    path('analytics/summary/', SummaryAnalyticsView.as_view(), name='analytics-summary'),
    path('analytics/by-domain/', DomainAnalyticsView.as_view(), name='analytics-domain'),
    path('analytics/by-branch/', BranchAnalyticsView.as_view(), name='analytics-branch'),
    path('analytics/by-sub-branch/', SubBranchAnalyticsView.as_view(), name='analytics-subbranch'),
    path('analytics/daily/', DailyAnalyticsView.as_view(), name='analytics-daily'),
    path('analytics/streak/', StreakAnalyticsView.as_view(), name='analytics-streak'),
    path('analytics/topics-detailed/', TopicDetailedAnalyticsView.as_view(), name='analytics-topics-detailed'),
]
