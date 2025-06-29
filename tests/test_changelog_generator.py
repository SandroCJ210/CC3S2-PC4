from scripts import changelog_generator as cg
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
            "Agregar caracteristica importante."
        )
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
    repo_path = temp_git_repo["repo_path"]
    expected = temp_git_repo["expected_commits"]

    commits = cg.get_commits_since_last_tag(str(repo_path))

    assert len(commits) == len(expected)

    actual = {(c["commit"], c["mensaje"]["tipo"], c["mensaje"]["descripcion"]) for c in commits}
    esperado = {(e["commit"], e["tipo"], e["descripcion"]) for e in expected}

    assert actual == esperado

def test_repo_no_tags(temp_git_repo_no_tags):
    """
    Probar que se lance error cuando no se encuentran tags en el repositorio.
    """
    repo_path = temp_git_repo_no_tags
    with pytest.raises(ValueError, match="tags"):
        commits = cg.get_commits_since_last_tag(str(repo_path))
