def test_create_student(client, school):
    payload = {
        "school_id": school["id"],
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "grade": "5A",
        "is_active": True,
    }

    response = client.post("/api/v1/students/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["school_id"] == school["id"]
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["grade"] == payload["grade"]


def test_list_students(client, school):
    # Ensure at least one student exists
    payload = {
        "school_id": school["id"],
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "grade": "6B",
        "is_active": True,
    }
    client.post("/api/v1/students/", json=payload)

    response = client.get("/api/v1/students/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_student_not_found(client):
    response = client.get("/api/v1/students/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"
