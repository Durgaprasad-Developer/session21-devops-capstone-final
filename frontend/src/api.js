const BASE = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Request failed')
  }
  if (res.status === 204) return null
  return res.json()
}

// Appointments
export const fetchAppointments = (params = {}) => {
  const qs = new URLSearchParams(params).toString()
  return request(`/appointments${qs ? '?' + qs : ''}`)
}
export const fetchAppointmentStats = () => request('/appointments/stats')
export const createAppointment = (data) =>
  request('/appointments', { method: 'POST', body: JSON.stringify(data) })
export const updateAppointment = (id, data) =>
  request(`/appointments/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deleteAppointment = (id) =>
  request(`/appointments/${id}`, { method: 'DELETE' })

// Doctors
export const fetchDoctors = () => request('/doctors')
export const createDoctor = (data) =>
  request('/doctors', { method: 'POST', body: JSON.stringify(data) })
export const updateDoctor = (id, data) =>
  request(`/doctors/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deleteDoctor = (id) =>
  request(`/doctors/${id}`, { method: 'DELETE' })

// Patients
export const fetchPatients = () => request('/patients')
export const createPatient = (data) =>
  request('/patients', { method: 'POST', body: JSON.stringify(data) })
export const updatePatient = (id, data) =>
  request(`/patients/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deletePatient = (id) =>
  request(`/patients/${id}`, { method: 'DELETE' })
