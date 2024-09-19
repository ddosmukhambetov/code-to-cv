FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code-to-cv

RUN apt-get update && apt-get install -y python3-dev \
    build-essential \
    gcc \
    musl-dev \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0

RUN pip install --upgrade pip
RUN pip install poetry

ADD pyproject.toml /code-to-cv

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

COPY . /code-to-cv
