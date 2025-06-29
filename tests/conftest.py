import pytest
from git import Repo
from pathlib import Path
import tempfile

@pytest.fixture
def temp_git_repo_basic() -> dict:
    """
    Crea un repo Git temporal con un tag y commits, y devuelve su metadata para validación.
    """

    tmp_dir = Path(tempfile.mkdtemp())
    repo = Repo.init(tmp_dir)
    file = tmp_dir / "archivo.txt"

    commits_info = []

    # Commit 1
    file.write_text("Inicial")
    repo.index.add([str(file)])
    commit1 = repo.index.commit("chore: inicial")
    repo.create_tag("v1.0.0")

    # Commit 2
    file.write_text("Funcionalidad")
    repo.index.add([str(file)])
    commit2 = repo.index.commit("feat(api): nueva ruta")
    commits_info.append({
        "commit": commit2.hexsha,
        "tipo": "feat",
        "descripcion": "nueva ruta"
    })

    # Commit 3
    file.write_text("Arreglo")
    repo.index.add([str(file)])
    commit3 = repo.index.commit("fix: corregir bug")
    commits_info.append({
        "commit": commit3.hexsha,
        "tipo": "fix",
        "descripcion": "corregir bug"
    })

    return {
        "repo_path": tmp_dir,
        "expected_commits": commits_info
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
