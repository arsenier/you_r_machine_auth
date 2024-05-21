# syntax=docker/dockerfile:1

FROM python:3.10-alpine
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-interaction --no-ansi
COPY . .
EXPOSE 8000
CMD ["python3", "main.py"]