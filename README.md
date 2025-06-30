# CC3S2-PC4

Se usó un repositorio aparte para probar este proyecto, se añadió ese repositorio como el submódulo "aux-repo".

## Scripts
### `release_flow.sh`
Script principal que orquesta el flujo de liberación local del proyecto. Ejecuta automáticamente el changelog_generator.py, muestra una vista previa del archivo CHANGELOG.md, detecta la nueva versión generada y permite al usuario confirmar si desea crear (o reetiquetar) y pushear el tag correspondiente al repositorio remoto.

#### Uso

```bash
bash release_flow.sh
```

### `changelog_generator.py`

Script para parsear commits de un repositorio Git. Se priorizan los commits convencionales, considerando cualquier otro commit en la categoría "otro". La salida es almacenada como un archivo JSON con los commits ordenados desde el más antiguo al más reciente. Además, el script genera automáticamente un archivo CHANGELOG.md con los commits agrupados por tipo (feat, fix, etc.), calcula la siguiente versión siguiendo el versionado semántico (MAJOR.MINOR.PATCH) según los cambios detectados desde el último tag y crea un nuevo tag Git local con la versión correspondiente.
También se calculan métricas de flujo usando los commits como referencia para saber el flujo de trabajo del equipo. Estas métricas son dos, throughput, que se calcula como el número de commits promedio por día, y task distribution, que es la proporción por cada tipo de trabajo o tarea realizada. Estos resultados son guardados en un documento metrics.json.

#### Uso

```
python changelog_generator.py [-d RUTA_REPOSITORIO] [-o ARCHIVO_SALIDA]
```

* `-d`, `--dir` especifica el directorio en donde se encuentra el repositorio Git. Por defecto se toma el directorio actual.
* `-o`, `--out` especifica el archivo en el que guardar la salida del script. Por defecto guarda la salida en `parsed_commits.json`.

#### Dependencias

El script depende de la librería `GitPython` para analizar los repositorios sin depender de llamadas directas al comando Git.

## Git Hooks

Ejecuta el siguiente script para instalar los hooks en tu entorno local
```bash
bash setup-hooks.sh
```
Este script configura automáticamente dos hooks personalizados:

- pre-commit: se ejecuta antes de que un commit se registre, para validar el formato del mensaje.

- pre-push: se ejecuta antes de hacer un git push y revisa que todos los commits pendientes por subir cumplan con el formato.

## Tests

Para ejecutar los tests de este repositorio, solo es necesario ejecutar `pytest` en la raíz del proyecto.

### 1. `test_parse_commits`

* **Tipo**: Unitario, parametrizado.
* **Propósito**: Verifica el correcto parseo de mensajes de commit según la convención Conventional Commits.

### 2. `test_get_commits`

* **Tipo**: Integración con fixture `temp_git_repo_basic`
* **Propósito**: Asegura que se obtienen correctamente los commits realizados después del último tag en el repositorio temporal.

### 3. `test_repo_no_tags`

* **Tipo**: Integración con fixture `temp_git_repo_no_tags`
* **Propósito**: Verifica que se lanza un `ValueError` si el repositorio no tiene ningún tag.

### 4. `test_repo_create_tag`

* **Tipo**: Integración con fixture `temp_git_repo_no_tags`
* **Propósito**: Comprueba que `crear_tag(...)` añade correctamente un nuevo tag al repositorio Git.

### 5. `test_calcular_siguiente_version`

* **Tipo**: Unitario, parametrizado por fixture
* **Fixtures utilizados**: `commits_fix_only`, `commits_with_feat`, `commits_breaking_change`
* **Propósito**: Valida que `calcular_siguiente_version(...)` produce la versión semántica correcta (patch, minor o major) en función de los tipos de commits.
* **Casos cubiertos**:

  * Solo fixes → incremento de parche.
  * Fixes + feat → incremento menor.
  * BREAKING CHANGE → incremento mayor.

### 6. `test_generar_changelog_md`

* **Tipo**: Unitario, parametrizado con fixture.
* **Propósito**: Verifica que la función `generar_changelog_md(...)` cree correctamente un archivo `CHANGELOG.md` estructurado y con contenido esperable.
* **Fixture usado**: `changelog_commits`, que define:

  * una lista de commits parseados,
  * la versión del release simulada,
  * y una estructura esperada de secciones con sus entradas.

### 7. `test_release_flow`

* **Tipo**: Integración.
* **Propósito**: Simula el flujo completo de una liberación:

  1. Obtiene los commits desde el último tag.
  2. Calcula la nueva versión semántica con base en los tipos de commit.
  3. Genera un archivo `CHANGELOG.md` con el contenido agrupado.
  4. Crea un nuevo tag Git con la versión calculada.
* **Fixture usado**: `temp_git_repo`, que proporciona:

  * el repositorio Git temporal,
  * los commits esperados,
  * el contenido esperado del changelog,
  * la versión esperada (`expected_version`).
