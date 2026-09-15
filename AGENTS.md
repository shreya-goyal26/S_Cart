# AGENTS.md

## Project overview
- This workspace is a small Django project named S_Cart with two apps: blog and shop.
- The main project settings live in S_Cart/settings.py and the root URL configuration is in S_Cart/urls.py.

## Working conventions
- Prefer app-level organization: keep new logic in the relevant app folder (for example blog/views.py or shop/views.py) rather than adding everything in the project root.
- Follow Django’s default structure: models.py, views.py, urls.py, and templates/<app>/... for each app.
- Keep changes small and consistent with the existing starter-style code.

## Common commands
- Run the development server: `python manage.py runserver`
- Create and apply migrations: `python manage.py makemigrations` and `python manage.py migrate`
- Run tests: `python manage.py test`
- Check project health: `python manage.py check`

## When editing the project
- Preserve the current Django setup and avoid introducing extra dependencies unless explicitly requested.
- If adding a new app, update INSTALLED_APPS and connect its URLs from the root URL config.
- Use simple view functions and URL patterns that fit the existing style.
