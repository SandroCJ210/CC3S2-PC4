# CC3S2-PC4

## Scripts

### `changelog_generator.py`

Script principal para parsear commits de un repositorio Git. Se priorizan los commits convencionales, considerando cualquier otro commit en la categoría "otro". La salida es almacenada como un archivo JSON con los commits ordenados desde el más antiguo al más reciente.

#### Uso

```
python changelog_generator.py [-d RUTA_REPOSITORIO] [-o ARCHIVO_SALIDA]
```

* `-d`, `--dir` especifica el directorio en donde se encuentra el repositorio Git. Por defecto se toma el directorio actual.
* `-o`, `--out` especifica el archivo en el que guardar la salida del script. Por defecto guarda la salida en `parsed_commits.json`.

#### Dependencias

El script depende de la librería `GitPython` para analizar los repositorios sin depender de llamadas directas al comando Git.
