import { useState, useEffect } from 'react'
import { fetchPatients, createPatient, updatePatient, deletePatient } from '../api.js'

const AVATAR_COLORS = ['#f59e0b', '#ef4444', '#8b5cf6', '#0ea5e9', '#22c55e']
const avatarColor = (name = '') => AVATAR_COLORS[name.charCodeAt(0) % AVATAR_COLORS.length]
const initials = (name = '') => name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()

function PatientModal({ patient, onSave, onClose }) {
  const [form, setForm] = useState(
    patient
      ? { name: patient.name, email: patient.email || '', phone: patient.phone || '', date_of_birth: patient.date_of_birth || '' }
      : { name: '', email: '', phone: '', date_of_birth: '' }
  )
  const [saving, setSaving] = useState(false)
  const [error, setError]   = useState(null)
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const handleSubmit = async e => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      const payload = { ...form, date_of_birth: form.date_of_birth || null }
      if (patient) await updatePatient(patient.id, payload)
      else         await createPatient(payload)
      onSave()
    } catch (err) { setError(err.message) }
    finally       { setSaving(false) }
  }

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-header">
          <h3>{patient ? 'Edit Patient' : 'New Patient'}</h3>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div className="error-banner" style={{ marginBottom: 16 }}>⚠️ {error}</div>}
            <div className="form-grid">
              <div className="form-group full-width">
                <label className="form-label" htmlFor="pat-name">Full Name</label>
                <input id="pat-name" className="form-input" required value={form.name}
                  onChange={e => set('name', e.target.value)} placeholder="Vikram Nair" />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="pat-email">Email</label>
                <input id="pat-email" type="email" className="form-input" value={form.email}
                  onChange={e => set('email', e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="pat-phone">Phone</label>
                <input id="pat-phone" className="form-input" value={form.phone}
                  onChange={e => set('phone', e.target.value)} />
              </div>
              <div className="form-group full-width">
                <label className="form-label" htmlFor="pat-dob">Date of Birth</label>
                <input id="pat-dob" type="date" className="form-input" value={form.date_of_birth}
                  onChange={e => set('date_of_birth', e.target.value)} />
              </div>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn-ghost" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={saving}>
              {saving ? '⏳ Saving…' : (patient ? '💾 Update' : '➕ Add Patient')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function Patients() {
  const [patients, setPatients] = useState([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)
  const [modal, setModal]       = useState(null)

  const load = () => {
    setLoading(true)
    fetchPatients()
      .then(setPatients)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }
  useEffect(load, [])

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this patient?')) return
    try { await deletePatient(id); load() }
    catch (e) { setError(e.message) }
  }

  const fmtDob = (d) => d ? new Date(d + 'T00:00:00').toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'

  return (
    <>
      <div className="section-card">
        <div className="section-header">
          <h2>Patients</h2>
          <div className="section-header-spacer" />
          <button className="btn-primary" onClick={() => setModal({ patient: null })}>➕ Add Patient</button>
        </div>

        {error && <div className="error-banner" style={{ margin: '12px 24px' }}>⚠️ {error}</div>}

        {loading ? (
          <div className="loading-state"><div className="spinner" /><p>Loading patients…</p></div>
        ) : patients.length === 0 ? (
          <div className="empty-state"><div className="empty-icon">👤</div><p>No patients yet.</p></div>
        ) : (
          <table className="data-table">
            <thead>
              <tr><th>#</th><th>Name</th><th>Email</th><th>Phone</th><th>Date of Birth</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {patients.map(p => (
                <tr key={p.id}>
                  <td style={{ color: 'var(--text-muted)', fontSize: 12 }}>#{p.id}</td>
                  <td>
                    <div className="name-cell">
                      <div className="avatar" style={{ background: avatarColor(p.name) }}>
                        {initials(p.name)}
                      </div>
                      <span style={{ fontWeight: 500 }}>{p.name}</span>
                    </div>
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>{p.email || '—'}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{p.phone || '—'}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{fmtDob(p.date_of_birth)}</td>
                  <td>
                    <div className="action-buttons">
                      <button id={`edit-pat-${p.id}`} className="icon-btn" title="Edit"
                        onClick={() => setModal({ patient: p })}>✏️</button>
                      <button id={`del-pat-${p.id}`} className="icon-btn danger" title="Delete"
                        onClick={() => handleDelete(p.id)}>🗑️</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {modal !== null && (
        <PatientModal
          patient={modal.patient}
          onSave={() => { setModal(null); load() }}
          onClose={() => setModal(null)}
        />
      )}
    </>
  )
}
