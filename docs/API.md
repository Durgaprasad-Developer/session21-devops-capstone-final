# BookEase — REST API Reference & Specification

The BookEase backend exposes a RESTful API built with FastAPI and documented automatically via OpenAPI / Swagger. When running locally or in a Kubernetes cluster, interactive documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs` (or `http://<INGRESS-IP>/docs`)
- **ReDoc**: `http://localhost:8000/redoc` (or `http://<INGRESS-IP>/redoc`)
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

![FastAPI Swagger Documentation](screenshots/fastapi_swagger_docs.png)

---

## Endpoint Catalog

### System & Health Endpoints

| Method | Route | Description | Response Codes |
|---|---|---|---|
| `GET` | `/health` | Liveness probe returning overall service health | `200 OK` |
| `GET` | `/ready` | Readiness probe validating PostgreSQL database connectivity | `200 OK`, `503 Service Unavailable` |
| `GET` | `/metrics` | Prometheus metrics scrape target | `200 OK` |

#### `/health` Example Response:
```json
{
  "status": "healthy"
}
```

#### `/ready` Example Response:
```json
{
  "status": "ready",
  "database": "connected"
}
```

---

### Appointments Management (`/api/appointments`)

| Method | Route | Description | Parameters / Body | Response |
|---|---|---|---|---|
| `GET` | `/api/appointments` | List all appointments with doctor and patient details | Optional query filters | `200 OK` array |
| `POST` | `/api/appointments` | Book appointment (enforces doctor working hours & double-booking prevention) | `AppointmentCreate` JSON body | `201 Created` |
| `GET` | `/api/appointments/{id}` | Retrieve specific appointment details | `id: int` path parameter | `200 OK` or `404 Not Found` |
| `PUT` | `/api/appointments/{id}` | Update appointment status (`scheduled`, `completed`, `cancelled`) | `status: str` | `200 OK` |
| `DELETE` | `/api/appointments/{id}` | Delete / cancel appointment record | `id: int` path parameter | `204 No Content` |
| `GET` | `/api/appointments/stats` | Outpatient queue statistics (total, today, completed, cancelled) | None | `200 OK` JSON object |

#### Appointment Creation Payload (`POST /api/appointments`):
```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2026-10-16",
  "start_time": "10:00:00",
  "end_time": "10:30:00",
  "reason": "Routine clinical cardiology check-up"
}
```

#### Queue Statistics Response (`GET /api/appointments/stats`):
```json
{
  "total": 3,
  "today": 3,
  "completed": 1,
  "cancelled": 0
}
```

---

### Doctors & Working Hours (`/api/doctors`)

| Method | Route | Description | Parameters / Body | Response |
|---|---|---|---|---|
| `GET` | `/api/doctors` | List all active physicians with specialty and daily availability hours | None | `200 OK` array |
| `POST` | `/api/doctors` | Register a new physician profile | `DoctorCreate` JSON body | `201 Created` |
| `GET` | `/api/doctors/{id}` | Retrieve doctor profile by ID | `id: int` path parameter | `200 OK` |
| `PUT` | `/api/doctors/{id}` | Update doctor credentials or availability hours | `DoctorUpdate` JSON body | `200 OK` |

#### Doctor Profile Schema:
```json
{
  "id": 1,
  "name": "Dr. Ananya Krishnan",
  "speciality": "Cardiology",
  "email": "ananya.krishnan@bookease.com",
  "phone": "+91-9876543210",
  "available_from": "09:00:00",
  "available_to": "17:00:00"
}
```

---

### Patients (`/api/patients`)

| Method | Route | Description | Parameters / Body | Response |
|---|---|---|---|---|
| `GET` | `/api/patients` | List all registered patients | None | `200 OK` array |
| `POST` | `/api/patients` | Register a new patient record | `PatientCreate` JSON body | `201 Created` |
| `GET` | `/api/patients/{id}` | Retrieve patient details by ID | `id: int` path parameter | `200 OK` |
| `DELETE` | `/api/patients/{id}` | Remove patient record | `id: int` path parameter | `204 No Content` |
