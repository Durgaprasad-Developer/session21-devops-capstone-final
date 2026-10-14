import { useState, useEffect, useCallback } from 'react'
import {
  fetchAppointments, createAppointment, updateAppointment, deleteAppointment,
  fetchDoctors, fetchPatients,
} from '../api.js'

const STATUS_COLORS = {
  scheduled: 'badge-scheduled',
  completed: 'badge-completed',
  cancelled: 'badge-cancelled',
}

const AVATAR_COLORS = ['#6366f1', '#0ea5e9', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6']
const avatarColor = (name = '') => AVATAR_COLORS[name.charCodeAt(0) % AVATAR_COLORS.length]
const initials = (name = '') => name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()

function AppointmentModal({ appt, doctors, patients, onSave, onClose }) {
  const [form, setForm] = useState(
    appt
      ? {
          doctor_id:        String(appt.doctor_id),
          patient_id:       String(appt.patient_id),
          appointment_date: appt.appointment_date,
          start_time:       appt.start_time,
          end_time:         appt.end_time,
          reason:           appt.reason || '',
          status:           appt.status,
        }
      : {
          doctor_id: '', patient_id: '', appointment_date: '',
          start_time: '', end_time: '', reason: '', status: 'scheduled',
        }
  )
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const handleSubmit = async e => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      const payload = {
        ...form,
        doctor_id: Number(form.doctor_id),
        patient_id: Number(form.patient_id),
      }
      if (appt) {
        await updateAppointment(appt.id, payload)
      } else {
        await createAppointment(payload)
      }
      onSave()
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal" role="dialog" aria-modal="true">
        <div className="modal-header">
          <h3>{appt ? 'Edit Appointment' : 'New Appointment'}</h3>
          <button className="modal-close" onClick={onClose} aria-label="Close">✕</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div className="error-banner" style={{ marginBottom: 16 }}>⚠️ {error}</div>}
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label" htmlFor="appt-patient">Patient</label>
                <select
                  id="appt-patient"
                  className="form-input"
                  value={form.patient_id}
                  onChange={e => set('patient_id', e.target.value)}
                  required
                >
                  <option value="">Select patient…</option>
                  {patients.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="appt-doctor">Doctor</label>
                <select
                  id="appt-doctor"
                  className="form-input"
                  value={form.doctor_id}
                  onChange={e => set('doctor_id', e.target.value)}
                  required
                >
                  <option value="">Select doctor…</option>
                  {doctors.map(d => (
                    <option key={d.id} value={d.id}>{d.name} — {d.speciality}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="appt-date">Date</label>
                <input
                  id="appt-date"
                  type="date"
                  className="form-input"
                  value={form.appointment_date}
                  onChange={e => set('appointment_date', e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="appt-status">Status</label>
                <select
                  id="appt-status"
                  className="form-input"
                  value={form.status}
                  onChange={e => set('status', e.target.value)}
                >
                  <option value="scheduled">Scheduled</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="appt-start">Start Time</label>
                <input
                  id="appt-start"
                  type="time"
                  className="form-input"
                  value={form.start_time}
                  onChange={e => set('start_time', e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="appt-end">End Time</label>
                <input
                  id="appt-end"
                  type="time"
                  className="form-input"
                  value={form.end_time}
                  onChange={e => set('end_time', e.target.value)}
                  required
                />
              </div>

              <div className="form-group full-width">
                <label className="form-label" htmlFor="appt-reason">Reason for Visit</label>
                <textarea
                  id="appt-reason"
                  className="form-input"
                  rows={3}
                  value={form.reason}
                  onChange={e => set('reason', e.target.value)}
                  placeholder="Describe the reason…"
                  style={{ resize: 'vertical' }}
                />
              </div>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn-ghost" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={saving}>
              {saving ? '⏳ Saving…' : (appt ? '💾 Update' : '➕ Create')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function Appointments() {
  const [appointments, setAppointments] = useState([])
  const [doctors, setDoctors]           = useState([])
  const [patients, setPatients]         = useState([])
  const [loading, setLoading]           = useState(true)
  const [error, setError]               = useState(null)
  const [search, setSearch]             = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [modal, setModal]               = useState(null) // null | { appt: null|object }
  const [deleting, setDeleting]         = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = {}
      if (statusFilter) params.status = statusFilter
      if (search)       params.search = search
      const [appts, docs, pats] = await Promise.all([
        fetchAppointments(params),
        fetchDoctors(),
        fetchPatients(),
      ])
      setAppointments(appts)
      setDoctors(docs)
      setPatients(pats)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [search, statusFilter])

  useEffect(() => { load() }, [load])

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this appointment?')) return
    setDeleting(id)
    try {
      await deleteAppointment(id)
      await load()
    } catch (e) {
      setError(e.message)
    } finally {
      setDeleting(null)
    }
  }

  const handleSaved = () => {
    setModal(null)
    load()
  }

  const fmtDate = (d) => d ? new Date(d + 'T00:00:00').toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
  const fmtTime = (t) => t ? t.slice(0, 5) : '—'

  return (
    <>
      <div className="section-card">
        <div className="section-header">
          <h2>Appointments</h2>
          <div className="section-header-spacer" />
          <button className="btn-primary" onClick={() => setModal({ appt: null })}>
            ➕ New Appointment
          </button>
        </div>

        <div className="filters-row">
          <input
            id="appt-search"
            className="search-input"
            placeholder="🔍 Search patient, doctor, reason…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <select
            id="appt-status-filter"
            className="filter-select"
            value={statusFilter}
            onChange={e => setStatusFilter(e.target.value)}
          >
            <option value="">All statuses</option>
            <option value="scheduled">Scheduled</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>

        {error && <div className="error-banner" style={{ margin: '12px 24px' }}>⚠️ {error}</div>}

        {loading ? (
          <div className="loading-state">
            <div className="spinner" />
            <p>Loading appointments…</p>
          </div>
        ) : appointments.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📅</div>
            <p>No appointments found. Create one to get started.</p>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Patient</th>
                  <th>Doctor</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Reason</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map(a => (
                  <tr key={a.id}>
                    <td style={{ color: 'var(--text-muted)', fontSize: 12 }}>#{a.id}</td>
                    <td>
                      <div className="name-cell">
                        <div className="avatar" style={{ background: avatarColor(a.patient?.name) }}>
                          {initials(a.patient?.name)}
                        </div>
                        {a.patient?.name ?? '—'}
                      </div>
                    </td>
                    <td>
                      <div style={{ fontWeight: 500 }}>{a.doctor?.name ?? '—'}</div>
                      <div style={{ fontSize: 11.5, color: 'var(--text-muted)' }}>{a.doctor?.speciality}</div>
                    </td>
                    <td>{fmtDate(a.appointment_date)}</td>
                    <td style={{ whiteSpace: 'nowrap' }}>{fmtTime(a.start_time)} – {fmtTime(a.end_time)}</td>
                    <td style={{ maxWidth: 180, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {a.reason || <span style={{ color: 'var(--text-muted)' }}>—</span>}
                    </td>
                    <td>
                      <span className={`badge ${STATUS_COLORS[a.status] || ''}`}>
                        {a.status}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button
                          id={`edit-appt-${a.id}`}
                          className="icon-btn"
                          title="Edit"
                          onClick={() => setModal({ appt: a })}
                        >✏️</button>
                        <button
                          id={`del-appt-${a.id}`}
                          className="icon-btn danger"
                          title="Delete"
                          disabled={deleting === a.id}
                          onClick={() => handleDelete(a.id)}
                        >{deleting === a.id ? '⏳' : '🗑️'}</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {modal !== null && (
        <AppointmentModal
          appt={modal.appt}
          doctors={doctors}
          patients={patients}
          onSave={handleSaved}
          onClose={() => setModal(null)}
        />
      )}
    </>
  )
}
