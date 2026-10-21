# Med Platform

Веб-орієнтована інформаційна система електронної медичної карти з гібридною моделлю управління доступом (RBAC + ABAC). Репозиторій кваліфікаційної роботи бакалавра.

**Стек:** Python 3.12, Django 5.0, Django REST Framework, PostgreSQL 16, Gunicorn, Docker Compose, Nginx (опційно).

## Запуск через Docker

```bash
cp .env.example .env
# відредагуйте .env: задайте власні SECRET_KEY і DB_PASSWORD
docker compose up --build
```

Сайт: http://localhost:8000, адмінка: http://localhost:8000/admin/

Створити адміністратора (в окремому терміналі):

```bash
docker compose exec web python manage.py createsuperuser
```

### З Nginx

```bash
docker compose --profile nginx up --build
```

Сайт буде доступний на http://localhost (порт 80); Nginx віддає статику й медіафайли.

## Локальний запуск без Docker

Якщо в `.env` не задано `DB_HOST`, використовується SQLite (`db.sqlite3`, не потрапляє в Git).

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # приберіть рядок DB_HOST або залиште його порожнім
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Секрети

- Усі секрети (`SECRET_KEY`, `DB_PASSWORD`) задаються лише у файлі `.env`, який є в `.gitignore`.
- У репозиторії зберігається тільки шаблон `.env.example` без реальних значень.
- Згенерувати `SECRET_KEY`: `python -c "import secrets; print(secrets.token_urlsafe(50))"`.
- Перевірка на витік секретів: `gitleaks detect --source . -v`.

## Резервне копіювання

Сервіс `backup` раз на добу робить копію БД (`pg_dump`) у папку `./backups` і видаляє копії, старші за `BACKUP_KEEP_DAYS` днів.

```bash
# зробити копію вручну
docker compose exec backup sh /scripts/backup.sh

# перевірити відновлення останньої копії
docker compose exec backup sh /scripts/restore_check.sh

# відновити робочу БД з копії
docker compose exec backup pg_restore --clean --if-exists --no-owner -d med_platform /backups/<файл>.dump
```

## Що є

- реєстрація пацієнта
- логін і logout
- профіль пацієнта
- медична книга
- кабінет лікаря
- прив'язка пацієнта до лікаря через доступ
- створення лікарів і адміністрування через Django admin
- спеціальність лікаря як поле з вибором, а не окремий каталог

## Структура

```
apps/
  users/           користувачі та ролі (patient, doctor, admin)
  medical/         профілі, медичні записи, вкладення
  access_control/  доступ лікаря до карти пацієнта
  core/            головна сторінка, службові команди
config/            налаштування Django
nginx/             конфігурація Nginx
scripts/           резервне копіювання й перевірка відновлення
```
