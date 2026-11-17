import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Domain

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

@pytest.mark.django_db
class TestDomainAPI:
    def test_create_domain(self, authenticated_client):
        response = authenticated_client.post('/api/domains/', {
            'name': 'Programming',
            'description': 'Learning programming'
        })
        assert response.status_code == 201
        assert response.data['name'] == 'Programming'
    
    def test_list_domains(self, authenticated_client, user):
        Domain.objects.create(user=user, name='Domain 1')
        Domain.objects.create(user=user, name='Domain 2')
        
        response = authenticated_client.get('/api/domains/')
        assert response.status_code == 200
        assert len(response.data) == 2
    
    def test_cannot_access_other_user_domain(self, authenticated_client):
        other_user = User.objects.create_user(
            username='other@example.com',
            email='other@example.com',
            password='pass123'
        )
        domain = Domain.objects.create(user=other_user, name='Other Domain')
        
        response = authenticated_client.get(f'/api/domains/{domain.id}/')
        assert response.status_code == 404
