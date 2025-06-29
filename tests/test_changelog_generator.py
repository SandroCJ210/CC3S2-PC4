from scripts import changelog_generator as cg
from git import Repo
import pytest


@pytest.mark.parametrize(
    "mensaje, tipo, escopo, descripcion, cuerpo",
    [
        (
            "feat(api): agregar caracteristica\n\nAgregar caracteristica importante.",
            "feat",
            "api",
            "agregar caracteristica",
            "Agregar caracteristica importante.",
        ),
        (
            "fix: arreglar error\n\nArreglar error fatal.",
            "fix",
            None,
            "arreglar error",
            "Arreglar error fatal.",
        ),
        ("commit inicial", "otro", None, "commit inicial", None),
        (
            "feat(api): agregar caracteristica\n\n\n\n\n",
            "feat",
            "api",
            "agregar caracteristica",
            None,
        ),
        (
            "feat!(break): agregar caracteristica\n\nAgregar caracteristica importante.",
            "BREAKING CHANGE",
            "break",
            "agregar caracteristica",
            "Agregar caracteristica importante.",
        ),
    ],
)
def test_parse_commits(mensaje, tipo, escopo, descripcion, cuerpo):
    """
    Probar funcionalidad de parseo de commits.
    Asegurar que regex y construcción de diccionario se cumplan.
    """
    result = cg.parse_commit_message(mensaje, "abc123")
    assert result["commit"] == "abc123"
    assert result["mensaje"]["tipo"] == tipo
    assert result["mensaje"]["escopo"] == escopo
    assert result["mensaje"]["descripcion"] == descripcion
    assert result["mensaje"]["cuerpo"] == cuerpo


def test_get_commits(temp_git_repo_basic):
    """
    Probar funcionalidad de obtención de commits en repositorio.
    """
    repo_path = temp_git_repo_basic["repo_path"]
    expected = temp_git_repo_basic["expected_commits"]

    commits = cg.get_commits_since_last_tag(str(repo_path))

    assert len(commits) == len(expected)

    actual = {
        (c["commit"], c["mensaje"]["tipo"], c["mensaje"]["descripcion"])
        for c in commits
    }
    esperado = {(e["commit"], e["tipo"], e["descripcion"]) for e in expected}

    assert actual == esperado


def test_repo_no_tags(temp_git_repo_no_tags):
    """
    Probar que se lance error cuando no se encuentran tags en el repositorio.
    """
    repo_path = temp_git_repo_no_tags
    with pytest.raises(ValueError, match="tags"):
        commits = cg.get_commits_since_last_tag(str(repo_path))

def test_repo_create_tag(temp_git_repo_no_tags):
    """
    Probar creación de tag de crear_tag en un repositorio.
    """
    repo_path = temp_git_repo_no_tags
    created_tag = "v1.0.0"
    cg.crear_tag(repo_path, created_tag)
    repo_tags = sorted(Repo(repo_path).tags, key=lambda t: t.commit.committed_datetime)
    assert repo_tags[-1].name == created_tag

# Utiliza los fixtures de conftest.py
# No se necesita probar toda la lógica de parseo de commits, por lo que crear
# un repositorio temporal no es necesario.
@pytest.mark.parametrize(
    "version_commits", ["commits_fix_only", "commits_with_feat", "commits_breaking_change"]
)
def test_calcular_siguiente_version(request, version_commits):
    """
    Probar funcionalidad de calculo de version siguiente.
    """
    datos = request.getfixturevalue(version_commits)
    commits = datos["commits"]
    tag = datos["tag"]
    esperado = datos["esperado"]

    resultado = cg.calcular_siguiente_version(commits, tag)
    assert (
        resultado == esperado
    ), f"{version_commits} esperado {esperado}, obtenido {resultado}"
