# Learning Buddy - Complete Setup Guide

## Table of Contents
- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Docker Commands](#docker-commands)
- [Development Workflow](#development-workflow)
- [Code Examples](#code-examples)
- [Testing](#testing)
- [Deployment](#deployment)

---

## Project Overview

**Learning Buddy** is a learning tracking application built with Django REST Framework that allows users to organize their study activities in a hierarchical structure (Domain → Branch → Sub-Branch) and track time spent with comprehensive analytics.

### Key Features
- User authentication with JWT
- Hierarchical learning structure organization
- Time tracking for learning activities
- Analytics by week, month, year, domain, branch, and sub-branch
- RESTful API design
- PostgreSQL database with Docker
- Optimized queries for performance

---

## Technology Stack

- **Framework**: Django 5.0.1 + Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL 16 (Docker container)
- **Package Manager**: UV (modern, fast Python package manager)
- **Container**: Docker & Docker Compose
- **Additional Libraries**:
  - django-filter (filtering)
  - django-cors-headers (CORS support)
  - python-decouple (environment variables)
  - psycopg2-binary (PostgreSQL adapter)

---

## Project Structure

```
learning_buddy/
├── docker-compose.yml
├── Dockerfile
├── .env
├── .env.example
├── .dockerignore
├── .gitignore
├── pyproject.toml
├── uv.lock
├── manage.py
├── README.md
├── setup.sh
│
├── learning_buddy/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── backends.py
│   ├── admin.py
│   └── tests.py
│
├── curriculum/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── admin.py
│   └── tests.py
│
├── activities/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   ├── permissions.py
│   ├── admin.py
│   └── tests.py
│
└── analytics/
    ├── __init__.py
    ├── views.py
    ├── serializers.py
    ├── urls.py
    ├── utils.py
    └── tests.py
```

---

## Database Schema

### Relationships Diagram

```
User (Django built-in)
  |
  └── Domain (1:N)
       |
       └── Branch (1:N)
            |
            └── SubBranch (1:N)
                 |
                 └── Activity (1:N)
```

### Models Detail

#### **User Model** (Django Built-in)
```python
Fields:
- id: AutoField (PK)
- email: EmailField (unique, used as username)
- password: CharField (hashed)
- first_name: CharField
- last_name: CharField
- date_joined: DateTimeField
- last_login: DateTimeField
```

#### **Domain Model**
```python
Fields:
- id: AutoField (PK)
- user: ForeignKey(User) CASCADE
- name: CharField(100)
- description: TextField (blank=True)
- created_at: DateTimeField (auto_now_add)
- updated_at: DateTimeField (auto_now)

Constraints:
- unique_together: ['user', 'name']
- ordering: ['name']
- indexes: [('user', 'created_at')]
```

#### **Branch Model**
```python
Fields:
- id: AutoField (PK)
- domain: ForeignKey(Domain) CASCADE
- name: CharField(100)
- description: TextField (blank=True)
- created_at: DateTimeField (auto_now_add)
- updated_at: DateTimeField (auto_now)

Constraints:
- unique_together: ['domain', 'name']
- ordering: ['name']
- indexes: [('domain', 'created_at')]
```

#### **SubBranch Model**
```python
Fields:
- id: AutoField (PK)
- branch: ForeignKey(Branch) CASCADE
- name: CharField(100)
- description: TextField (blank=True)
- created_at: DateTimeField (auto_now_add)
- updated_at: DateTimeField (auto_now)

Constraints:
- unique_together: ['branch', 'name']
- ordering: ['name']
- indexes: [('branch', 'created_at')]
```

#### **Activity Model**
```python
Fields:
- id: AutoField (PK)
- sub_branch: ForeignKey(SubBranch) CASCADE
- date: DateField (default=today, user can edit)
- duration: IntegerField (minutes, min=1)
- notes: TextField (blank=True)
- created_at: DateTimeField (auto_now_add, not editable)
- updated_at: DateTimeField (auto_now)

Constraints:
- ordering: ['-date', '-created_at']
- indexes: [('sub_branch', 'date'), ('date',)]

Notes:
- date: Defaults to today if not provided, can be edited
- created_at: Set once when created, cannot be edited
- updated_at: Updates automatically on every save
```

---

## Setup Instructions

### Prerequisites
- Docker & Docker Compose installed
- Git installed
- UV installed (optional, Docker will handle it)

### Installation Steps

#### **Step 1: Install UV (Optional for local development)**

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On macOS with Homebrew
brew install uv

# On Windows with PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### **Step 2: Clone/Create Project**

```bash
mkdir learning_buddy
cd learning_buddy
```

#### **Step 3: Create Configuration Files**

Create the following files in your project root:

**pyproject.toml**
```toml
[project]
name = "learning-buddy"
version = "0.1.0"
description = "A learning tracking application with Django REST Framework"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "django>=5.0.1",
    "djangorestframework>=3.14.0",
    "djangorestframework-simplejwt>=5.3.1",
    "django-filter>=23.5",
    "django-cors-headers>=4.3.1",
    "python-decouple>=3.8",
    "psycopg2-binary>=2.9.9",
]

[project.optional-dependencies]
dev = [
    "black>=24.1.0",
    "isort>=5.13.0",
    "flake8>=7.0.0",
    "pytest>=7.4.0",
    "pytest-django>=4.7.0",
]
prod = [
    "gunicorn>=21.2.0",
    "whitenoise>=6.6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 100
target-version = ['py311']
exclude = '''
/(
    \.git
  | \.venv
  | migrations
  | __pycache__
)/
'''

[tool.isort]
profile = "black"
line_length = 100
skip_glob = ["*/migrations/*"]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "learning_buddy.settings"
python_files = ["test_*.py", "*_test.py", "tests.py"]
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: learning_buddy_db
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${DATABASE_NAME}
      - POSTGRES_USER=${DATABASE_USER}
      - POSTGRES_PASSWORD=${DATABASE_PASSWORD}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DATABASE_USER} -d ${DATABASE_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    container_name: learning_buddy_web
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=${DEBUG}
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_NAME=${DATABASE_NAME}
      - DATABASE_USER=${DATABASE_USER}
      - DATABASE_PASSWORD=${DATABASE_PASSWORD}
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
```

**Dockerfile**
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

COPY pyproject.toml uv.lock* /app/

RUN uv pip install -r pyproject.toml

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

**.env.example**
```env
# Django Settings
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings
DATABASE_NAME=learning_buddy
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres_secure_password
DATABASE_HOST=db
DATABASE_PORT=5432

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**.dockerignore**
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
dist/
*.egg-info/
.installed.cfg
*.egg
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/static/
/media/
.env
.env.local
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
.git/
.gitignore
Dockerfile
docker-compose.yml
.dockerignore
README.md
*.md
```

**.gitignore**
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/
.venv/
venv/
ENV/
env/
.uv/
uv.lock
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/static/
/media/
/staticfiles/
.env
.env.local
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
.pytest_cache/
.coverage
htmlcov/
*.pid
```

#### **Step 4: Create Environment File**

```bash
cp .env.example .env
# Edit .env with your actual values
```

#### **Step 5: Start Docker Containers**

```bash
docker-compose up --build
```

#### **Step 6: Create Django Apps (in another terminal)**

```bash
# Wait for containers to be fully up, then:
docker-compose exec web django-admin startproject learning_buddy .
docker-compose exec web python manage.py startapp accounts
docker-compose exec web python manage.py startapp curriculum
docker-compose exec web python manage.py startapp activities
docker-compose exec web python manage.py startapp analytics
```

#### **Step 7: Configure Django Settings**

Edit `learning_buddy/settings.py` with the configuration provided in the [Django Settings](#django-settings) section below.

#### **Step 8: Run Migrations**

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

#### **Step 9: Create Superuser**

```bash
docker-compose exec web python manage.py createsuperuser
```

#### **Step 10: Access the Application**

- API Root: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/docs/ (if configured)

---

## API Endpoints

### **Authentication Endpoints**

```
POST   /api/auth/signup/
POST   /api/auth/login/
POST   /api/auth/token/refresh/
POST   /api/auth/password-reset/
POST   /api/auth/password-reset-confirm/
GET    /api/auth/profile/
```

### **Domain Endpoints**

```
GET    /api/domains/
POST   /api/domains/
GET    /api/domains/{id}/
PUT    /api/domains/{id}/
PATCH  /api/domains/{id}/
DELETE /api/domains/{id}/
```

### **Branch Endpoints**

```
GET    /api/branches/
       Query: ?domain={domain_id}
POST   /api/branches/
GET    /api/branches/{id}/
PUT    /api/branches/{id}/
PATCH  /api/branches/{id}/
DELETE /api/branches/{id}/
```

### **Sub-Branch Endpoints**

```
GET    /api/sub-branches/
       Query: ?branch={branch_id}
POST   /api/sub-branches/
GET    /api/sub-branches/{id}/
PUT    /api/sub-branches/{id}/
PATCH  /api/sub-branches/{id}/
DELETE /api/sub-branches/{id}/
```

### **Activity Endpoints**

```
GET    /api/activities/
       Query Params:
       - ?sub_branch={id}
       - ?date={YYYY-MM-DD}
       - ?date_from={YYYY-MM-DD}&date_to={YYYY-MM-DD}
       - ?ordering=-date,duration
POST   /api/activities/
GET    /api/activities/{id}/
PUT    /api/activities/{id}/
PATCH  /api/activities/{id}/
DELETE /api/activities/{id}/
```

### **Analytics Endpoints**

```
GET    /api/analytics/summary/
       Query: ?period=week|month|year&date={YYYY-MM-DD}

GET    /api/analytics/by-domain/
       Query: ?date_from={YYYY-MM-DD}&date_to={YYYY-MM-DD}

GET    /api/analytics/by-branch/
       Query: ?domain={id}&date_from={YYYY-MM-DD}&date_to={YYYY-MM-DD}

GET    /api/analytics/by-sub-branch/
       Query: ?branch={id}&date_from={YYYY-MM-DD}&date_to={YYYY-MM-DD}

GET    /api/analytics/daily/
       Query: ?date_from={YYYY-MM-DD}&date_to={YYYY-MM-DD}

GET    /api/analytics/streak/
```

---

## Docker Commands

### **Container Management**

```bash
# Start containers
docker-compose up

# Start in detached mode (background)
docker-compose up -d

# Stop containers
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v

# Rebuild containers
docker-compose up --build

# Restart specific service
docker-compose restart web
docker-compose restart db
```

### **Logs**

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100
```

### **Django Management Commands**

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Django shell
docker-compose exec web python manage.py shell

# Collect static files
docker-compose exec web python manage.py collectstatic

# Run tests
docker-compose exec web pytest

# Code formatting
docker-compose exec web black .
docker-compose exec web isort .

# Linting
docker-compose exec web flake8
```

### **Database Commands**

```bash
# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d learning_buddy

# Inside PostgreSQL shell:
\dt                              # List all tables
\d+ table_name                   # Describe a table
SELECT * FROM curriculum_domain; # Query data
\q                               # Quit

# Backup database
docker-compose exec db pg_dump -U postgres learning_buddy > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres learning_buddy < backup.sql
```

### **UV Package Management**

```bash
# Install new package
docker-compose exec web uv pip install package-name

# Update all packages
docker-compose exec web uv pip install --upgrade -r pyproject.toml

# List installed packages
docker-compose exec web uv pip list

# Show outdated packages
docker-compose exec web uv pip list --outdated
```

---

## Development Workflow

### **Adding a New Feature**

1. Create a new branch
```bash
git checkout -b feature/new-feature
```

2. Make your changes to models, views, serializers, etc.

3. Create and apply migrations
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

4. Write tests
```bash
# Create tests in tests.py
docker-compose exec web pytest
```

5. Format and lint code
```bash
docker-compose exec web black .
docker-compose exec web isort .
docker-compose exec web flake8
```

6. Commit and push
```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

### **Making Model Changes**

1. Edit your models in `models.py`

2. Create migrations
```bash
docker-compose exec web python manage.py makemigrations
```

3. Review migration file in `migrations/` directory

4. Apply migrations
```bash
docker-compose exec web python manage.py migrate
```

5. Update serializers and views if needed

6. Restart web container
```bash
docker-compose restart web
```

### **Testing the API**

Using cURL:

```bash
# Sign up
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","first_name":"John","last_name":"Doe"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Create Domain (with JWT token)
curl -X POST http://localhost:8000/api/domains/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"name":"Programming","description":"Learning programming"}'
```

Using Python requests:

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "email": "test@example.com",
    "password": "testpass123"
})
token = response.json()['access']

# Create Domain
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/domains/", 
    json={"name": "Programming", "description": "Learning programming"},
    headers=headers
)
print(response.json())
```

---

## Code Examples

### **Django Settings**

`learning_buddy/settings.py`:

```python
from pathlib import Path
from decouple import config, Csv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    
    # Local apps
    'accounts',
    'curriculum',
    'activities',
    'analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'learning_buddy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'learning_buddy.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
CORS_ALLOW_CREDENTIALS = True

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
}

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Email
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Custom Authentication
AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']
```

### **Models Example**

`curriculum/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='domains')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'name']
        ordering = ['name']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"

