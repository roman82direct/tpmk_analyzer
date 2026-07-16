# tpmk_analyzer_backend

## Основные слои

### 1. API слой
Отвечает за:
- прием файлов;
- создание задач обработки;
- получение статусов;
- выдачу результатов;
- работу с данными для UI.

### 2. Service layer
Отвечает за:
- чтение Excel;
- нормализацию данных;
- бизнес-валидацию;
- формирование итоговых датафреймов;
- подготовку данных для отчетов.

### 3. Worker layer
Отвечает за:
- выполнение тяжелых операций;
- запись данных в PostgreSQL;
- генерацию XLSX;
- подготовку данных для графиков и BI-отчетов.

### 4. Data layer
Отвечает за:
- raw-данные;
- staging-данные;
- analytics-данные;
- историю обработок;
- метаданные файлов и задач.

## Структура проекта

```text
tpmk_analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── migrations/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── excel/
│   │   │   ├── analytics/
│   │   │   └── reports/
│   │   ├── workers/
│   │   │   ├── jobs.py
│   │   │   └── processor.py
│   │   ├── repositories/
│   │   │   ├── upload_repo.py
│   │   │   ├── job_repo.py
│   │   │   └── report_repo.py
│   │   └── utils/
│   │       ├── file_storage.py
│   │       └── excel_helpers.py
│   ├── tests/
│   ├── pyproject.toml
│   └── README.md
├── frontend/
│   ├── streamlit_app.py
│   ├── pages/
│   ├── components/
│   ├── assets/
│   └── README.md
├── storage/
│   ├── input/
│   ├── output/
├── docker/
├── docker-compose.yml
└── README.md
```