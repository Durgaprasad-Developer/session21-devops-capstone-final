import { useState } from 'react'
import Dashboard from './pages/Dashboard.jsx'
import Appointments from './pages/Appointments.jsx'
import Doctors from './pages/Doctors.jsx'
import Patients from './pages/Patients.jsx'

const NAV = [
  { id: 'dashboard',    label: 'Dashboard',     icon: '📊' },
  { id: 'appointments', label: 'Appointments',  icon: '📅' },
  { id: 'doctors',      label: 'Doctors',       icon: '🩺' },
  { id: 'patients',     label: 'Patients',      icon: '👤' },
]

export default function App() {
  const [page, setPage] = useState('dashboard')

  const pages = {
    dashboard:    <Dashboard onNavigate={setPage} />,
    appointments: <Appointments />,
    doctors:      <Doctors />,
    patients:     <Patients />,
  }

  const current = NAV.find(n => n.id === page)

  return (
    <div className="app-layout">
      {/* ── Sidebar ───────────────────────────────────── */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">📋</div>
          <div>
            <h1>BookEase</h1>
            <span>Appointment System</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-section-label">Navigation</div>
          {NAV.map(item => (
            <button
              key={item.id}
              className={`nav-item ${page === item.id ? 'active' : ''}`}
              onClick={() => setPage(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      {/* ── Main Content ──────────────────────────────── */}
      <div className="main-content">
        <header className="header">
          <div>
            <div className="header-title">{current?.label}</div>
            <div className="header-subtitle">Manage your {current?.label.toLowerCase()}</div>
          </div>
        </header>

        <main className="page">
          {pages[page]}
        </main>
      </div>
    </div>
  )
}
