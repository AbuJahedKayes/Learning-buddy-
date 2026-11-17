import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

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
class TestSignUp:
    def test_signup_success(self, api_client):
        response = api_client.post('/api/auth/signup/', {
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        assert response.status_code == 201
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_signup_duplicate_email(self, api_client, user):
        response = api_client.post('/api/auth/signup/', {
            'email': 'test@example.com',
            'password': 'anotherpass123'
        })
        assert response.status_code == 400

@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, api_client, user):
        response = api_client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_invalid_credentials(self, api_client):
        response = api_client.post('/api/auth/login/', {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        })
        assert response.status_code == 401

@pytest.mark.django_db
class TestProfile:
    def test_profile_authenticated(self, authenticated_client, user):
        response = authenticated_client.get('/api/auth/profile/')
        assert response.status_code == 200
        assert response.data['email'] == user.email

    def test_profile_unauthenticated(self, api_client):
        response = api_client.get('/api/auth/profile/')
        assert response.status_code == 401
