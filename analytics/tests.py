import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from curriculum.models import Domain, Branch, SubBranch
from activities.models import Activity
from datetime import date, timedelta

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='test@example.com',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def setup_data(user):
    domain = Domain.objects.create(user=user, name='Programming')
    branch = Branch.objects.create(domain=domain, name='Python')
    sub_branch = SubBranch.objects.create(branch=branch, name='Django')
    
    # Create activities for the past week
    for i in range(7):
        Activity.objects.create(
            sub_branch=sub_branch,
            date=date.today() - timedelta(days=i),
            duration=60
        )
    return domain, branch, sub_branch

@pytest.mark.django_db
class TestAnalyticsSummary:
    def test_summary_week(self, authenticated_client, setup_data):
        response = authenticated_client.get('/api/analytics/summary/', {'period': 'week'})
        assert response.status_code == 200
        assert 'total_duration' in response.data
        assert 'total_activities' in response.data

    def test_summary_month(self, authenticated_client, setup_data):
        response = authenticated_client.get('/api/analytics/summary/', {'period': 'month'})
        assert response.status_code == 200

@pytest.mark.django_db
class TestStreakAnalytics:
    def test_streak_calculation(self, authenticated_client, setup_data):
        response = authenticated_client.get('/api/analytics/streak/')
        assert response.status_code == 200
        assert 'current_streak' in response.data
        assert 'longest_streak' in response.data
        assert response.data['current_streak'] >= 1

@pytest.mark.django_db
class TestDomainAnalytics:
    def test_by_domain(self, authenticated_client, setup_data):
        response = authenticated_client.get('/api/analytics/by-domain/')
        assert response.status_code == 200
        assert len(response.data) > 0
