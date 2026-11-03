from time import perf_counter

import pytest


@pytest.mark.performance
@pytest.mark.parametrize(
    # utilisation du terme "budget", car il s'agit d'un terme utilisé en génie logiciel
    # pour les tests de performance
    "size, budget",
    [
        (10, 0.01),
        (100, 0.05),
        (1000, 0.2),
    ],
)
def test_triangulation_execution_time(size, budget):
    """Test 1 : Mesure du temps d'exécution de la triangulation.

    Vérifie le temps nécessaire pour trianguler des ensembles de points
    de tailles différentes.
    """
    points = generate_mock_points(size)
    start = perf_counter()
    compute_triangulation(points)
    elapsed = perf_counter() - start
    assert elapsed < budget


@pytest.mark.performance
@pytest.mark.parametrize(
    "size, budget",
    [
        (10, 0.005),
        (100, 0.02),
        (1000, 0.1),
    ],
)
def test_point_set_conversion_time(size, budget):
    """Test 2 : Mesure du temps de conversion des PointSet.

    Vérifie le temps nécessaire pour sérialiser et désérialiser des
    PointSet de tailles différentes.
    """
    points = generate_mock_points(size)
    start = perf_counter()
    binary = serialize_point_set(points)
    deserialize_point_set(binary)
    elapsed = perf_counter() - start
    assert elapsed < budget


@pytest.mark.performance
@pytest.mark.parametrize(
    "v_count, t_count, budget",
    [
        (10, 10, 0.005),
        (100, 150, 0.03),
        (1000, 1800, 0.15),
    ],
)
def test_triangles_conversion_time(v_count, t_count, budget):
    """Test 3 : Mesure du temps de conversion des Triangles.

    Vérifie le temps nécessaire pour sérialiser et désérialiser des Triangles
    contenant un nombre différent de sommets et de triangles.
    """
    vertices, triangles = generate_mock_triangles(v_count, t_count)
    start = perf_counter()
    binary = serialize_triangles(vertices, triangles)
    deserialize_triangles(binary)
    elapsed = perf_counter() - start
    assert elapsed < budget


@pytest.mark.performance
@pytest.mark.parametrize(
    "category, size",
    [
        ("faible", 10),
        ("moyen", 100),
        ("important", 500),
        ("très important", 1000),
    ],
)
@pytest.mark.performance
@pytest.mark.parametrize(
    "operation_type, size, budget",
    [
        ("triangulation", 100, 0.05),
        ("point_set_conversion", 100, 0.02),
        ("triangles_conversion", 100, 0.03),
    ],
)
def test_repeated_performance_measurements(operation_type, size, budget):
    """Test 4 : Répétition des mesures.

    Répéter les tests plusieurs fois pour chaque catégorie de volume de données
    (faible, moyen important, très important),
    afin d'obtenir des mesures de performance représentatives.
    """
    iterations = 5
    durations = []

    for _ in range(iterations):
        if operation_type == "triangulation":
            points = generate_mock_points(size)
            start = perf_counter()
            compute_triangulation(points)
            durations.append(perf_counter() - start)
        elif operation_type == "point_set_conversion":
            points = generate_mock_points(size)
            start = perf_counter()
            binary = serialize_point_set(points)
            deserialize_point_set(binary)
            durations.append(perf_counter() - start)
        elif operation_type == "triangles_conversion":
            vertices, triangles = generate_mock_triangles(size, size)
            start = perf_counter()
            binary = serialize_triangles(vertices, triangles)
            deserialize_triangles(binary)
            durations.append(perf_counter() - start)

    average_duration = sum(durations) / iterations
    assert average_duration < budget
