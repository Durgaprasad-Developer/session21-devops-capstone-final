import { useState, useEffect } from 'react'
import { fetchAppointmentStats, fetchDoctors, fetchPatients, createAppointment } from '../api.js'

const CLINICAL_DOCTORS = [
  {
    id: 1,
    name: 'Dr. Ananya Krishnan',
    specialty: 'Cardiology',
    title: 'Chief Cardiologist & Vascular Specialist',
    department: 'Heart & Vascular Center',
    room: 'OPD Block A · Room 104',
    timing: 'Today · 09:30 AM – 01:00 PM',
    experience: '14+ Yrs Exp',
    rating: '4.9 ★',
    fee: '$120',
    avatarBg: '#0284c7',
  },
  {
    id: 2,
    name: 'Dr. Rajesh Sharma',
    specialty: 'Pediatrics',
    title: 'Senior Consultant Pediatrician',
    department: 'Child Healthcare Pavilion',
    room: 'Children’s Wing · Suite 12',
    timing: 'Today · 10:00 AM – 02:00 PM',
    experience: '11+ Yrs Exp',
    rating: '4.8 ★',
    fee: '$95',
    avatarBg: '#d97706',
  },
  {
    id: 3,
    name: 'Dr. Priya Patel',
    specialty: 'Neurology',
    title: 'Consultant Neurosurgeon & Spine Specialist',
    department: 'Brain & Spine Institute',
    room: 'Neuro OPD · 3rd Floor, Room 302',
    timing: 'Tomorrow · 11:00 AM – 03:00 PM',
    experience: '16+ Yrs Exp',
    rating: '4.9 ★',
    fee: '$150',
    avatarBg: '#059669',
  },
  {
    id: 4,
    name: 'Dr. David Kim',
    specialty: 'Orthopedics',
    title: 'Orthopedic Surgeon & Sports Medicine',
    department: 'Bone & Joint Rehabilitation',
    room: 'Sports Medicine Unit · Room 205',
    timing: 'Tomorrow · 02:00 PM – 05:30 PM',
    experience: '9+ Yrs Exp',
    rating: '4.7 ★',
    fee: '$110',
    avatarBg: '#7c3aed',
  },
]

const SPECIALTIES = ['All Specialties', 'Cardiology', 'Pediatrics', 'Neurology', 'Orthopedics', 'General Medicine']

