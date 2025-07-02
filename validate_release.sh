#!/bin/bash

#Detener ante cualquier error
set -e

#Seguridad

# Detectar archivos sensibles
sensitive_files=$(find . -type f \( -name ".env" -o -name ".key" -o -name "secrets.*" \))
if [[ -n "$sensitive_files" ]]; then
    echo "Se encontraron archivos sensibles:"
    echo "$sensitive_files"
fi

# Linting

#Ejecutar flake8
flake8 scripts/changelog_generator.py || echo "Errores detectados con flake8"
# Ejecutar Bandit
bandit scripts/changelog_generator.py || echo "Errores detectados con bandit"

# Ejecutar shellcheck
shellcheck release_flow.sh || echo "Errores detectados con shellcheck"

#Compliance

#Validar formato del último commit
last_msg=$(git log -1 --pretty=format:"%s")
pattern="^(feat|fix|chore|docs|refactor|test|style|perf|ci|build|revert)(!)?(\([^)]+\))?: .+"

if ! [[ "$last_msg" =~ $pattern ]]; then
    echo "El último commit no cumple con el formato convencional"
    echo "$last_msg"
fi

#Validar existencia de CHANGELOG.md
if [[ ! -f "CHANGELOG.md" ]]; then
    echo "No se encontró el archivo CHANGELOG.md"
fi

#Verificar que el último tag es semántico
last_tag= $(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [[ ! "$last_tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "El último tag $last_tag no cumple con el formato semántico (vX.Y.Z)"
fi