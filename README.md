# Med Platform Complete

## Запуск

```bash
cp .env.example .env
docker compose up --build
```

В окремому терміналі:

```bash
docker compose exec web python manage.py createsuperuser
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

