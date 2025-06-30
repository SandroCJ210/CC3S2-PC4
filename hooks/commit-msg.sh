#!/bin/sh

# commit-msg: valida que el mensaje del commit siga el formato de Conventional Commits antes de registrarlo localmente. Si no cumple, el commit se cancela.

# guardar la ruta del archivo temporal donde git guarda el mensaje del commit actual
commit_msg_file="$1"

# leer el contenido del mensaje
commit_msg=$(cat "$commit_msg_file")

# expresión regular que define un mensaje válido
# tipo(scope opcional): descripción
pattern="^(feat|fix|chore|docs|refactor|test|style|perf|ci|build|revert)(!)?(\([^)]+\))?: .+"

# validar que el mensaje cumpla con el formato
if ! echo "$commit_msg" | grep -Eq "$pattern"; then
  echo "Formato de commit inválido"
  echo "Usar el formato válido: tipo(scope opcional): descripción"
  echo "Referencia: https://www.conventionalcommits.org/en/v1.0.0/"
  exit 1
fi

echo "Formato de commit válido"
exit 0
