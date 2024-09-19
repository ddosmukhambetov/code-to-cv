#!/bin/bash

alembic upgrade head

uvicorn app.main:app_factory --host 0.0.0.0 --port 8000 --factory --reload
