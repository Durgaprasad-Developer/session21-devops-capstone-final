import { useState, useEffect } from 'react'
import { fetchAppointmentStats } from '../api.js'

const KPI_CONFIG = [
  { key: 'total',     label: 'Total Appointments', icon: '📋', color: '#6366f1' },
  { key: 'today',     label: "Today's Appointments", icon: '📅', color: '#0ea5e9' },
  { key: 'upcoming',  label: 'Upcoming',             icon: '⏳', color: '#f59e0b' },
  { key: 'completed', label: 'Completed',             icon: '✅', color: '#22c55e' },
  { key: 'cancelled', label: 'Cancelled',             icon: '❌', color: '#ef4444' },
]

export default function Dashboard({ onNavigate }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAppointmentStats()
      .then(setStats)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      {error && <div className="error-banner">⚠️ {error}</div>}

      {/* KPI cards */}
      <div className="kpi-grid">
        {KPI_CONFIG.map(({ key, label, icon, color }) => (
          <div className="kpi-card" key={key} style={{ '--kpi-color': color }}>
            <div className="kpi-icon">{icon}</div>
            <div className="kpi-label">{label}</div>
            <div className="kpi-value">
              {loading ? '—' : stats?.[key] ?? 0}
            </div>
          </div>
        ))}
      </div>

      {/* Quick links */}
      <div className="kpi-grid" style={{ marginBottom: 0 }}>
        {[
          { label: 'New Appointment', icon: '➕', page: 'appointments', color: '#6366f1' },
          { label: 'Manage Doctors',  icon: '🩺', page: 'doctors',      color: '#0ea5e9' },
          { label: 'Manage Patients', icon: '👤', page: 'patients',     color: '#22c55e' },
        ].map(({ label, icon, page, color }) => (
          <div
            key={page}
            className="kpi-card"
            style={{ '--kpi-color': color, cursor: 'pointer' }}
            onClick={() => onNavigate(page)}
          >
            <div className="kpi-icon">{icon}</div>
            <div className="kpi-label" style={{ fontSize: 13, fontWeight: 600, color: '#475569', textTransform: 'none', letterSpacing: 0 }}>
              {label}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
