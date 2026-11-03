from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "point_set_id, raw_points",
    [
        ("123e4567-e89b-12d3-a456-426614174000", [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]),
        (
            "123e4567-e89b-12d3-a456-426614174001",
            [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0), (1.0, 1.0)],
        ),
        ("123e4567-e89b-12d3-a456-426614174002", [(1.0, 1.0), (4.0, 1.0), (2.5, 4.0)]),
    ],
)
@patch("app.fetch_point_set_from_manager")
def test_triangulator_fetches_existing_point_set(
    mock_fetch, client, point_set_id, raw_points
):
    """Test 1 : Test de la récupération d'un PointSet existant.

    Vérifie que le Triangulator récupère correctement le PointSet auprès du
    PointSetManager et utilise les données reçues pour effectuer la triangulation.
    """
    mock_fetch.return_value = serialize_point_set(raw_points)
    response = client.get(f"/triangulation/{point_set_id}")

    assert response.status_code == 200
    mock_fetch.assert_called_once_with(point_set_id)
    assert len(response.data) >= 4


@pytest.mark.parametrize(
    "missing_id",
    [
        "00000000-0000-0000-0000-000000000000",
        "11111111-1111-1111-1111-111111111111",
        "22222222-2222-2222-2222-222222222222",
    ],
)
@patch("app.fetch_point_set_from_manager")
def test_triangulator_handles_non_existent_point_set(mock_fetch, client, missing_id):
    """Test 2 : Test d'un PointSet inexistant.

    Vérifie que le Triangulator renvoie une réponse 404 contenant un code et un message
    lorsque le PointSetManager indique que le PointSet demandé n'existe pas.
    """
    mock_fetch.side_effect = PointSetNotFoundError("Not found")
    response = client.get(f"/triangulation/{missing_id}")

    assert response.status_code == 404
    data = response.get_json()
    assert "code" in data
    assert "message" in data


@pytest.mark.parametrize(
    "point_set_id",
    [
        "123e4567-e89b-12d3-a456-426614174010",
        "123e4567-e89b-12d3-a456-426614174011",
        "123e4567-e89b-12d3-a456-426614174012",
    ],
)
@patch("app.fetch_point_set_from_manager")
def test_triangulator_handles_manager_unavailable(mock_fetch, client, point_set_id):
    """Test 3 : Test d'une indisponibilité du PointSetManager.

    Vérifie que le Triangulator renvoie une réponse 503 contenant un code
    et un message lorsque la communication avec le PointSetManager échoue
    ou que celui-ci est indisponible.
    """
    mock_fetch.side_effect = ConnectionError("Service down")
    response = client.get(f"/triangulation/{point_set_id}")

    assert response.status_code == 503
    data = response.get_json()
    assert "code" in data
    assert "message" in data


@pytest.mark.parametrize(
    "invalid_payload",
    [
        b"\x00\x00\x00\x01",
        b"corrupted_binary_data",
        b"\xff\xff\xff\xff",
    ],
)
@patch("app.fetch_point_set_from_manager")
def test_triangulator_handles_invalid_manager_response(
    mock_fetch, client, invalid_payload
):
    """Test 4 : Test d'une réponse invalide du PointSetManager.

    Vérifie que le Triangulator gère correctement un PointSet reçu
    qui ne respecte pas le format binaire attendu.
    """
    mock_fetch.return_value = invalid_payload
    response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174020")

    assert response.status_code in (400, 500)
    data = response.get_json()
    assert "code" in data
    assert "message" in data
