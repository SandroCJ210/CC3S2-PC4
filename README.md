# CC3S2-PC4

Se usó un repositorio aparte para probar este proyecto, se añadió ese repositorio como el submódulo "aux-repo".

## Scripts

### `changelog_generator.py`

Script principal para parsear commits de un repositorio Git. Se priorizan los commits convencionales, considerando cualquier otro commit en la categoría "otro". La salida es almacenada como un archivo JSON con los commits ordenados desde el más antiguo al más reciente. Además, el script genera automáticamente un archivo CHANGELOG.md con los commits agrupados por tipo (feat, fix, etc.), calcula la siguiente versión siguiendo el versionado semántico (MAJOR.MINOR.PATCH) según los cambios detectados desde el último tag y crea un nuevo tag Git local con la versión correspondiente.

#### Uso

```
python changelog_generator.py [-d RUTA_REPOSITORIO] [-o ARCHIVO_SALIDA]
```

* `-d`, `--dir` especifica el directorio en donde se encuentra el repositorio Git. Por defecto se toma el directorio actual.
* `-o`, `--out` especifica el archivo en el que guardar la salida del script. Por defecto guarda la salida en `parsed_commits.json`.

#### Dependencias

El script depende de la librería `GitPython` para analizar los repositorios sin depender de llamadas directas al comando Git.
### Git Hooks

Ejecuta el siguiente script para instalar los hooks en tu entorno local
```bash
bash setup-hooks.sh
```
Este script configura automáticamente dos hooks personalizados:

- pre-commit: se ejecuta antes de que un commit se registre, para validar el formato del mensaje.

- pre-push: se ejecuta antes de hacer un git push y revisa que todos los commits pendientes por subir cumplan con el formato.