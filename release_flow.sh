#!/bin/bash

# release_flow.sh - Script para orquestar un flujo de liberación local
# Autor: Ariana Camila Lopez Julcarima - aclj20

set -e  

# Ruta al repositorio y script principal
REPO_DIR="."
SCRIPT="scripts/changelog_generator.py"

# Ejecutar el script Python para generar el changelog y la versión
echo "Generando CHANGELOG y calculando la siguiente versión del proyecto"
output=$(python "$SCRIPT" -d "$REPO_DIR") || {
    echo "Error al ejecutar $SCRIPT"
    exit 1
}

# Extraer la versión generada
version=$(echo "$output" | grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' | tail -1)

# Verificar si se obtuvo una versión válida
if [[ -z "$version" ]]; then
    echo "No se detectó una versión válida desde el script"
    exit 1
fi

# Validar que CHANGELOG.md fue generado
if [[ ! -f "CHANGELOG.md" ]]; then
    echo "No se encontró el archivo CHANGELOG.md"
    exit 1
fi

# Verificar si hay commits nuevos
if echo "$output" | grep -q "No se encontraron commits nuevos"; then
    echo "No hay commits nuevos desde el último tag. No se generará changelog ni se actualizará el tag."
    exit 0
fi

# Obtener el último tag del repositorio
ultimo_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")


# Si la nueva versión es igual al último tag, permitir reetiquetar
if [[ "$version" == "$ultimo_tag" ]]; then
    echo "Se detectaron nuevos commits, pero no afectan la versión semántica ($version)"
    read -p "¿Deseas reetiquetar '$version' al nuevo commit? [y/N]: " retag
    if [[ "$retag" =~ ^[Yy]$ ]]; then
        # Reemplazar el tag local por uno apuntando al nuevo commit
        git tag -d "$version"
        git tag "$version"
        echo "Tag '$version' actualizado localmente para apuntar al último commit."

        # Verificar si el tag ya existe en el remoto
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

# Mostrar vista previa del changelog generado
echo ""
echo "Vista previa del nuevo CHANGELOG.md:"
echo "----------------------------------------"
tail -n 20 CHANGELOG.md
echo "----------------------------------------"
echo ""
echo "Versión sugerida por el script: $version"
echo ""

# Confirmar si se desea hacer push del tag
read -p "¿Deseas continuar y pushear el tag '$version'? [y/N]: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Operación cancelada por el usuario."
    exit 0
fi

# Crear el tag localmente
git tag "$version"

# Verificar si el tag existe localmente
if git rev-parse "$version" >/dev/null 2>&1; then
    echo "El tag '$version' existe localmente."
else
    echo "El tag '$version' no existe localmente. Verifica si fue creado correctamente por el script."
    exit 1
fi

# Verificar si el tag existe en el remoto
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