class Branch(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['domain', 'name']
        ordering = ['name']
        verbose_name_plural = 'Branches'
        indexes = [
            models.Index(fields=['domain', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.domain.name} - {self.name}"

class SubBranch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='sub_branches')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['branch', 'name']
        ordering = ['name']
        verbose_name_plural = 'Sub-Branches'
        indexes = [
            models.Index(fields=['branch', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.branch.name} - {self.name}"
```

`activities/models.py`:

```python
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from curriculum.models import SubBranch

class Activity(models.Model):
    sub_branch = models.ForeignKey(SubBranch, on_delete=models.CASCADE, related_name='activities')
    date = models.DateField(default=timezone.now, help_text="Date when the activity was performed")
    duration = models.IntegerField(validators=[MinValueValidator(1)], help_text="Duration in minutes")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Activities'
        indexes = [
            models.Index(fields=['sub_branch', 'date']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.sub_branch.name} - {self.date} ({self.duration}min)"
```

### **Serializers Example**

`curriculum/serializers.py`:

```python
from rest_framework import serializers
from .models import Domain, Branch, SubBranch

class DomainSerializer(serializers.ModelSerializer):
    branches_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Domain
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'branches_count']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_branches_count(self, obj):
        return obj.branches.count()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BranchSerializer(serializers.ModelSerializer):
    sub_branches_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = ['id', 'domain', 'name', 'description', 'created_at', 'updated_at', 'sub_branches_count']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_sub_branches_count(self, obj):
        return obj.sub_branches.count()
    
    def validate_domain(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only create branches for your own domains.")
        return value

class SubBranchSerializer(serializers.ModelSerializer):
    activities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SubBranch
        fields = ['id', 'branch', 'name', 'description', 'created_at', 'updated_at', 'activities_count']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_activities_count(self, obj):
        return obj.activities.count()
    
    def validate_branch(self, value):
        if value.domain.user != self.context['request'].user:
            raise serializers.ValidationError("You can only create sub-branches for your own branches.")
        return value
```

`activities/serializers.py`:

```python
from rest_framework import serializers
from django.utils import timezone
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    sub_branch_name = serializers.CharField(source='sub_branch.name', read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'sub_branch', 'sub_branch_name', 'date', 
            'duration', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Activity date cannot be in the future.")
        return value
    
    def validate_duration(self, value):
        if value > 1440:  # 24 hours
            raise serializers.ValidationError("Duration cannot exceed 24 hours (1440 minutes).")
        return value
    
    def validate_sub_branch(self, value):
        user = self.context['request'].user
        if value.branch.domain.user != user:
            raise serializers.ValidationError("You can only create activities for your own sub-branches.")
        return value
```

### **Views Example**

`curriculum/views.py`:

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Domain, Branch, SubBranch
from .serializers import DomainSerializer, BranchSerializer, SubBranchSerializer
from .permissions import IsOwner

class DomainViewSet(viewsets.ModelViewSet):
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Domain.objects.filter(user=self.request.user).prefetch_related('branches')

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
        ).filter(branch__domain__user=self.request.user)
        
        # Filter by branch if provided
        branch_id = self.request.query_params.get('branch')
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        
        return queryset
```

`activities/views.py`:

```python
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
        ).filter(sub_branch__branch__domain__user=self.request.user)
```

### **Permissions Example**

`curriculum/permissions.py`:

```python
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners to view/edit their objects.
    """
    
    def has_object_permission(self, request, view, obj):
        # For Domain
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # For Branch
        if hasattr(obj, 'domain'):
            return obj.domain.user == request.user
        
        # For SubBranch
        if hasattr(obj, 'branch'):
            return obj.branch.domain.user == request.user
        
        return False
```

`activities/permissions.py`:

```python
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission for Activity objects.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the activity belongs to the user through the chain
        return obj.sub_branch.branch.domain.user == request.user
```

### **Filters Example**

`activities/filters.py`:

```python
import django_filters
from .models import Activity

class ActivityFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    sub_branch = django_filters.NumberFilter(field_name='sub_branch')
    
    class Meta:
        model = Activity
        fields = ['date', 'sub_branch']
```

### **URLs Configuration**

`learning_buddy/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('curriculum.urls')),
    path('api/', include('activities.urls')),
    path('api/', include('analytics.urls')),
]
```

`accounts/urls.py`:

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, LoginView, ProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
```

`curriculum/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DomainViewSet, BranchViewSet, SubBranchViewSet

router = DefaultRouter()
router.register(r'domains', DomainViewSet, basename='domain')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'sub-branches', SubBranchViewSet, basename='subbranch')

urlpatterns = [
    path('', include(router.urls)),
]
```

`activities/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
]
```

`analytics/urls.py`:

```python
from django.urls import path
from .views import (
    SummaryAnalyticsView,
    DomainAnalyticsView,
    BranchAnalyticsView,
    SubBranchAnalyticsView,
    DailyAnalyticsView,
    StreakAnalyticsView
)

urlpatterns = [
    path('analytics/summary/', SummaryAnalyticsView.as_view(), name='analytics-summary'),
    path('analytics/by-domain/', DomainAnalyticsView.as_view(), name='analytics-domain'),
    path('analytics/by-branch/', BranchAnalyticsView.as_view(), name='analytics-branch'),
    path('analytics/by-sub-branch/', SubBranchAnalyticsView.as_view(), name='analytics-subbranch'),
    path('analytics/daily/', DailyAnalyticsView.as_view(), name='analytics-daily'),
    path('analytics/streak/', StreakAnalyticsView.as_view(), name='analytics-streak'),
]
```

### **Analytics Views Example**

`analytics/utils.py`:

```python
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count

def get_period_dates(period, date=None):
    """Returns start_date and end_date for given period"""
    if date is None:
        date = timezone.now().date()
    
    if period == 'week':
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'month':
        start_date = date.replace(day=1)
        next_month = start_date + timedelta(days=32)
        end_date = next_month.replace(day=1) - timedelta(days=1)
    elif period == 'year':
        start_date = date.replace(month=1, day=1)
        end_date = date.replace(month=12, day=31)
    else:
        raise ValueError("Period must be 'week', 'month', or 'year'")
    
    return start_date, end_date

def calculate_streak(activities):
    """Calculate current and longest streak from activities"""
    if not activities:
        return {'current_streak': 0, 'longest_streak': 0}
    
    # Get unique dates sorted in descending order
    dates = sorted(set(a.date for a in activities), reverse=True)
    
    if not dates:
        return {'current_streak': 0, 'longest_streak': 0}
    
    # Calculate current streak
    current_streak = 0
    today = timezone.now().date()
    
    for i, date in enumerate(dates):
        expected_date = today - timedelta(days=i)
        if date == expected_date:
            current_streak += 1
        else:
            break
    
    # Calculate longest streak
    longest_streak = 1
    temp_streak = 1
    
    for i in range(len(dates) - 1):
        if (dates[i] - dates[i + 1]).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1
    
    return {
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'last_activity_date': dates[0] if dates else None
    }
```

`analytics/views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime
from activities.models import Activity
from .utils import get_period_dates, calculate_streak

class SummaryAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        period = request.query_params.get('period', 'week')
        date_str = request.query_params.get('date')
        
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()
        
        start_date, end_date = get_period_dates(period, date)
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        stats = activities.aggregate(
            total_duration=Sum('duration'),
            total_activities=Count('id')
        )
        
        # Calculate average daily duration
        days_in_period = (end_date - start_date).days + 1
        avg_daily = stats['total_duration'] / days_in_period if stats['total_duration'] else 0
        
        # Domain breakdown
        domain_stats = activities.values(
            'sub_branch__branch__domain__id',
            'sub_branch__branch__domain__name'
        ).annotate(
            duration=Sum('duration')
        ).order_by('-duration')
        
        total = stats['total_duration'] or 1
        domains_data = [
            {
                'domain_id': d['sub_branch__branch__domain__id'],
                'domain_name': d['sub_branch__branch__domain__name'],
                'duration': d['duration'],
                'percentage': round((d['duration'] / total) * 100, 2)
            }
            for d in domain_stats
        ]
        
        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'total_duration': stats['total_duration'] or 0,
            'total_activities': stats['total_activities'] or 0,
            'average_daily_duration': round(avg_daily, 2),
            'domains': domains_data
        })

class DomainAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        )
        
        if date_from:
            activities = activities.filter(date__gte=date_from)
        if date_to:
            activities = activities.filter(date__lte=date_to)
        
        # Group by domain, then branch, then sub-branch
        domain_data = {}
        
        for activity in activities:
            domain = activity.sub_branch.branch.domain
            branch = activity.sub_branch.branch
            sub_branch = activity.sub_branch
            
            if domain.id not in domain_data:
                domain_data[domain.id] = {
                    'domain_id': domain.id,
                    'domain_name': domain.name,
                    'total_duration': 0,
                    'branches': {}
                }
            
            if branch.id not in domain_data[domain.id]['branches']:
                domain_data[domain.id]['branches'][branch.id] = {
                    'branch_id': branch.id,
                    'branch_name': branch.name,
                    'duration': 0,
                    'sub_branches': {}
                }
            
            if sub_branch.id not in domain_data[domain.id]['branches'][branch.id]['sub_branches']:
                domain_data[domain.id]['branches'][branch.id]['sub_branches'][sub_branch.id] = {
                    'sub_branch_id': sub_branch.id,
                    'sub_branch_name': sub_branch.name,
                    'duration': 0
                }
            
            domain_data[domain.id]['total_duration'] += activity.duration
            domain_data[domain.id]['branches'][branch.id]['duration'] += activity.duration
            domain_data[domain.id]['branches'][branch.id]['sub_branches'][sub_branch.id]['duration'] += activity.duration
        
        # Convert to list format
        result = []
        for domain in domain_data.values():
            domain['branches'] = [
                {
                    **branch,
                    'sub_branches': list(branch['sub_branches'].values())
                }
                for branch in domain['branches'].values()
            ]
            result.append(domain)
        
        return Response(result)

class BranchAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        domain_id = request.query_params.get('domain')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        )
        
        if domain_id:
            activities = activities.filter(sub_branch__branch__domain_id=domain_id)
        if date_from:
            activities = activities.filter(date__gte=date_from)
        if date_to:
            activities = activities.filter(date__lte=date_to)
        
        branch_stats = activities.values(
            'sub_branch__branch__id',
            'sub_branch__branch__name'
        ).annotate(
            total_duration=Sum('duration'),
            activities_count=Count('id')
        ).order_by('-total_duration')
        
        result = [
            {
                'branch_id': b['sub_branch__branch__id'],
                'branch_name': b['sub_branch__branch__name'],
                'total_duration': b['total_duration'],
                'activities_count': b['activities_count']
            }
            for b in branch_stats
        ]
        
        return Response(result)

class SubBranchAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        branch_id = request.query_params.get('branch')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        )
        
        if branch_id:
            activities = activities.filter(sub_branch__branch_id=branch_id)
        if date_from:
            activities = activities.filter(date__gte=date_from)
        if date_to:
            activities = activities.filter(date__lte=date_to)
        
        subbranch_stats = activities.values(
            'sub_branch__id',
            'sub_branch__name'
        ).annotate(
            total_duration=Sum('duration'),
            activities_count=Count('id')
        ).order_by('-total_duration')
        
        result = [
            {
                'sub_branch_id': s['sub_branch__id'],
                'sub_branch_name': s['sub_branch__name'],
                'total_duration': s['total_duration'],
                'activities_count': s['activities_count']
            }
            for s in subbranch_stats
        ]
        
        return Response(result)

class DailyAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        )
        
        if date_from:
            activities = activities.filter(date__gte=date_from)
        if date_to:
            activities = activities.filter(date__lte=date_to)
        
        daily_stats = activities.values('date').annotate(
            total_duration=Sum('duration'),
            activities_count=Count('id')
        ).order_by('-date')
        
        result = [
            {
                'date': d['date'],
                'total_duration': d['total_duration'],
                'activities_count': d['activities_count']
            }
            for d in daily_stats
        ]
        
        return Response(result)

class StreakAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        activities = Activity.objects.filter(
            sub_branch__branch__domain__user=request.user
        ).order_by('-date')
        
        streak_data = calculate_streak(activities)
        
        return Response(streak_data)
```

### **Authentication Backend**

`accounts/backends.py`:

```python
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using email instead of username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
```

### **Admin Configuration**

`curriculum/admin.py`:

```python
from django.contrib import admin
from .models import Domain, Branch, SubBranch

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'domain__name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SubBranch)
class SubBranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'branch__name']
    readonly_fields = ['created_at', 'updated_at']
```

`activities/admin.py`:

```python
from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['sub_branch', 'date', 'duration', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['sub_branch__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
```

---

## Testing

### **Setup Testing**

`pytest.ini` (create in project root):

```ini
[pytest]
DJANGO_SETTINGS_MODULE = learning_buddy.settings
python_files = tests.py test_*.py *_tests.py
addopts = --reuse-db
```

### **Example Tests**

`curriculum/tests.py`:

```python
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Domain, Branch, SubBranch

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
```

### **Running Tests**

```bash
# Run all tests
docker-compose exec web pytest

# Run specific test file
docker-compose exec web pytest curriculum/tests.py

# Run with coverage
docker-compose exec web pytest --cov=.

# Run with verbose output
docker-compose exec web pytest -v

# Run specific test
docker-compose exec web pytest curriculum/tests.py::TestDomainAPI::test_create_domain
```

---

## Deployment

### **Production Dockerfile**

```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

COPY pyproject.toml uv.lock* /app/
RUN uv pip install -r pyproject.toml --extra prod

COPY . /app/
RUN python manage.py collectstatic --noinput

# Production stage
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

RUN useradd -m -u 1000 django && chown -R django:django /app
USER django

EXPOSE 8000

CMD ["gunicorn", "learning_buddy.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

### **Production docker-compose.yml**

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${DATABASE_NAME}
      - POSTGRES_USER=${DATABASE_USER}
      - POSTGRES_PASSWORD=${DATABASE_PASSWORD}
    networks:
      - backend

  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: gunicorn learning_buddy.wsgi:application --bind 0.0.0.0:8000 --workers 3
    volumes:
      - static_volume:/app/staticfiles
    expose:
      - 8000
    environment:
      - DEBUG=False
      - DATABASE_HOST=db
    depends_on:
      - db
    networks:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    volumes:
      - static_volume:/app/staticfiles
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    networks:
      - backend

volumes:
  postgres_data:
  static_volume:

networks:
  backend:
```

### **Production Environment Variables**

```env
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_NAME=learning_buddy
DATABASE_USER=postgres
DATABASE_PASSWORD=very-secure-password
DATABASE_HOST=db
DATABASE_PORT=5432

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Troubleshooting

### **Common Issues**

#### Database connection errors
```bash
# Check if PostgreSQL is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### Migration errors
```bash
# Reset migrations (WARNING: loses data)
docker-compose exec web python manage.py migrate --fake app_name zero
docker-compose exec web python manage.py migrate app_name

# Or reset database completely
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

#### Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"
```

#### Permission denied errors
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with sudo
sudo docker-compose up
```

---

## Additional Resources

### **Useful Commands Cheat Sheet**

```bash
# Docker
docker-compose up -d                    # Start in background
docker-compose down                     # Stop all services
docker-compose logs -f web              # Follow web logs
docker-compose exec web bash            # Access web container shell

# Django
python manage.py makemigrations         # Create migrations
python manage.py migrate                # Apply migrations
python manage.py createsuperuser        # Create admin user
python manage.py shell                  # Django shell
python manage.py dbshell                # Database shell

# UV
uv pip install package                  # Install package
uv pip list                             # List packages
uv pip install --upgrade package        # Upgrade package

# Testing
pytest                                  # Run all tests
pytest -v                               # Verbose output
pytest --cov=.                          # With coverage

# Code Quality
black .                                 # Format code
isort .                                 # Sort imports
flake8                                  # Lint code
```

### **API Request Examples**

```bash
# Set base URL and token
export BASE_URL="http://localhost:8000/api"
export TOKEN="your-jwt-token-here"

# Sign up
curl -X POST $BASE_URL/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123","first_name":"John","last_name":"Doe"}'

# Login
curl -X POST $BASE_URL/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}'

# Create Domain
curl -X POST $BASE_URL/domains/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Programming","description":"Learning to code"}'

# Get all activities
curl -X GET "$BASE_URL/activities/?date_from=2024-01-01&date_to=2024-01-31" \
  -H "Authorization: Bearer $TOKEN"

# Get analytics summary
curl -X GET "$BASE_URL/analytics/summary/?period=week" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Performance Optimization Tips

### **Database Optimization**

1. **Use select_related for foreign keys**:
   ```python
   Activity.objects.select_related('sub_branch__branch__domain')
   ```

2. **Use prefetch_related for reverse relations**:
   ```python
   Domain.objects.prefetch_related('branches__sub_branches')
   ```

3. **Add database indexes** (already included in models):
   ```python
   indexes = [
       models.Index(fields=['date']),
       models.Index(fields=['sub_branch', 'date']),
   ]
   ```

4. **Use aggregation instead of Python loops**:
   ```python
   # Good
   activities.aggregate(total=Sum('duration'))
   
   # Bad
   total = sum(activity.duration for activity in activities)
   ```

### **Query Optimization**

```python
# Bad - N+1 query problem
domains = Domain.objects.all()
for domain in domains:
    print(domain.branches.count())  # One query per domain

# Good - Single query with annotation
domains = Domain.objects.annotate(
    branch_count=Count('branches')
)
for domain in domains:
    print(domain.branch_count)  # No additional queries
```

### **Caching (Optional)**

Add Redis for caching (future enhancement):

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}

# Usage in views
from django.core.cache import cache

def get_analytics(user):
    cache_key = f'analytics_{user.id}'
    data = cache.get(cache_key)
    
    if data is None:
        data = calculate_analytics(user)
        cache.set(cache_key, data, 3600)  # Cache for 1 hour
    
    return data
```

---

## Security Best Practices

### **Environment Variables**
- Never commit `.env` file to git
- Use strong SECRET_KEY in production
- Use strong database passwords
- Rotate JWT tokens regularly

### **HTTPS in Production**
```python
# settings.py (production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### **CORS Configuration**
```python
# Only allow specific origins
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]

# Don't use CORS_ORIGIN_ALLOW_ALL = True in production
```

### **Rate Limiting**
Install django-ratelimit:
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='100/h')
def my_view(request):
    pass
```

---

## Backup and Restore

### **Backup Database**

```bash
# Create backup
docker-compose exec db pg_dump -U postgres learning_buddy > backup_$(date +%Y%m%d_%H%M%S).sql

# Create compressed backup
docker-compose exec db pg_dump -U postgres learning_buddy | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### **Restore Database**

```bash
# Restore from backup
docker-compose exec -T db psql -U postgres learning_buddy < backup_20240124.sql

# Restore from compressed backup
gunzip < backup_20240124.sql.gz | docker-compose exec -T db psql -U postgres learning_buddy
```

### **Automated Backups**

Create `backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="learning_buddy_backup_$DATE.sql.gz"

# Create backup
docker-compose exec db pg_dump -U postgres learning_buddy | gzip > "$BACKUP_DIR/$FILENAME"

# Keep only last 30 days of backups
find $BACKUP_DIR -name "learning_buddy_backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $FILENAME"
```

Add to crontab for daily backups:
```bash
0 2 * * * /path/to/backup.sh
```

---

## Monitoring and Logging

### **Django Logging Configuration**

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

### **Health Check Endpoint**

Create `learning_buddy/health.py`:

```python
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

Add to `urls.py`:
```python
from .health import health_check

urlpatterns = [
    path('health/', health_check),
    # ... other urls
]
```

---

## FAQ

### **Q: How do I change the database from PostgreSQL to MySQL?**

Update `pyproject.toml`:
```toml
dependencies = [
    # ... other packages
    "mysqlclient>=2.2.0",  # Instead of psycopg2-binary
]
```

Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT', default='3306'),
    }
}
```

### **Q: How do I add email verification on signup?**

Use django-allauth or implement custom email verification using tokens.

### **Q: Can I use SQLite for development?**

Yes, update `settings.py`:
```python
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### **Q: How do I export data to CSV/Excel?**

