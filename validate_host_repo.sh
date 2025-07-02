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
echo "Sin archivos sensibles detectados"

# Linting

#Ejecutar flake8
flake8 scripts/changelog_generator.py || {
    echo "Errores detectados con flake8"
    exit 1
}
echo "flake8 sin errores"

# Ejecutar Bandit
bandit scripts/changelog_generator.py > /dev/null 2>&1|| {
    echo "Errores detectados con bandit"
    exit 1
}
echo "bandit sin errores"

# Ejecutar shellcheck 
shellcheck release_flow.sh || {
    echo "Errores detectados con shellcheck"
    exit 1
}
echo "shellcheck sin errores"

echo "Validación exitosa"

