"""
changelog_generator.py

Script para parsear commits en un repositorio Git priorizando commits convencionales
a partir del último tag y guardar la información en formato JSON.

Uso:
    python changelog_generator.py [-d RUTA_REPOSITORIO] [-o ARCHIVO_SALIDA]

Parámetros:
    -d, --dir     Ruta al repositorio Git a analizar (por defecto: el directorio actual).
    -o, --out Ruta donde se guardará el archivo JSON generado (por defecto: parsed_commits.json).

Ejemplo:
    python changelog_generator.py -d ./mi_repositorio -o ./salidas/commits.json

Requiere:
    - Python 3.6+
    - GitPython

Autor:
    Diego Akira García Rojas - Akira-13
"""

import json
import re
import argparse
# Se utiliza la librería GitPython para interactuar con lso repositorios a través de una API.
# De esta forma se evita trabajar directamente con comandos git en subprocesos.
from git import Repo
from typing import Dict, List

# Regex para parsear mensajes convencionales de commits.
COMMIT_REGEX = r'^(feat|fix|chore|docs|refactor|test|style|perf|ci|build|revert)(\([^)]+\))?: .+'

def parse_commit_message(commit_msg: str, commit_hash: str) -> Dict:
    """
    Leer mensaje de commit convencional.

    Argumentos
    ----------
    commit_msg
      Mensaje de commit a analizar
    commit_hash
      Hash del commit

    Retorna
    -------
    Dict
      Diccionario con la información del commit
    """
    lines = commit_msg.strip().split("\n")
    header = lines[0]
    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else None

    match = re.match(COMMIT_REGEX, header)

    if match:
        tipo = match.group(1)
        escopo = match.group(2)[1:-1] if match.group(2) else None
        descripcion = match.group(3)
    else:
        tipo = "otro"
        escopo = None
        descripcion = header

    return {
        "commit": commit_hash,
        "mensaje": {
            "tipo": tipo,
            "escopo": escopo,
            "descripcion": descripcion,
            "cuerpo": body or None
        }
    }

def get_commits_since_last_tag(repo_path=".") -> List[Dict]:
    """
    Leer commits desde el último tag del repositorio

    Argumentos
    ----------
    repo_path
      Ruta relativa del repositorio a analizar

    Retorna
    -------
    Lista de diccionarios
       Lista de diccionarios con información de commits
    """
    repo = Repo(repo_path)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    if not tags:
        raise ValueError("No se encontraron tags en el repositorio.")

    last_tag = tags[-1]
    commits = list(repo.iter_commits(f"{last_tag}..HEAD"))

    print(f"Se encontraron {len(commits)} commits desde el último tag: {last_tag}")

    parsed_commits = []
    for commit in reversed(commits): # antiguo a reciente
        parsed = parse_commit_message(commit.message, commit.hexsha)
        parsed_commits.append(parsed)

    return parsed_commits

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parsea commits desde el último tag en un repositorio Git.",
                                     "\nAlmacena los commits parseados en parsed_commits.json")
    # Argumentos
    parser.add_argument(
        "-d", "--dir",
        type=str,
        default=".",
        help="Ruta al repositorio Git (por defecto: directorio actual '.')"
    )
    parser.add_argument(
        "-o", "--out",
        type=str,
        default="parsed_commits.json",
        help="Ruta del archivo de salida (por defecto: parsed_commits.json)"
    )

    args = parser.parse_args()

    # Lectura de commits
    parsed_commits = get_commits_since_last_tag(args.dir)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(parsed_commits, f, indent=2, ensure_ascii=False)
    print("Commits parseados guardados en 'parsed_commits.json'")
