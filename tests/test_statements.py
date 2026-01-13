def _create_school_student_and_invoices(client):
    # Create school
    school_payload = {
        "name": "Statement School",
        "tax_id": "111222333",
        "address": "Statement St 1",
        "is_active": True,
    }
    school_resp = client.post("/api/v1/schools/", json=school_payload)
    assert school_resp.status_code == 201
    school = school_resp.json()

    # Create student
    student_payload = {
        "school_id": school["id"],
        "first_name": "Statement",
        "last_name": "Student",
        "email": "statement.student@example.com",
        "grade": "9A",
        "is_active": True,
    }
    student_resp = client.post("/api/v1/students/", json=student_payload)
    assert student_resp.status_code == 201
    student = student_resp.json()

    # Create invoices: 2 unpaid, 1 paid
    invoices_payload = [
        {
            "student_id": student["id"],
            "amount": 1000.0,
            "due_date": "2026-01-31",
            "paid": False,
        },
        {
            "student_id": student["id"],
            "amount": 500.0,
            "due_date": "2026-02-28",
            "paid": True,
        },
        {
            "student_id": student["id"],
            "amount": 250.0,
            "due_date": "2026-03-31",
            "paid": False,
        },
    ]

    for payload in invoices_payload:
        resp = client.post("/api/v1/invoices/", json=payload)
        assert resp.status_code == 201

    return school, student


def test_student_statement(client):
    school, student = _create_school_student_and_invoices(client)

    resp = client.get(f"/api/v1/students/{student['id']}/statement")
    assert resp.status_code == 200

    data = resp.json()
    assert data["student_id"] == student["id"]
    assert data["school_id"] == school["id"]

    # Check totals: 1000 + 500 + 250 = 1750
    assert data["total_invoiced"] == 1750.0
    # Paid: only the 500 one
    assert data["total_paid"] == 500.0
    # Pending: 1000 + 250 = 1250
    assert data["total_pending"] == 1250.0

    assert isinstance(data["invoices"], list)
    assert len(data["invoices"]) == 3


def test_school_statement(client):
    school, student = _create_school_student_and_invoices(client)

    resp = client.get(f"/api/v1/schools/{school['id']}/statement")
    assert resp.status_code == 200

    data = resp.json()
    assert data["school_id"] == school["id"]
    assert data["total_students"] >= 1

    assert data["total_invoiced"] == 1750.0
    assert data["total_paid"] == 500.0
    assert data["total_pending"] == 1250.0

    assert isinstance(data["invoices"], list)
    assert len(data["invoices"]) == 3
