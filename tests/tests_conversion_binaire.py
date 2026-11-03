import struct

import pytest


@pytest.mark.parametrize(
    "points",
    [
        [(0.0, 0.0)],
        [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)],
        [(0.5, 1.5), (-2.0, 3.0), (4.1, -5.2), (0.0, 0.0), (10.0, 10.0)],
    ],
)
def test_point_set_serialization_deserialization(points):
    """Test 1 : Test de la sérialisation et désérialisation des PointSet.

    Vérifie le nombre de points, les coordonnées et le respect du format binaire
    défini par l'API.
    """
    binary_data = serialize_point_set(points)
    recovered_points, count = deserialize_point_set(binary_data)

    assert count == len(points)
    assert len(recovered_points) == len(points)
    assert recovered_points == points


@pytest.mark.parametrize(
    "invalid_data",
    [
        b"\x00\x00\x00",
        b"\x02\x00\x00\x00\x00\x00\x00\x00",
        b"invalid_binary_stream_payload",
    ],
)
def test_invalid_point_set_binary_data(invalid_data):
    """Test 2 : Test de données binaires invalides ou incohérentes.

    Vérifie que des données ne respectant pas le format attendu ne soient
    pas interprétées comme un PointSet valide.
    """
    with pytest.raises((ValueError, struct.error)):
        deserialize_point_set(invalid_data)


@pytest.mark.parametrize(
    "vertices, triangles",
    [
        ([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], [(0, 1, 2)]),
        ([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)], [(0, 1, 2), (0, 2, 3)]),
        ([(0.0, 0.0), (2.0, 0.0), (1.0, 2.0)], []),
    ],
)
def test_triangles_serialization_deserialization(vertices, triangles):
    """Test 3 : Test de la sérialisation et désérialisation des Triangles.

    Vérifie le nombre de sommets, le nombre de Triangles
    et les trois indices de chaque Triangle.
    """
    binary_data = serialize_triangles(vertices, triangles)
    rec_vertices, rec_triangles, v_count, t_count = deserialize_triangles(binary_data)

    assert v_count == len(vertices)
    assert t_count == len(triangles)
    assert rec_triangles == triangles


@pytest.mark.parametrize(
    "data_structure, is_triangles",
    [
        ([(0.0, 0.0), (1.0, 1.0)], False),
        ([(2.0, 3.0), (4.0, 5.0), (6.0, 7.0)], False),
        (([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], [(0, 1, 2)]), True),
    ],
)
def test_binary_round_trip_conversion(data_structure, is_triangles):
    """Test 4 : Test d'une conversion aller-retour.

    Vérifie qu'une sérialisation suivie d'une désérialisation (un aller-retour)
    conserve intégralement les données initiales.
    """
    if not is_triangles:
        binary = serialize_point_set(data_structure)
        recovered, _ = deserialize_point_set(binary)
        assert recovered == data_structure
    else:
        vertices, triangles = data_structure
        binary = serialize_triangles(vertices, triangles)
        rec_v, rec_t, _, _ = deserialize_triangles(binary)
        assert rec_v == vertices
        assert rec_t == triangles


@pytest.mark.parametrize(
    "vertices, triangles",
    [
        ([], []),
        ([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)], []),
        ([], [(0, 1, 2)]),
    ],
)
def test_binary_edge_cases(vertices, triangles):
    """Test 5 : Test de cas limites.

    Vérifie le comportement avec des données ne contenant
    aucun sommet et/ou aucun triangle.
    """
    binary_data = serialize_triangles(vertices, triangles)
    rec_vertices, rec_triangles, v_count, t_count = deserialize_triangles(binary_data)

    assert v_count == len(vertices)
    assert t_count == len(triangles)
    assert len(rec_vertices) == len(vertices)
    assert len(rec_triangles) == len(triangles)
