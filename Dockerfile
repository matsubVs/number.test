FROM --platform=linux/amd64 python:3.10.4-bullseye

LABEL maintainer="matsubus@mail.ru"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry

WORKDIR /g_sheets/

COPY poetry.lock pyproject.toml /g_sheets/

RUN poetry install

COPY . /g_sheets/