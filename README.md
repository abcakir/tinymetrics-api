# 🚀 TinyMetrics API

A scalable, high-performance URL Shortener service featuring real-time analytics and OAuth2 authentication. Built for cloud deployment.

## ✨ Features
- **Shorten URLs**: Efficient algorithm for generating short codes.
- **Analytics**: Track clicks, user agents, and timestamps in real-time.
- **Security**: OAuth2 (GitHub) & JWT Authentication.
- **Containerized**: Fully Dockerized for easy deployment (AWS compatible).

## 🛠 Tech Stack
- **Core:** Python 3.11+, FastAPI
- **Database:** PostgreSQL, SQLAlchemy, Alembic
- **Infrastructure:** Docker, Docker Compose
- **Testing:** Pytest

## ⚡️ Quick Start

### Prerequisites
- Docker & Docker Compose

### Run Locally
```bash
# 1. Clone the repo
git clone [https://github.com/DEIN_USERNAME/tinymetrics-api.git](https://github.com/DEIN_USERNAME/tinymetrics-api.git)

# 2. Create .env file
cp .env.example .env

# 3. Start services
docker-compose up -d --build

# 4. Access API Docs
Open http://localhost:8000/docs