#!/bin/bash

#Detener ante cualquier error
set -e

#Validar formato del último commit
last_msg=$(git log -1 --pretty=format:"%s")
pattern="^(feat|fix|chore|docs|refactor|test|style|perf|ci|build|revert)(!)?(\([^)]+\))?: .+"

if ! [[ "$last_msg" =~ $pattern ]]; then
    echo "El último commit no cumple con el formato convencional"
    echo "$last_msg"
    echo 1
fi
echo "El último commit cumple con el formato"

#Validar existencia de CHANGELOG.md
if [[ ! -f "CHANGELOG.md" ]]; then
    echo "No se encontró el archivo CHANGELOG.md"
    exit 1
fi
echo "Archivo CHANGELOG.md encotrado"

#Verificar que el último tag es semántico
last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
if [[ ! "$last_tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "El último tag $last_tag no cumple con el formato semántico (vX.Y.Z)"
    exit 1
fi
echo "Tag semántico válido"