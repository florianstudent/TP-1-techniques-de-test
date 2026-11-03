from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "point_set_id",
    [
        "123e4567-e89b-12d3-a456-426614174000",
        "223e4567-e89b-12d3-a456-426614174001",
        "323e4567-e89b-12d3-a456-426614174002",
    ],
)
def test_triangulation_api_valid_request(client, point_set_id):
    """Test 1 : Test d'une requête valide avec un PointSetID existant.

    Vérifie l'envoi d'une réponse 200 contenant un Triangle au format binaire attendu
    si la requête est valide.
    """
    response = client.get(f"/triangulation/{point_set_id}")
    assert response.status_code == 200
    assert response.content_type == "application/octet-stream"
    assert len(response.data) >= 4


@pytest.mark.parametrize(
    "invalid_id",
    [
        "not-a-uuid",
        "12345",
        "xyz-abc-def-ghi",
    ],
)
def test_triangulation_api_invalid_format(client, invalid_id):
    """Test 2 : Test d'un PointSetID au format invalide.

    Vérifie l'envoi d'une réponse 400 contenant un code et un message
    si le PointSetID a un format invalide.
    """
    response = client.get(f"/triangulation/{invalid_id}")
    assert response.status_code == 400
    data = response.get_json()
    assert "code" in data
    assert "message" in data


@pytest.mark.parametrize(
    "missing_id",
    [
        "00000000-0000-0000-0000-000000000000",
        "11111111-1111-1111-1111-111111111111",
        "22222222-2222-2222-2222-222222222222",
    ],
)
def test_triangulation_api_not_found(client, missing_id):
    """Test 3 : Test d'un PointSetID inexistant.

    Vérifie l'envoi d'une réponse 404 contenant un code et un message
    si le PointSetID n'existe pas.
    """
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
@patch("app.compute_triangulation")
def test_triangulation_api_failure(mock_compute, client, point_set_id):
    """Test 4 : Test d'un échec de triangulation.

    Vérifie l'envoi d'une réponse 500 contenant un code
    et un message associé si la triangulation échoue.
    """
    mock_compute.side_effect = ValueError("Algorithm failed")
    response = client.get(f"/triangulation/{point_set_id}")
    assert response.status_code == 500
    data = response.get_json()
    assert "code" in data
    assert "message" in data


@pytest.mark.parametrize(
    "point_set_id",
    [
        "123e4567-e89b-12d3-a456-426614174020",
        "123e4567-e89b-12d3-a456-426614174021",
        "123e4567-e89b-12d3-a456-426614174022",
    ],
)
@patch("app.fetch_point_set_from_manager")
def test_triangulation_api_manager_unavailable(mock_fetch, client, point_set_id):
    """Test 5 : Test d'une indisponibilité du PointSetManager.

    Vérifie l'envoi d'une réponse 503 contenant un code
    et un message si le PointSetManager est indisponible.
    """
    mock_fetch.side_effect = ConnectionError("Manager offline")
    response = client.get(f"/triangulation/{point_set_id}")
    assert response.status_code == 503
    data = response.get_json()
    assert "code" in data
    assert "message" in data
