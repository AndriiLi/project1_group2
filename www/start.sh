#!/bin/bash


if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "Ни 'docker compose', ни 'docker-compose' не найдены. Установите Docker Compose."
    exit 1
fi


$DOCKER_COMPOSE_CMD up -d



OS=$(uname)

if [ "$OS" = "Linux" ]; then
    echo "Запущено на Linux"
    xdg-open http://localhost:8501

elif [ "$OS" = "Darwin" ]; then
   open http://localhost:8501

elif [ "$OS" = "CYGWIN_NT" ] || [ "$OS" = "MINGW32_NT" ] || [ "$OS" = "MINGW64_NT" ]; then
    start http://localhost:8501

else
    echo "Неизвестная операционная система: $OS"
fi















xdg-open http://localhost:8080

# Если вы используете macOS, используйте:
# open http://localhost:8080

# Если Windows:
# start http://localhost:8080