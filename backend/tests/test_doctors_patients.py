"""Tests — Doctor and Patient endpoints."""


def test_create_and_list_doctors(client):
    resp = client.post(
        "/api/doctors",
        json={"name": "Dr. Smith", "speciality": "Dermatology"},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Dr. Smith"

    list_resp = client.get("/api/doctors")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1


def test_get_nonexistent_doctor(client):
    resp = client.get("/api/doctors/99999")
    assert resp.status_code == 404


def test_create_and_list_patients(client):
    resp = client.post(
        "/api/patients",
        json={"name": "Jane Doe", "email": "jane@example.com"},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Jane Doe"

    list_resp = client.get("/api/patients")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1


def test_update_doctor(client):
    create_resp = client.post(
        "/api/doctors",
        json={"name": "Dr. Old Name", "speciality": "ENT"},
    )
    doc_id = create_resp.json()["id"]
    update_resp = client.put(
        f"/api/doctors/{doc_id}",
        json={"name": "Dr. New Name"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Dr. New Name"


def test_delete_patient(client):
    create_resp = client.post(
        "/api/patients",
        json={"name": "Temp Patient", "email": "temp@example.com"},
    )
    pat_id = create_resp.json()["id"]
    del_resp = client.delete(f"/api/patients/{pat_id}")
    assert del_resp.status_code == 204
    assert client.get(f"/api/patients/{pat_id}").status_code == 404
