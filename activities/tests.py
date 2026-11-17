import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from curriculum.models import Domain, Branch, SubBranch
from .models import Activity
from datetime import date

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
def domain(user):
    return Domain.objects.create(user=user, name='Programming')

@pytest.fixture
def branch(domain):
    return Branch.objects.create(domain=domain, name='Python')

@pytest.fixture
def sub_branch(branch):
    return SubBranch.objects.create(branch=branch, name='Django')

@pytest.mark.django_db
class TestActivityAPI:
    def test_create_activity(self, authenticated_client, sub_branch):
        response = authenticated_client.post('/api/activities/', {
            'sub_branch': sub_branch.id,
            'date': str(date.today()),
            'duration': 60,
            'notes': 'Learned Django basics'
        })
        assert response.status_code == 201
        assert response.data['duration'] == 60

    def test_list_activities(self, authenticated_client, sub_branch):
        Activity.objects.create(
            sub_branch=sub_branch,
            date=date.today(),
            duration=30
        )
        response = authenticated_client.get('/api/activities/')
        assert response.status_code == 200

    def test_cannot_access_other_user_activities(self, api_client, sub_branch):
        other_user = User.objects.create_user(
            username='other@example.com',
            email='other@example.com',
            password='pass123'
        )
        api_client.force_authenticate(user=other_user)
        
        Activity.objects.create(
            sub_branch=sub_branch,
            date=date.today(),
            duration=45
        )
        
        response = api_client.get('/api/activities/')
        assert response.status_code == 200
        assert len(response.data.get('results', response.data)) == 0
