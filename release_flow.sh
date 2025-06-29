#!/bin/bash

# release_flow.sh
# Flujo de liberación local: changelog + versión + creación de tag + push

set -e  

REPO_DIR="."
SCRIPT="scripts/changelog_generator.py"

echo "Generando CHANGELOG y calculando la siguiente versión del proyecto"
output=$(python "$SCRIPT" -d "$REPO_DIR") || {
    echo "Error al ejecutar $SCRIPT"
    exit 1
}

# Extraer la versión generada
version=$(echo "$output" | grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' | tail -1)

if [[ -z "$version" ]]; then
    echo "No se detectó una versión válida desde el script"
    exit 1
fi

# Validar que CHANGELOG.md existe
if [[ ! -f "CHANGELOG.md" ]]; then
    echo "No se encontró el archivo CHANGELOG.md"
    exit 1
fi

# Verificar si hay commits nuevos
if echo "$output" | grep -q "No se encontraron commits nuevos"; then
    echo "No hay commits nuevos desde el último tag. No se generará changelog ni se actualizará el tag."
    exit 0
fi

# Verificar si la nueva versión es igual al último tag
ultimo_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [[ "$version" == "$ultimo_tag" ]]; then
    echo "Se detectaron nuevos commits, pero no afectan la versión semántica ($version)"
    read -p "¿Deseas reetiquetar '$version' al nuevo commit? [y/N]: " retag
    if [[ "$retag" =~ ^[Yy]$ ]]; then
        git tag -d "$version"
        git tag "$version"
        echo "Tag '$version' actualizado localmente para apuntar al último commit."

        if git ls-remote --tags origin | grep -q "refs/tags/$version"; then
            read -p "El tag ya existe en remoto. ¿Deseas forzar el push? [y/N]: " force_push
            if [[ "$force_push" =~ ^[Yy]$ ]]; then
                git push --force origin "$version"
                echo "Tag actualizado y forzado en remoto."
            else
                echo "Push cancelado por el usuario."
            fi
        else
            git push origin "$version"
            echo "Tag nuevo enviado al remoto."
        fi
    else
        echo "Tag no actualizado."
    fi
    exit 0
fi

echo ""
echo "Vista previa del nuevo CHANGELOG.md:"
echo "----------------------------------------"
tail -n 20 CHANGELOG.md
echo "----------------------------------------"
echo ""
echo "Versión sugerida por el script: $version"
echo ""

# Confirmación del usuario
read -p "¿Deseas continuar y pushear el tag '$version'? [y/N]: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Operación cancelada por el usuario."
    exit 0
fi

# Verificar si el tag existe localmente
if git rev-parse "$version" >/dev/null 2>&1; then
    echo "El tag '$version' existe localmente."
else
    echo "El tag '$version' no existe localmente. Verifica si fue creado correctamente por el script."
    exit 1
fi

# Verificar si ya está en el remoto
if git ls-remote --tags origin | grep -q "refs/tags/$version"; then
    echo "El tag '$version' ya existe en el repositorio remoto."
    read -p "¿Deseas forzar el push del tag local para que apunte al último commit? [y/N]: " force_push
    if [[ "$force_push" != "y" && "$force_push" != "Y" ]]; then
        echo "Push cancelado por el usuario."
        exit 0
    fi
    git push --force origin "$version"
else
    git push origin "$version"
fi

echo "Tag '$version' enviado al repositorio remoto exitosamente."

exit 0
