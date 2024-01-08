# Admin Panel
---
## 1. Подготовка проекта
### Настроить переменные среды
#### ***Внимание! Это тестовые данные!***
#### Django
SECRET_KEY=```Your django key```

DB_NAME=movies_database<br/>
DB_USER=postgres<br/>
DB_PASSWORD=postgres<br/>
DB_HOST=db<br/>
DB_PORT=5432<br/>

DEBUG=False

#### SQLite
SQLITE=db.sqlite

#### PostgreSQL
POSTGRES_DB=movies_database<br/>
POSTGRES_USER=postgres<br/>
POSTGRES_PASSWORD=postgres<br/>
PGPORT=5432<br/>

#### Redis
REDIS_HOST=redis_state<br/>
REDIS_PORT=6379<br/>

#### Elasticsearch
ELASTIC_HTTP=http<br/>
ELASTIC_HOST=elasticsearch<br/>
ELASTIC_PORT=9200<br/>

### 2. Сборка и запуск проекта
```docker compose up --build```













