import subprocess

import pytest


def test_all_tests_execution():
    """Test 1 : Vérification de l'exécution de tous les tests.

    Vérifie que l'ensemble des tests des parties 1 à 4 s'exécute correctement.
    """
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    assert result.returncode == 0


def test_code_coverage():
    """Test 2 : Vérification de la couverture de code.

    Vérifie que la couverture obtenue avec coverage est suffisante
    (>= 85% selon les normes de SonarQube)
    et que les parties importantes du projet sont couvertes par les tests.
    """
    cov_result = subprocess.run(
        ["coverage", "run", "-m", "pytest"], capture_output=True, text=True
    )
    assert cov_result.returncode == 0
    report_result = subprocess.run(
        ["coverage", "report", "-m", "--fail-under=85"], capture_output=True, text=True
    )
    assert report_result.returncode == 0


def test_code_quality_linting():
    """Test 3 : Vérification du respect des règles de qualité du code.

    Vérifie que le projet respecte les règles définies avec ruff
    et qu'aucune erreur de linting n'est détectée.
    """
    result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)
    assert result.returncode == 0


def test_documentation_generation():
    """Test 4 : Vérification de la documentation.

    Vérifie que la documentation du projet peut être générée correctement avec pdoc3
    et qu'elle couvre les éléments importants du code.
    """
    result = subprocess.run(
        ["pdoc", "--html", "app", "--output-dir", "docs"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


@pytest.mark.parametrize(
    "make_target",
    [
        "test",
        "unit_test",
        "perf_test",
        "coverage",
        "lint",
        "doc",
    ],
)
def test_make_commands(make_target):
    """Test 5 : Vérification des commandes make du projet.

    Vérifie que les commandes test, unit_test, perf_test, coverage, lint et doc
    prévues par le sujet fonctionnent correctement.
    """
    result = subprocess.run(["make", make_target], capture_output=True, text=True)
    assert result.returncode == 0
