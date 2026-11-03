import pytest


@pytest.mark.parametrize(
    "points",
    [
        [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)],
        [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)],
        [(0.0, 0.0), (2.0, 0.0), (1.0, 1.0), (0.0, 2.0)],
    ],
)
def test_triangulation_simple_point_set(points):
    """Test 1 : test de triangulation avec un ensemble de points simple.

    Vérifie que la triangulation obtenue est valide pour un ensemble de points
    permettant de former un ou plusieurs triangles.
    """
    vertices, triangles = compute_triangulation(points)

    assert len(vertices) == len(points)
    assert len(triangles) >= 1
    for tri in triangles:
        assert len(tri) == 3
        for index in tri:
            assert 0 <= index < len(vertices)


@pytest.mark.parametrize(
    "points",
    [
        [],
        [(0.0, 0.0)],
        [(0.0, 0.0), (1.0, 1.0)],
    ],
)
def test_triangulation_insufficient_points(points):
    """Test 2 : test de triangulation avec un nombre de points insuffisant.

    Vérifie que le cas d'un ensemble contenant moins de 3 points
    lève bien une exception.
    """
    with pytest.raises(ValueError):
        compute_triangulation(points)


@pytest.mark.parametrize(
    "points",
    [
        [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)],
        [(0.0, 0.0), (0.0, 0.0), (1.0, 1.0)],
        [(1.0, 1.0), (1.0, 1.0), (1.0, 1.0)],
    ],
)
def test_triangulation_degenerate_points(points):
    """Test 3 : test de triangulation avec des points dégénérés.

    Vérifie le comportement face à 3 configurations de points dégénérés
    (comme des points alignés et/ou dupliqués).
    """
    with pytest.raises(ValueError):
        compute_triangulation(points)


@pytest.mark.parametrize(
    "points",
    [
        [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0), (1.0, 1.0)],
        [(0.0, 0.0), (3.0, 0.0), (0.0, 3.0), (3.0, 3.0)],
        [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)],
    ],
)
def test_triangulation_consistency(points):
    """Test 4 : test de cohérence de la triangulation obtenue.

    Vérifie la cohérence des indices et la validité des Triangles
    pour 3 jeux de données.
    """
    vertices, triangles = compute_triangulation(points)

    assert vertices == points
    for tri in triangles:
        i1, i2, i3 = tri
        assert i1 != i2 and i2 != i3 and i1 != i3
        for index in tri:
            assert 0 <= index < len(points)
