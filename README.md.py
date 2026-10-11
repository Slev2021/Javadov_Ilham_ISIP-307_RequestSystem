## API

### Запуск

```bash
pip install -r requirements.txt
uvicorn src.api.app:app --reload --port 8000
Адрес: http://localhost:8000
Swagger UI: http://localhost:8000/docs
Метод	URL	Описание
GET	/api/requests	Список заявок с фильтрами
POST	/api/requests	Создать заявку
GET	/api/requests/{id}	Получить заявку
PUT	/api/requests/{id}	Обновить заявку
PATCH	/api/requests/{id}/status	Сменить статус
DELETE	/api/requests/{id}	Удалить заявку
Пример запроса
bash
curl -X POST http://localhost:8000/api/requests \
  -H "Content-Type: application/json" \
  -d '{"title":"Тест","author_id":1,"category_id":1,"priority_id":2}'
Формат ошибок
json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Поле 'title' обязательно",
    "details": {"field": "title"}
  }
}
## Шаг 12. Коммиты

```bash
# 1. Pydantic-схемы и валидация
git add src/api/schemas.py
git commit -m "feat(api): add request/response schemas with validation"

# 2. Обработка ошибок
git add src/api/errors.py
git commit -m "feat(api): add unified error handling with error codes"

# 3. Роуты API
git add src/api/routes.py src/api/app.py
git commit -m "feat(api): add REST endpoints for requests (CRUD, filters, status)"

# 4. Документация и README
git add docs/api/ README.md
git commit -m "docs(api): add Postman collection, examples and API section in README"

# 5. Слияние в develop
git checkout develop
git merge main
git push origin develop

https://github.com/Slev2021/Javadov_Ilham_ISIP-307_RequestSystem.git