Install pandas and create an export endpoint:
```python
import pandas as pd
from django.http import HttpResponse

def export_activities(request):
    activities = Activity.objects.filter(
        sub_branch__branch__domain__user=request.user
    ).values('date', 'duration', 'notes')
    
    df = pd.DataFrame(activities)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="activities.csv"'
    df.to_csv(response, index=False)
    
    return response
```

---

## Next Steps and Enhancements

### **Potential Features to Add**

1. **Goals and Targets**
   - Set learning goals
   - Track progress towards goals
   - Notifications for goal milestones

2. **Social Features**
   - Share progress with friends
   - Leaderboards
   - Study groups

3. **Advanced Analytics**
   - Weekly/Monthly reports
   - Productivity heatmaps
   - Time distribution charts

4. **Mobile App**
   - React Native or Flutter
   - Use same Django API

5. **Pomodoro Timer**
   - Built-in timer
   - Auto-create activities

6. **AI Recommendations**
   - Suggest optimal study times
   - Recommend areas to focus on

7. **Export/Import**
   - Export to various formats
   - Import from other apps

8. **Notifications**
   - Email/Push notifications
   - Daily reminders
   - Streak alerts

---

## Contributing

### **Development Setup**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `docker-compose exec web pytest`
5. Format code: `docker-compose exec web black .`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

### **Code Standards**

- Follow PEP 8
- Write tests for new features
- Update documentation
- Use meaningful commit messages

---

## License

This project is licensed under the MIT License.

---

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Contact: your-email@example.com

---

## Changelog

### Version 0.1.0 (2024-01-24)
- Initial release
- User authentication with JWT
- Hierarchical learning structure (Domain → Branch → Sub-Branch)
- Activity tracking
- Analytics endpoints
- Docker setup with PostgreSQL
- UV package management

---

**Happy Learning! 📚🚀**