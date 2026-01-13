def test_create_school(client):
    payload = {
        "name": "New School",
        "tax_id": "987654321",
        "address": "Another Street 456",
        "is_active": True,
    }

    response = client.post("/api/v1/schools/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == payload["name"]
    assert data["tax_id"] == payload["tax_id"]
    assert data["address"] == payload["address"]


def test_list_schools(client):
    response = client.get("/api/v1/schools/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_school_not_found(client):
    response = client.get("/api/v1/schools/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "School not found"
