def test_create_invoice(client, school):
    # First create a student for this school
    student_payload = {
        "school_id": school["id"],
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "grade": "6B",
        "is_active": True,
    }
    student_resp = client.post("/api/v1/students/", json=student_payload)
    assert student_resp.status_code == 201
    student_id = student_resp.json()["id"]

    invoice_payload = {
        "student_id": student_id,
        "amount": 1500.5,
        "due_date": "2026-01-31",
        "paid": False,
    }

    response = client.post("/api/v1/invoices/", json=invoice_payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["student_id"] == student_id
    assert data["amount"] == invoice_payload["amount"]
    assert data["paid"] is False


def test_list_invoices(client, school):
    # ensure at least one invoice exists
    student_payload = {
        "school_id": school["id"],
        "first_name": "Mark",
        "last_name": "Brown",
        "email": "mark.brown@example.com",
        "grade": "7C",
        "is_active": True,
    }
    student_resp = client.post("/api/v1/students/", json=student_payload)
    student_id = student_resp.json()["id"]

    invoice_payload = {
        "student_id": student_id,
        "amount": 999.9,
        "due_date": "2026-02-01",
        "paid": True,
    }
    client.post("/api/v1/invoices/", json=invoice_payload)

    response = client.get("/api/v1/invoices/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_invoice_not_found(client):
    response = client.get("/api/v1/invoices/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Invoice not found"
