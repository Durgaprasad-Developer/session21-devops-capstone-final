"""Tests 2-5 — Appointment CRUD endpoints."""


def test_list_appointments_empty(client):
    """GET /api/appointments returns an empty list when no appointments exist."""
    resp = client.get("/api/appointments")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_appointment(client, sample_appointment):
    """POST /api/appointments creates and returns an appointment."""
    assert sample_appointment["status"] == "scheduled"
    assert sample_appointment["reason"] == "Check-up"
    assert "id" in sample_appointment


def test_list_appointments_after_create(client, sample_appointment):
    """GET /api/appointments returns the created appointment."""
    resp = client.get("/api/appointments")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_appointment["id"]


def test_get_appointment_by_id(client, sample_appointment):
    """GET /api/appointments/{id} returns a specific appointment."""
    appt_id = sample_appointment["id"]
    resp = client.get(f"/api/appointments/{appt_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == appt_id


def test_update_appointment_status(client, sample_appointment):
    """PUT /api/appointments/{id} updates status to completed."""
    appt_id = sample_appointment["id"]
    resp = client.put(
        f"/api/appointments/{appt_id}",
        json={"status": "completed"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


def test_get_nonexistent_appointment(client):
    """GET /api/appointments/99999 returns 404."""
    resp = client.get("/api/appointments/99999")
    assert resp.status_code == 404


def test_delete_appointment(client, sample_appointment):
    """DELETE /api/appointments/{id} removes the appointment."""
    appt_id = sample_appointment["id"]
    del_resp = client.delete(f"/api/appointments/{appt_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/appointments/{appt_id}")
    assert get_resp.status_code == 404


def test_appointment_stats(client, sample_appointment):
    """GET /api/appointments/stats returns aggregated counts."""
    resp = client.get("/api/appointments/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert "upcoming" in data
    assert "completed" in data
    assert "cancelled" in data


def test_end_time_before_start_time_rejected(client, sample_doctor, sample_patient):
    """POST /api/appointments with end_time <= start_time returns 422."""
    resp = client.post(
        "/api/appointments",
        json={
            "doctor_id": sample_doctor["id"],
            "patient_id": sample_patient["id"],
            "appointment_date": "2030-02-01",
            "start_time": "10:00:00",
            "end_time": "09:00:00",
            "reason": "Bad time",
        },
    )
    assert resp.status_code == 422
