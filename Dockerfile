FROM python:3.12.3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    pip install --upgrade pip "poetry == 2.1.3"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root


COPY src/ src/
COPY .env .

