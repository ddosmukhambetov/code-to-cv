FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /src

RUN apt-get update && apt-get install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry

ADD pyproject.toml /src

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

COPY . /src
