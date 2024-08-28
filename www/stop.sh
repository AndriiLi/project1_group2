#!/bin/bash


if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "Ни 'docker compose', ни 'docker-compose' не найдены. Установите Docker Compose."
    exit 1
fi

$DOCKER_COMPOSE_CMD down