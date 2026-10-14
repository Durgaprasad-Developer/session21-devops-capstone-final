import { useState, useEffect } from 'react'
import { fetchDoctors, createDoctor, updateDoctor, deleteDoctor } from '../api.js'

const AVATAR_COLORS = ['#6366f1', '#0ea5e9', '#22c55e', '#f59e0b', '#8b5cf6']
const avatarColor = (name = '') => AVATAR_COLORS[name.charCodeAt(0) % AVATAR_COLORS.length]
const initials = (name = '') => name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()

function DoctorModal({ doctor, onSave, onClose }) {
  const [form, setForm] = useState(
    doctor
      ? {
          name: doctor.name, speciality: doctor.speciality,
          email: doctor.email || '', phone: doctor.phone || '',
          availability_start: doctor.availability_start || '',
          availability_end:   doctor.availability_end || '',
        }
      : { name: '', speciality: '', email: '', phone: '', availability_start: '', availability_end: '' }
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
        availability_start: form.availability_start || null,
        availability_end:   form.availability_end   || null,
      }
      if (doctor) await updateDoctor(doctor.id, payload)
      else        await createDoctor(payload)
      onSave()
    } catch (err) { setError(err.message) }
    finally      { setSaving(false) }
  }

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-header">
          <h3>{doctor ? 'Edit Doctor' : 'New Doctor'}</h3>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div className="error-banner" style={{ marginBottom: 16 }}>⚠️ {error}</div>}
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label" htmlFor="doc-name">Full Name</label>
                <input id="doc-name" className="form-input" required value={form.name}
                  onChange={e => set('name', e.target.value)} placeholder="Dr. Ananya Krishnan" />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="doc-spec">Speciality</label>
                <input id="doc-spec" className="form-input" required value={form.speciality}
                  onChange={e => set('speciality', e.target.value)} placeholder="Cardiology" />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="doc-email">Email</label>
                <input id="doc-email" type="email" className="form-input" value={form.email}
                  onChange={e => set('email', e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="doc-phone">Phone</label>
                <input id="doc-phone" className="form-input" value={form.phone}
                  onChange={e => set('phone', e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="doc-avail-start">Available From</label>
                <input id="doc-avail-start" type="time" className="form-input"
                  value={form.availability_start} onChange={e => set('availability_start', e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="doc-avail-end">Available Until</label>
                <input id="doc-avail-end" type="time" className="form-input"
                  value={form.availability_end} onChange={e => set('availability_end', e.target.value)} />
              </div>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn-ghost" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={saving}>
              {saving ? '⏳ Saving…' : (doctor ? '💾 Update' : '➕ Add Doctor')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function Doctors() {
  const [doctors, setDoctors]   = useState([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)
  const [modal, setModal]       = useState(null)

  const load = () => {
    setLoading(true)
    fetchDoctors()
      .then(setDoctors)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this doctor? All associated appointments will also be deleted.')) return
    try {
      await deleteDoctor(id)
      load()
    } catch (e) { setError(e.message) }
  }

  return (
    <>
      <div className="section-card">
        <div className="section-header">
          <h2>Doctors</h2>
          <div className="section-header-spacer" />
          <button className="btn-primary" onClick={() => setModal({ doctor: null })}>➕ Add Doctor</button>
        </div>

        {error && <div className="error-banner" style={{ margin: '12px 24px' }}>⚠️ {error}</div>}

        {loading ? (
          <div className="loading-state"><div className="spinner" /><p>Loading doctors…</p></div>
        ) : doctors.length === 0 ? (
          <div className="empty-state"><div className="empty-icon">🩺</div><p>No doctors yet.</p></div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th><th>Name</th><th>Speciality</th><th>Email</th><th>Phone</th><th>Availability</th><th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {doctors.map(d => (
                <tr key={d.id}>
                  <td style={{ color: 'var(--text-muted)', fontSize: 12 }}>#{d.id}</td>
                  <td>
                    <div className="name-cell">
                      <div className="avatar" style={{ background: avatarColor(d.name) }}>
                        {initials(d.name)}
                      </div>
                      <span style={{ fontWeight: 500 }}>{d.name}</span>
                    </div>
                  </td>
                  <td>
                    <span className="badge" style={{ background: '#eef2ff', color: '#4f46e5' }}>
                      {d.speciality}
                    </span>
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>{d.email || '—'}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{d.phone || '—'}</td>
                  <td style={{ fontSize: 12.5, color: 'var(--text-secondary)' }}>
                    {d.availability_start && d.availability_end
                      ? `${d.availability_start.slice(0,5)} – ${d.availability_end.slice(0,5)}`
                      : '—'}
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button id={`edit-doc-${d.id}`} className="icon-btn" title="Edit"
                        onClick={() => setModal({ doctor: d })}>✏️</button>
                      <button id={`del-doc-${d.id}`} className="icon-btn danger" title="Delete"
                        onClick={() => handleDelete(d.id)}>🗑️</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {modal !== null && (
        <DoctorModal
          doctor={modal.doctor}
          onSave={() => { setModal(null); load() }}
          onClose={() => setModal(null)}
        />
      )}
    </>
  )
}
