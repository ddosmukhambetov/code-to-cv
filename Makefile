DC = docker compose
EXEC = docker exec -it

ENV = --env-file .env

APP_FILE = docker_compose/app.yaml
DB_FILE = docker_compose/db.yaml

APP_CONTAINER = app
DB_CONTAINER = postgres

POSTGRES_USER = user # Change this to your user
POSTGRES_DB = code_to_cv_db # Change this to your database name

.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) $(ENV) down --remove-orphans

.PHONY: app-exec
app-exec:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY: app-make-migrations
app-make-migrations:
	$(EXEC) $(APP_CONTAINER) bash -c "alembic revision --autogenerate -m 'migration'"

.PHONY: app-migrate
app-migrate:
	$(EXEC) $(APP_CONTAINER) bash -c "alembic upgrade head"

.PHONY: app-downgrade-migrations
app-downgrade-migrations:
	$(EXEC) $(APP_CONTAINER) bash -c "alembic downgrade base"

.PHONY: app-create-superuser
app-create-superuser:
	$(EXEC) $(APP_CONTAINER) bash -c "python3 app/users/actions/create_superuser.py"

.PHONY: app-logs
app-logs:
	$(DC) -f $(APP_FILE) $(ENV) logs -f

.PHONY: db
db:
	$(DC) -f $(DB_FILE) $(ENV) up --build -d

.PHONY: db-down
db-down:
	$(DC) -f $(DB_FILE) $(ENV) down --remove-orphans

.PHONY: db-exec
db-exec:
	$(EXEC) $(DB_CONTAINER) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

.PHONY: db-logs
db-logs:
	$(DC) -f $(DB_FILE) $(ENV) logs -f

.PHONY: all
all:
	$(DC) -f $(APP_FILE) -f $(DB_FILE) $(ENV) up --build -d

.PHONY: all-down
all-down:
	$(DC) -f $(APP_FILE) -f $(DB_FILE) $(ENV) down --remove-orphans

.PHONY: all-logs
all-logs:
	$(DC) -f $(APP_FILE) -f $(DB_FILE) $(ENV) logs -f
