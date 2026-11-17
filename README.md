# Learning Buddy - Backend

Learning Buddy is a learning tracking application built with **Django REST Framework**. It allows users to organize their study activities in a hierarchical structure (Domain → Branch → Sub-Branch → Topic) and track time spent with comprehensive analytics.

## 🚀 Features

- **JWT Authentication**: Secure user signup, login, and profile management.
- **Hierarchical Structure**: Organize learning into Domains, Branches, Sub-Branches, and Topics.
- **Activity Tracking**: Log learning sessions with duration, time, day, notes, and topic tags.
- **Analytics Dashboard**: Get insights into your learning progress:
  - Weekly/Monthly/Quarterly summaries.
  - Breakdown by Domain, Branch, Sub-Branch, and Topic.
  - Daily activity tracking with multi-entity comparison.
  - Learning streaks calculation.
  - Time-of-day and weekday productivity insights.
- **Topic Management**: Tag activities with topics for granular tracking.
- **Efficient API**: Optimized with `select_related` and `prefetch_related` to avoid N+1 queries.
- **Dockerized**: Ready for development and production with Docker and PostgreSQL.

## 🛠️ Technology Stack

- **Framework**: Django 5.0.1
- **API**: Django REST Framework 3.14.0
- **Auth**: djangorestframework-simplejwt (JWT)
- **Database**: PostgreSQL 16
- **Package Manager**: UV
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- `sudo` privileges (if required for Docker)

## 🗄️ Database Configuration

By default, the application uses **PostgreSQL**. The following default credentials are used in development (configured via `.env`):

- **Database**: `learning_buddy`
- **User**: `postgres`
- **Password**: `postgres`
- **Host**: `db`
- **Port**: `5432`

> [!NOTE]
> Database data is persisted in a Docker volume named `learning_buddy_data`.

## ⚙️ Setup & Installation

1. **Clone or Navigate to the project directory**:
   ```bash
   cd learning_buddy
   ```

2. **Configure Environment Variables**:
   Copy the example environment file and edit it:
   ```bash
   cp .env.example .env
   ```

3. **Start the Application**:
   Use Docker Compose to build and start the services:
   ```bash
   docker compose up -d --build
   ```

4. **Run Migrations**:
   ```bash
   docker compose exec web python manage.py migrate
   ```

6. **Default Superuser Credentials**:
   If you have already run the setup steps, an initial superuser is available:
   - **Username**: `admin`
   - **Password**: `admin`
   - **Email**: `admin@example.com`

## 🔗 Accessing the Application

- **API Root**: [http://localhost:8000/api/](http://localhost:8000/api/)
- **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Health Check**: [http://localhost:8000/health/](http://localhost:8000/health/)

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/signup/` - New user registration.
- `POST /api/auth/login/` - Login and get JWT tokens.
- `POST /api/auth/token/refresh/` - Refresh access token.
- `GET /api/auth/profile/` - Get current user profile.
- `POST /api/auth/simple-password-reset/` - Simple password reset (dev only).

### Curriculum & Activities
- `GET/POST /api/domains/` - Manage Domains.
- `GET/POST /api/branches/` - Manage Branches.
- `GET/POST /api/sub-branches/` - Manage Sub-Branches.
- `GET/POST /api/topics/` - Manage Topics (tags for activities).
- `GET/POST /api/activities/` - Track Learning Activities (supports time, day, topics).

### Analytics
- `GET /api/analytics/summary/` - Period-based summary (week/month/quarter).
- `GET /api/analytics/by-domain/` - Analytics grouped by domain.
- `GET /api/analytics/by-branch/` - Analytics grouped by branch.
- `GET /api/analytics/by-sub-branch/` - Analytics grouped by sub-branch.
- `GET /api/analytics/daily/` - Daily activity breakdown with multi-entity comparison.
- `GET /api/analytics/streak/` - Current and longest learning streaks.
- `GET /api/analytics/topics-detailed/` - Detailed topic analytics with sub-branch filtering.

## 🔑 API Usage

To access protected endpoints, you must include the JWT token in the `Authorization` header:

```bash
Authorization: Bearer <your_access_token>
```

### 🌓 Dark Mode / Frontend
This backend is designed to work with the **Learning Buddy Frontend**. Ensure CORS settings in `.env` include your frontend's URL (default: `http://localhost:3000` or `http://localhost:5173`).

## 📁 Project Structure

```text
learning_buddy/
├── accounts/          # User registration & Auth
├── activities/        # Time tracking logic
├── analytics/         # Progress metrics & dashboards
├── curriculum/        # Learning hierarchy (Domains, etc.)
├── learning_buddy/    # Root configuration & settings
├── manage.py          # Django CLI
├── pyproject.toml     # Python dependencies
├── Dockerfile         # Container image definition
└── docker-compose.yml # Service orchestration
```

## 🧪 Testing

Run the test suite using `pytest`:
```bash
docker compose exec web pytest
```

## 🛠️ Development Tools

- **Code Formatting**: `docker compose exec web black .`
- **Import Sorting**: `docker compose exec web isort .`
- **Linting**: `docker compose exec web flake8`
