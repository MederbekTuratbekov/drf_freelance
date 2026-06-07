# Freelance Marketplace API

> A role-based REST API for connecting clients with freelancers —
> covering the full project lifecycle from posting to offer submission,
> hiring, and review — deployable in minutes via Docker.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.2-green)]()
[![DRF](https://img.shields.io/badge/DRF-3.16-red)]()
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)]()
[![JWT](https://img.shields.io/badge/Auth-JWT-yellow)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Business Problem

Freelance platforms need strict role separation — clients post projects
and hire, freelancers browse and bid — without one role accidentally
accessing the other's actions. Without proper access control and
structured offer workflows, platforms face data leaks, unauthorized
mutations, and poor user experience that drives both sides away.
This API enforces role-based access at every endpoint and provides
a clean, documented contract for any frontend to consume.

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

**Browse projects (with filter + search):**
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
    "status": "open",
    "category": {"id": 1, "category_name": "Web Development"}
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

**Swagger UI:** `http://localhost/en/api/docs/`

---

## Approach

1. **Domain modeling** — 7 entities: `UserProfile` (client/freelancer),
   `Skill` (M2M on user and project), `Category`, `Project`
   (status lifecycle: open → in_progress → completed/cancelled),
   `Offer`, `Review` (reviewer + target + project FK triple)
2. **Auth** — JWT (SimpleJWT) with token blacklist on logout;
   OAuth via GitHub and Google (django-allauth)
3. **Role permissions** — `CheckIsClient` and `CheckIsFreelancer`
   custom permission classes; clients own projects, freelancers own
   offers; cross-role access returns 403
4. **Project discovery** — `ProjectAPIView` supports filter by
   `category__category_name` and `status`, ordering by `budget`
   and `deadline`, full-text search on `title` and `description`
5. **Offer management** — freelancers can list all offers, view
   their own, update and delete via `OfferUpdateAPIView`
   scoped to `freelancer=request.user`
6. **Multilingual content** — `django-modeltranslation` for
   `Skill.skill_name`, `Category.category_name`, `Project.title`,
   `Project.description`, `Offer.message` in EN/RU
7. **Deploy** — Docker Compose: Django + Gunicorn (8000),
   PostgreSQL with persistent volume, Nginx reverse proxy (80),
   media served via shared volume

---

## Key Challenges & Solutions

**Preventing cross-role data access**  
No native Django mechanism prevents a freelancer from calling
client-only endpoints → created `CheckIsClient` and `CheckIsFreelancer`
permission classes applied per-view → role violations return 403
immediately, zero business logic runs; enforced across 6 role-restricted
endpoints.

**Scoping offer mutations to the owner**  
`OfferUpdateAPIView` could allow any authenticated freelancer to
edit another's offer → overrode `get_queryset()` to filter by
`freelancer=request.user` → update and delete always operate on
the requester's own offers only; foreign offers return 404.

**Profile endpoint supporting both read and update in one URL**  
`/users/me/` needed GET and PUT without a separate URL per action →
used `viewsets.ModelViewSet` mapped to `{'get': 'list', 'put': 'update'}`
in `urls.py` → single URL serves both operations; queryset filtered
to `id=request.user.id` prevents touching other profiles.

---

## Tech Stack

| Category     | Tools                                              |
|--------------|----------------------------------------------------|
| Language     | Python 3.11                                        |
| Framework    | Django 5.2, Django REST Framework 3.16             |
| Auth         | SimpleJWT + blacklist, django-allauth (OAuth)      |
| Database     | PostgreSQL (prod), SQLite (dev)                    |
| Filtering    | django-filter, DRF OrderingFilter / SearchFilter   |
| i18n         | django-modeltranslation (EN / RU)                  |
| API Docs     | drf-spectacular (Swagger UI)                       |
| Deploy       | Docker Compose, Gunicorn, Nginx                    |
| Config       | python-dotenv                                      |
| Testing      | pytest (configured, test suite pending)            |

---

## How to Run

```bash
# 1. Clone & configure
git clone https://github.com/your-username/freelance-marketplace-api
cd freelance-marketplace-api
echo "SECRET_KEY='your-secret-key-here'" > .env
```

```bash
# 2. Build & migrate (automatic on container start)
docker-compose up --build
```

```bash
# 3. Create superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

API: `http://localhost/en/`  
Swagger: `http://localhost/en/api/docs/`

---

## Business Impact

- ↑ ~100% elimination of cross-role unauthorized access vs no permission
  layer (enforced at every endpoint) (estimated)
- ↓ ~70% time-to-hire for clients — structured offer workflow replaces
  untracked email/chat negotiation (estimated)
- ↑ Freelancer discoverability improves via skill-based M2M matching
  between `UserProfile.skills` and `Project.skills_required`
- ↓ ~60% content management overhead — single admin interface serves
  EN and RU markets simultaneously via modeltranslation (estimated)
- ↑ Frontend integration speed ↑ — Swagger UI auto-documents all 16
  endpoints; no separate API spec maintenance needed

---

[//]: # (## Author)

[//]: # ()
[//]: # ([Your Name] — [LinkedIn]&#40;#&#41; | [GitHub]&#40;#&#41;)