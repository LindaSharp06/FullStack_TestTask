## Что было сделано

### Бэкенд

Монолитная структура из двух файлов разбита на слои:

| Файл | Ответственность |
|---|---|
| `database.py` | Единый engine и session factory |
| `repository.py` | Все запросы к БД (FileRepository, AlertRepository) |
| `storage.py` | Файловый ввод-вывод |
| `service.py` | Оркестрация: вызывает репозиторий и storage |
| `tasks.py` | Только Celery-задачи |
| `app.py` | Только HTTP-маршруты |

Исправленные баги:
- Дублирование `engine`/`async_session_maker` в `service.py` и `tasks.py` — теперь оба используют `database.py`
- Небезопасный глобальный event loop в Celery-воркерах заменён на `asyncio.run()` для каждой задачи
- Отсутствующее поле `stored_name` в схеме `FileItem` — эндпоинт скачивания зависел от него, но оно не сериализовалось

### Фронтенд

Монолитный `page.tsx` разбит на слои:

```
lib/types.ts          — типы FileItem, AlertItem
lib/utils.ts          — formatDate, formatSize, getLevelVariant, getProcessingVariant
lib/api.ts            — все fetch-вызовы, BASE_URL из переменной окружения
components/
  FileTable.tsx        — таблица файлов
  AlertTable.tsx       — таблица алертов
  UploadModal.tsx      — форма загрузки со своим состоянием
app/page.tsx           — только layout и загрузка данных
```

Захардкоженный `http://localhost:8000` в трёх местах заменён на переменную окружения `NEXT_PUBLIC_API_URL`.
