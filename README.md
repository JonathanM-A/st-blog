# ST Blog API

This Django-driven REST API provides user registration, authentication, post management, and password reset flows via `dj-rest-auth`, `django-allauth`, and JWT (`djangorestframework-simplejwt`).

## Features

- User registration with email-based authentication (no username)
- Login/logout and token refresh (JWT)
- Password reset and password change
- Post listing, creation, update, delete (in `apps.posts`)
- Swagger (`drf_yasg`) and Redoc API docs
- Django Debug Toolbar in development

## Tech stack

- Django 5.2+
- Django REST Framework
- dj-rest-auth
- django-allauth
- djangorestframework-simplejwt
- drf_yasg (Swagger/OpenAPI)
- PostgreSQL (default)

## Quick start

1. Clone repository

```bash
git clone https://github.com/JonathanM-A/st-blog.git st
cd st
```

2. Create and activate virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create `.env` file (or copy from sample)

```ini
DJANGO_SETTINGS_MODULE=config.settings.base
DEBUG=True
SECRET_KEY="your-secret"
ALLOWED_HOSTS=127.0.0.1,localhost
DB_HOST=localhost
DB_USER=postgres
DB_PORT=5432
DB_PASSWORD=yourpassword
DB_NAME=blog
```

5. Run migrations

```bash
python3 manage.py migrate
```

6. Start server

```bash
python3 manage.py runserver
```

7. Go to API docs:

- Swagger: `http://127.0.0.1:8000/swagger/`
- Redoc: `http://127.0.0.1:8000/`

## API endpoints

### Auth

- `POST /auth/register/` – register new user
- `POST /auth/login/` – login (JWT pair)
- `POST /auth/logout/` – logout
- `POST /auth/token/refresh/` – refresh access token
- `POST /auth/password/change/` – change password
- `POST /auth/password/reset/` – request password reset
- `POST /auth/password/reset/confirm/<uidb64>/<token>/` – confirm password reset

### API

- `GET /api/v1/users/profile/` - view user profile details
- `PUT /api/v1/users/profile/` - edit user profile 

## Email testing in development

Base configuration uses:

```py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This prints reset links to the console so you can copy/paste them without SMTP.

## Project setup

1. Clone repository

```bash
git clone <repo-url> st
cd st
```

2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create `.env` from sample values and set secrets

5. Run database migrations

```bash
python3 manage.py migrate
```

6. Run locally

```bash
python3 manage.py runserver
```

## Project structure

- `apps/users/` - custom user model, auth serializers, profile endpoint.
- `apps/posts/` - post model, CRUD APIs (list/create/retrieve/update/delete).
- `config/` - project settings and root URL routes.
- `config/auth_urls.py` - auth routes with `dj-rest-auth` integrated.

## Useful commands

- `python3 manage.py check`
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`
- `python3 manage.py createsuperuser`

## Notes

- Ensure `.env` has correct DB credentials and `DJANGO_SETTINGS_MODULE` set.
- For production, replace console email backend with SMTP backend and secure settings in `config/settings/prod.py`.