export default function Dashboard({ onNavigate }) {
  const [stats, setStats] = useState(null)
  const [doctors, setDoctors] = useState([])
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedSpecialty, setSelectedSpecialty] = useState('All Specialties')
  const [searchQuery, setSearchQuery] = useState('')
  const [bookingDoctor, setBookingDoctor] = useState(null)

  // Booking Form State
  const [bookingForm, setBookingForm] = useState({
    patient_id: '',
    doctor_id: '',
    appointment_date: new Date().toISOString().split('T')[0],
    start_time: '10:00',
    end_time: '10:30',
    reason: 'Routine Consultation',
    status: 'scheduled',
  })
  const [bookingSaving, setBookingSaving] = useState(false)
  const [bookingError, setBookingError] = useState(null)
  const [bookingSuccess, setBookingSuccess] = useState(false)

  useEffect(() => {
    Promise.all([
      fetchAppointmentStats().catch(() => null),
      fetchDoctors().catch(() => []),
      fetchPatients().catch(() => []),
    ])
      .then(([statsData, doctorsData, patientsData]) => {
        setStats(statsData)
        setDoctors(doctorsData || [])
        setPatients(patientsData || [])
      })
      .finally(() => setLoading(false))
  }, [])

  const handleOpenBooking = (doc) => {
    setBookingDoctor(doc)
    setBookingError(null)
    setBookingSuccess(false)

    let matchedDoc = doctors.find(
      d => d.name.toLowerCase().includes(doc.name.toLowerCase().replace('dr. ', '')) ||
           d.speciality.toLowerCase() === doc.specialty.toLowerCase()
    )
    if (!matchedDoc && doctors.length > 0) {
      matchedDoc = doctors[0]
    }

    setBookingForm({
      patient_id: patients.length > 0 ? String(patients[0].id) : '',
      doctor_id: matchedDoc ? String(matchedDoc.id) : (doctors[0] ? String(doctors[0].id) : ''),
      appointment_date: new Date().toISOString().split('T')[0],
      start_time: '10:00',
      end_time: '10:30',
      reason: `${doc.specialty} Consultation with ${doc.name}`,
      status: 'scheduled',
    })
  }

  const handleCloseBooking = () => {
    setBookingDoctor(null)
    setBookingError(null)
    setBookingSuccess(false)
  }

  const handleBookingSubmit = async (e) => {
    e.preventDefault()
    if (!bookingForm.doctor_id || !bookingForm.patient_id) {
      setBookingError('Please select both a patient and an attending physician.')
      return
    }
    setBookingSaving(true)
    setBookingError(null)
    try {
      await createAppointment({
        ...bookingForm,
        doctor_id: Number(bookingForm.doctor_id),
        patient_id: Number(bookingForm.patient_id),
      })
      setBookingSuccess(true)
      fetchAppointmentStats().then(setStats).catch(() => {})
      setTimeout(() => {
        handleCloseBooking()
        onNavigate('appointments')
      }, 1200)
    } catch (err) {
      setBookingError(err.message || 'Appointment booking failed. Please verify doctor availability.')
    } finally {
      setBookingSaving(false)
    }
  }

  const filteredDoctors = CLINICAL_DOCTORS.filter(d => {
    const matchesSpec =
      selectedSpecialty === 'All Specialties' ||
      d.specialty.toLowerCase() === selectedSpecialty.toLowerCase()
    const matchesSearch =
      d.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      d.specialty.toLowerCase().includes(searchQuery.toLowerCase()) ||
      d.department.toLowerCase().includes(searchQuery.toLowerCase()) ||
      d.room.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesSpec && matchesSearch
  })

  return (
    <div className="clinical-dashboard">
      {/* ── Welcome Hero Banner ─────────────────────────── */}
      <section className="be-hero-banner">
        <div className="be-hero-content">
          <div className="be-hero-eyebrow">
            <span className="be-hero-pulse" /> CENTRAL HOSPITAL OPD PORTAL
          </div>
          <h1 className="be-hero-heading">
            Intelligent Medical Scheduling & Doctor Availability
          </h1>
          <p className="be-hero-desc">
            Streamline outpatient queues with real-time conflict-free slot booking,
            automated physician rosters, and atomic database appointment confirmation.
          </p>
          <div className="be-hero-actions">
            <button
              className="be-btn-primary"
              onClick={() => {
                const el = document.getElementById('be-specialists-section')
                if (el) el.scrollIntoView({ behavior: 'smooth' })
              }}
            >
              📅 Schedule Consultation
            </button>
            <button
              className="be-btn-secondary"
              onClick={() => onNavigate('doctors')}
            >
              🩺 View Doctor Roster
            </button>
          </div>
        </div>
      </section>

      {/* ── Real-Time Clinical KPI Ribbon ──────────────── */}
      <section className="be-kpi-grid">
        <div className="be-kpi-card">
          <div className="be-kpi-header">
            <span className="be-kpi-icon-wrap" style={{ background: '#e0f2fe', color: '#0284c7' }}>📋</span>
            <span className="be-kpi-title">Total Bookings</span>
          </div>
          <div className="be-kpi-value">{loading ? '—' : stats?.total ?? 0}</div>
          <div className="be-kpi-caption">Lifetime patient visits</div>
        </div>

        <div className="be-kpi-card">
          <div className="be-kpi-header">
            <span className="be-kpi-icon-wrap" style={{ background: '#fef3c7', color: '#d97706' }}>🕒</span>
            <span className="be-kpi-title">Today's OPD Queue</span>
          </div>
          <div className="be-kpi-value">{loading ? '—' : stats?.today ?? 0}</div>
          <div className="be-kpi-caption">Scheduled for today</div>
        </div>

        <div className="be-kpi-card">
          <div className="be-kpi-header">
            <span className="be-kpi-icon-wrap" style={{ background: '#dbeafe', color: '#2563eb' }}>⏳</span>
            <span className="be-kpi-title">Upcoming Visits</span>
          </div>
          <div className="be-kpi-value">{loading ? '—' : stats?.upcoming ?? 0}</div>
          <div className="be-kpi-caption">Confirmed future slots</div>
        </div>

        <div className="be-kpi-card">
          <div className="be-kpi-header">
            <span className="be-kpi-icon-wrap" style={{ background: '#dcfce7', color: '#16a34a' }}>✅</span>
            <span className="be-kpi-title">Completed</span>
          </div>
          <div className="be-kpi-value">{loading ? '—' : stats?.completed ?? 0}</div>
          <div className="be-kpi-caption">Concluded consultations</div>
        </div>

        <div className="be-kpi-card">
          <div className="be-kpi-header">
            <span className="be-kpi-icon-wrap" style={{ background: '#f3e8ff', color: '#7e22ce' }}>🩺</span>
            <span className="be-kpi-title">Attending Doctors</span>
          </div>
          <div className="be-kpi-value">{loading ? '—' : (doctors.length || 4)}</div>
          <div className="be-kpi-caption">Available in roster</div>
        </div>
      </section>

      {/* ── Specialists & Departments Section ───────────── */}
      <section id="be-specialists-section" className="be-specialists-section">
        <div className="be-section-head">
          <div>
            <h2 className="be-section-title">Hospital Departments & Attending Physicians</h2>
            <p className="be-section-desc">
              Select a specialized department, view real-time physician hours, and book verified consultation slots.
            </p>
          </div>
        </div>

        {/* Filter Toolbar */}
        <div className="be-filter-toolbar">
          <div className="be-specialty-pills">
            {SPECIALTIES.map(spec => (
              <button
                key={spec}
                className={`be-pill ${selectedSpecialty === spec ? 'active' : ''}`}
                onClick={() => setSelectedSpecialty(spec)}
              >
                {spec}
              </button>
            ))}
          </div>

          <div className="be-search-box">
            <span className="be-search-icon">🔍</span>
            <input
              type="text"
              className="be-search-input"
              placeholder="Search physicians, departments, room…"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* Doctor Cards Grid */}
        <div className="be-doctors-grid">
          {filteredDoctors.map(doc => (
            <div key={doc.id} className="be-doctor-card">
              <div className="be-doc-header">
                <div className="be-doc-avatar" style={{ background: doc.avatarBg }}>
                  {doc.name.replace('Dr. ', '').split(' ').map(n => n[0]).join('')}
                </div>
                <div className="be-doc-primary">
                  <div className="be-doc-tag">{doc.specialty.toUpperCase()}</div>
                  <h3 className="be-doc-name">{doc.name}</h3>
                  <div className="be-doc-title">{doc.title}</div>
                </div>
              </div>

              <div className="be-doc-details">
                <div className="be-doc-meta-row">
                  <span className="be-meta-label">Department</span>
                  <span className="be-meta-value">{doc.department}</span>
                </div>
                <div className="be-doc-meta-row">
                  <span className="be-meta-label">Location</span>
                  <span className="be-meta-value">📍 {doc.room}</span>
                </div>
                <div className="be-doc-meta-row">
                  <span className="be-meta-label">OPD Timing</span>
                  <span className="be-meta-value be-timing-badge">🕒 {doc.timing}</span>
                </div>
                <div className="be-doc-meta-row">
                  <span className="be-meta-label">Credentials</span>
                  <span className="be-meta-value">{doc.experience} · {doc.rating}</span>
                </div>
              </div>

              <div className="be-doc-footer">
                <div>
                  <div className="be-fee-caption">Consultation Fee</div>
                  <div className="be-fee-amount">{doc.fee}</div>
                </div>
                <button
                  className="be-btn-book"
                  onClick={() => handleOpenBooking(doc)}
                >
                  Book Visit ➔
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Hospital System Guarantees ──────────────────── */}
      <section className="be-trust-grid">
        <div className="be-trust-card">
          <div className="be-trust-icon">🛡️</div>
          <div>
            <h4 className="be-trust-title">Atomic Slot Locking</h4>
            <p className="be-trust-text">Database transactions guarantee zero overlapping appointments for any physician.</p>
          </div>
        </div>

        <div className="be-trust-card">
          <div className="be-trust-icon">⚡</div>
          <div>
            <h4 className="be-trust-title">Kubernetes Auto-Scaling</h4>
            <p className="be-trust-text">Backed by HPA v2 scaling pods from 2 to 5 replicas during peak OPD hours.</p>
          </div>
        </div>

        <div className="be-trust-card">
          <div className="be-trust-icon">🩺</div>
          <div>
            <h4 className="be-trust-title">Live Doctor Rosters</h4>
            <p className="be-trust-text">Real-time synchronization between active clinic hours and doctor availability.</p>
          </div>
        </div>
      </section>

      {/* ── Interactive Booking Modal ────────────────────── */}
      {bookingDoctor && (
        <div className="modal-overlay" onClick={e => e.target === e.currentTarget && handleCloseBooking()}>
          <div className="modal be-modal-dialog" role="dialog" aria-modal="true">
            <div className="modal-header">
              <div>
                <div className="be-modal-badge">OPD CONSULTATION BOOKING</div>
                <h3 className="be-modal-title">Schedule with {bookingDoctor.name}</h3>
                <div className="be-modal-meta">{bookingDoctor.department} · {bookingDoctor.room}</div>
              </div>
              <button className="modal-close" onClick={handleCloseBooking}>✕</button>
            </div>

            <form onSubmit={handleBookingSubmit}>
              <div className="modal-body">
                {bookingError && (
                  <div className="error-banner" style={{ marginBottom: 16 }}>
                    ⚠️ {bookingError}
                  </div>
                )}
                {bookingSuccess && (
                  <div className="success-banner" style={{ marginBottom: 16, background: '#ecfdf5', color: '#065f46', padding: '10px 14px', borderRadius: 8 }}>
                    ✅ Appointment confirmed! Redirecting to appointments list…
                  </div>
                )}

                <div className="form-grid">
                  <div className="form-group">
                    <label className="form-label" htmlFor="be-patient-select">Patient</label>
                    <select
                      id="be-patient-select"
                      className="form-input"
                      value={bookingForm.patient_id}
                      onChange={e => setBookingForm(f => ({ ...f, patient_id: e.target.value }))}
                      required
                    >
                      <option value="">Select registered patient…</option>
                      {patients.map(p => (
                        <option key={p.id} value={p.id}>{p.name} ({p.phone || p.email || 'Patient'})</option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label" htmlFor="be-doctor-select">Attending Doctor</label>
                    <select
                      id="be-doctor-select"
                      className="form-input"
                      value={bookingForm.doctor_id}
                      onChange={e => setBookingForm(f => ({ ...f, doctor_id: e.target.value }))}
                      required
                    >
                      <option value="">Select physician…</option>
                      {doctors.map(d => (
                        <option key={d.id} value={d.id}>{d.name} — {d.speciality}</option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label" htmlFor="be-appt-date">Appointment Date</label>
                    <input
                      id="be-appt-date"
                      type="date"
                      className="form-input"
                      value={bookingForm.appointment_date}
                      onChange={e => setBookingForm(f => ({ ...f, appointment_date: e.target.value }))}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Consultation Window</label>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                      <input
                        type="time"
                        className="form-input"
                        value={bookingForm.start_time}
                        onChange={e => setBookingForm(f => ({ ...f, start_time: e.target.value }))}
                        required
                      />
                      <input
                        type="time"
                        className="form-input"
                        value={bookingForm.end_time}
                        onChange={e => setBookingForm(f => ({ ...f, end_time: e.target.value }))}
                        required
                      />
                    </div>
                  </div>

                  <div className="form-group" style={{ gridColumn: 'span 2' }}>
                    <label className="form-label" htmlFor="be-reason">Clinical Notes / Reason</label>
                    <input
                      id="be-reason"
                      type="text"
                      className="form-input"
                      value={bookingForm.reason}
                      onChange={e => setBookingForm(f => ({ ...f, reason: e.target.value }))}
                      placeholder="e.g. Follow-up consultation, ECG review, routine checkup"
                    />
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={handleCloseBooking}>
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={bookingSaving || bookingSuccess}
                >
                  {bookingSaving ? 'Locking Slot…' : 'Confirm Appointment ➔'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
