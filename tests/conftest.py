import pytest
from git import Repo
from pathlib import Path
import tempfile


@pytest.fixture
def temp_git_repo() -> dict:
    """
    Crea un repositorio Git con un tag inicial y commits, incluyendo un BREAKING CHANGE.
    Devuelve:
        - ruta del repo,
        - lista de commits esperados,
        - estructura de changelog esperada.
    """
    tmp_dir = Path(tempfile.mkdtemp())
    repo = Repo.init(tmp_dir)
    file = tmp_dir / "archivo.txt"

    commits_info = []
    changelog_info = {"Features": [], "Bug Fixes": [], "Breaking Changes": []}
    next_version = "v2.0.0"

    # Commit 1 - inicial con tag
    file.write_text("Inicial")
    repo.index.add([str(file)])
    repo.index.commit("chore: inicial")
    repo.create_tag("v1.0.0")

    # Commit 2 - feat
    file.write_text("Funcionalidad nueva")
    repo.index.add([str(file)])
    commit_feat = repo.index.commit("feat(core): agregar endpoint de usuario")
    commits_info.append(
        {
            "commit": commit_feat.hexsha,
            "tipo": "feat",
            "descripcion": "agregar endpoint de usuario",
        }
    )
    changelog_info["Features"].append("agregar endpoint de usuario")

    # Commit 3 - fix
    file.write_text("Arreglo crítico")
    repo.index.add([str(file)])
    commit_fix = repo.index.commit("fix: corregir fallo en autenticación")
    commits_info.append(
        {
            "commit": commit_fix.hexsha,
            "tipo": "fix",
            "descripcion": "corregir fallo en autenticación",
        }
    )
    changelog_info["Bug Fixes"].append("corregir fallo en autenticación")

    # Commit 4 - BREAKING CHANGE
    file.write_text("Cambio mayor")
    repo.index.add([str(file)])
    commit_break = repo.index.commit(
        "feat!(core): eliminar API obsoleta\n\nSe elimina soporte legacy."
    )
    commits_info.append(
        {
            "commit": commit_break.hexsha,
            "tipo": "BREAKING CHANGE",
            "descripcion": "eliminar API obsoleta",
        }
    )
    changelog_info["Breaking Changes"].append("eliminar API obsoleta")

    return {
        "repo_path": tmp_dir,
        "expected_commits": commits_info,
        "expected_changelog": changelog_info,
        "expected_version": next_version,
    }


@pytest.fixture
def temp_git_repo_no_tags(tmp_path) -> Path:
    repo_path = tmp_path / "repo_sin_tags"
    repo = Repo.init(repo_path)

    file = repo_path / "README.md"
    file.write_text("Sin tags")
    repo.index.add([str(file)])
    repo.index.commit("feat: repo sin tags")

    return repo_path


# Fixtures para probar lógica de generación de tags
@pytest.fixture
def commits_fix_only():
    return {
        "commits": [
            {"mensaje": {"tipo": "fix", "descripcion": "arreglar error 1"}},
            {"mensaje": {"tipo": "fix", "descripcion": "arreglar error 2"}},
        ],
        "tag": "v1.2.3",
        "esperado": "v1.2.4",
    }


@pytest.fixture
def commits_with_feat():
    return {
        "commits": [
            {"mensaje": {"tipo": "fix", "descripcion": "arreglar error"}},
            {"mensaje": {"tipo": "feat", "descripcion": "agregar funcionalidad"}},
        ],
        "tag": "v1.2.3",
        "esperado": "v1.3.0",
    }


@pytest.fixture
def commits_breaking_change():
    return {
        "commits": [
            {
                "mensaje": {
                    "tipo": "BREAKING CHANGE",
                    "descripcion": "realizar cambio crítico",
                }
            },
            {"mensaje": {"tipo": "feat", "descripcion": "agregar funcionalidad"}},
        ],
        "tag": "v1.2.3",
        "esperado": "v2.0.0",
    }


# Fixture para probar lógica de generación de commits
@pytest.fixture
def changelog_commits():
    return {
        "commits": [
            {"mensaje": {"tipo": "feat", "descripcion": "añadir funcionalidad"}},
            {"mensaje": {"tipo": "fix", "descripcion": "arreglar error"}},
            {
                "mensaje": {
                    "tipo": "BREAKING CHANGE",
                    "descripcion": "cambio importante",
                }
            },
            {"mensaje": {"tipo": "docs", "descripcion": "actualizar documentación"}},
        ],
        "version": "v1.5.0",
        "esperado": {
            "Features": ["añadir funcionalidad"],
            "Bug Fixes": ["arreglar error"],
            "Breaking Changes": ["cambio importante"],
            "Documentation": ["actualizar documentación"],
        },
    }
