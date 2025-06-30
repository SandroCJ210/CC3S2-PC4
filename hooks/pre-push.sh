#!/bin/sh

# pre-push: revisa que todos los commits pendientes por subir al remoto tengan un formato válido. Si encuentra errores, se impide el push.

# obtener el nombre de la rama actual
branch=$(git rev-parse --abbrev-ref HEAD)

# obtener los mensajes de commits que aún no han sido enviados al remoto
commits=$(git log origin/$branch..HEAD --pretty=format:"%s")

# expresión regular que define un mensaje válido
# tipo(scope opcional): descripción
pattern="^(feat|fix|chore|docs|refactor|test|style|perf|ci|build|revert)(!)?(\([^)]+\))?: .+"

# filtrar mensajes que no cumplen con el formato esperado
invalids=$(echo "$commits" | grep -Ev "$pattern")

# impedir el push si existen commits inválidos
if [ -n "$invalids" ]; then
  echo "Existen commits pendientes con formato inválido:"
  echo "$invalids"
  echo "Referencia: https://www.conventionalcommits.org/en/v1.0.0/"
  exit 1
fi

echo "Todos los commits pendientes tienen formato válido"
exit 0
