FROM python:3.12.3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && \
    pip install --upgrade pip "poetry == 1.8.2"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install


COPY src/ src/
COPY .env .

