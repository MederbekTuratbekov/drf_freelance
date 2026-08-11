# Freelance Marketplace API

> Role-based REST API connecting clients with freelancers —
> full project lifecycle from posting to offer, hiring, and review.
> Deployable in minutes via Docker.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.2-green)]()
[![DRF](https://img.shields.io/badge/DRF-3.16-red)]()
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)]()
[![JWT](https://img.shields.io/badge/Auth-JWT-yellow)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Problem

Freelance platforms need strict role separation — clients post and hire,
freelancers browse and bid. Without proper access control, platforms face
data leaks and unauthorized mutations. This API enforces role-based access
at every endpoint with a clean, documented contract for any frontend.

---

## Endpoints

| Method | URL | Role | Description |
|--------|-----|------|-------------|
| POST | `/register/` | Any | Register (client/freelancer) |
| POST | `/login/` | Any | JWT login |
| POST | `/logout/` | Auth | Blacklist token |
| GET/PUT | `/users/me/` | Auth | Own profile |
| GET | `/users/<pk>/` | Auth | View other profile |
| GET/POST | `/projects/` | Auth | Browse / create projects |
| GET | `/projects/<pk>/` | Auth | Project detail |
| GET | `/projects/my/` | Client | Own projects |
| GET/POST | `/offers/` | Freelancer | Browse / submit offers |
| GET | `/offers/my/` | Freelancer | Own offers |
| GET/PUT/DELETE | `/offers/<pk>/` | Freelancer | Manage own offer |
| POST | `/reviews/` | Auth | Leave review |
| GET | `/categories/` | Any | Category list |
| GET | `/categories/<pk>/` | Auth | Category detail |
| GET | `/skills/` | Any | Skills list |

Swagger UI: `http://localhost/en/api/docs/`

---

## Quick Start

```bash
git clone https://github.com/your-username/freelance-marketplace-api
cd freelance-marketplace-api
echo "SECRET_KEY='your-secret-key'" > .env
docker-compose up --build
```

```bash
# Optional: create superuser
docker-compose exec web python manage.py createsuperuser
```

API: `http://localhost/en/`
Swagger: `http://localhost/en/api/docs/`

---

## Demo

**Register as freelancer:**
```bash
curl -X POST http://localhost/en/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_dev", "email": "john@example.com",
       "password": "secret123", "role": "freelancer"}'
```
```json
{
  "user": {"username": "john_dev", "email": "john@example.com"},
  "access": "<JWT_ACCESS_TOKEN>",
  "refresh": "<JWT_REFRESH_TOKEN>"
}
```

**Browse projects:**
```bash
curl "http://localhost/en/projects/?status=open&ordering=budget" \
  -H "Authorization: Bearer <access_token>"
```
```json
[
  {
    "id": 3,
    "title": "Build a landing page",
    "budget": "500",
    "deadline": "2025-10-01",
    "status": "open"
  }
]
```

**Submit an offer (freelancer only):**
```bash
curl -X POST http://localhost/en/offers/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"project": 3, "proposed_budget": "450",
       "proposed_deadline": "2025-09-25",
       "message": "I can deliver this in 3 weeks."}'
```

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.11 |
| Framework | Django 5.2, DRF 3.16 |
| Auth | SimpleJWT + blacklist, django-allauth (OAuth) |
| Database | PostgreSQL (prod) / SQLite (dev) |
| Filtering | django-filter, OrderingFilter, SearchFilter |
| i18n | django-modeltranslation (EN / RU) |
| API Docs | drf-spectacular (Swagger UI) |
| Deploy | Docker Compose, Gunicorn, Nginx |
| Config | python-dotenv |

---

## Project Structure
```
drf_freelance/
    ├── readme.md
    └── freelance/
        ├── manage.py
        ├── Dockerfile
        ├── docker-compose.yml
        ├── requirements.txt
        ├── mysite/
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── urls.py
        │   ├── asgi.py
        │   └── wsgi.py
        ├── freelance/
        │   ├── __init__.py
        │   ├── admin.py
        │   ├── apps.py
        │   ├── models.py
        │   ├── views.py
        │   ├── serializers.py
        │   ├── urls.py
        │   ├── permissions.py
        │   ├── migrations/
        │   │   ├── __init__.py
        │   │   └── 0001_initial.py
        │   └── tests/
        │       └── test_*.py
        ├── nginx/
        │   └── nginx.conf
        ├── static/
        └── media/
```
---

## Key Decisions

**Role-based access**
`CheckIsClient` and `CheckIsFreelancer` permission classes applied
per-view — role violations return 403 immediately; enforced across
6 restricted endpoints.

**Offer scoping**
`OfferUpdateAPIView.get_queryset()` filters by `freelancer=request.user`
— freelancers can only edit their own offers; foreign offers return 404.

**Single profile URL**
`/users/me/` handles GET and PUT via one ViewSet mapped to
`{'get': 'list', 'put': 'update'}` — queryset filtered to
`id=request.user.id`; touching other profiles is impossible.

**Unique offer constraint**
`UniqueConstraint(fields=['project', 'freelancer'])` at DB level —
one freelancer can submit only one offer per project.

---
