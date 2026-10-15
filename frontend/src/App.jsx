import { useState } from 'react'
import Dashboard from './pages/Dashboard.jsx'
import Appointments from './pages/Appointments.jsx'
import Doctors from './pages/Doctors.jsx'
import Patients from './pages/Patients.jsx'

const NAV = [
  { id: 'dashboard',    label: 'Dashboard',    icon: '📊' },
  { id: 'appointments', label: 'Appointments', icon: '📅' },
  { id: 'doctors',      label: 'Doctors',      icon: '🩺' },
  { id: 'patients',     label: 'Patients',     icon: '👥' },
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
    <div className="bookease-layout">
      {/* ── Navy Blue Clinical Sidebar ──────────────────── */}
      <aside className="be-sidebar">
        <div className="be-sidebar-top">
          <div className="be-brand">
            <div className="be-brand-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="24" height="24" rx="6" fill="#0284c7" />
                <path d="M12 6V18M6 12H18" stroke="#ffffff" strokeWidth="2.8" strokeLinecap="round" />
              </svg>
            </div>
            <div>
              <div className="be-brand-name">BookEase</div>
              <div className="be-brand-tag">Clinical Scheduling</div>
            </div>
          </div>

          <div className="be-nav-heading">MAIN MENU</div>

          <nav className="be-nav">
            {NAV.map(item => {
              const isActive = page === item.id
              return (
                <button
                  key={item.id}
                  className={`be-nav-item ${isActive ? 'active' : ''}`}
                  onClick={() => setPage(item.id)}
                >
                  <span className="be-nav-icon">{item.icon}</span>
                  <span className="be-nav-label">{item.label}</span>
                  {isActive && <span className="be-nav-indicator" />}
                </button>
              )
            })}
          </nav>
        </div>

        {/* ── Hospital Emergency & On-Duty Card ─────────── */}
        <div className="be-sidebar-duty-card">
          <div className="be-duty-header">
            <span className="be-duty-dot" />
            <span className="be-duty-title">24/7 OPD Active</span>
          </div>
          <p className="be-duty-desc">
            Central Hospital OPD Wing is accepting patient bookings and emergency consultations.
          </p>
          <button
            className="be-duty-btn"
            onClick={() => setPage('appointments')}
          >
            + Quick Appointment
          </button>
        </div>

        {/* ── User & System Status Footer ──────────────── */}
        <div className="be-sidebar-footer">
          <div className="be-user-card">
            <div className="be-user-avatar">OP</div>
            <div className="be-user-meta">
              <div className="be-user-name">OPD Reception</div>
              <div className="be-user-role">Central Hospital Admin</div>
            </div>
          </div>
          <div className="be-system-tag">
            <span className="be-status-dot" /> Microservices Live (Kubernetes)
          </div>
        </div>
      </aside>

      {/* ── Main Viewport Area ─────────────────────────── */}
      <div className="be-main-wrapper">
        {/* Top Navbar */}
        <header className="be-topbar">
          <div className="be-topbar-left">
            <div className="be-campus-badge">
              <span className="be-campus-icon">🏥</span>
              <span>Central Hospital — Main OPD Campus</span>
              <span className="be-campus-arrow">⌄</span>
            </div>
          </div>

          <div className="be-topbar-right">
            <div className="be-badge-online">
              <span className="be-pulse-circle" /> API v1.0.0 Online
            </div>
            {page !== 'appointments' && (
              <button
                className="be-btn-primary-top"
                onClick={() => setPage('appointments')}
              >
                + New Appointment
              </button>
            )}
          </div>
        </header>

        {/* Dynamic Page Content */}
        <main className="be-page-container">
          {page !== 'dashboard' && (
            <div className="be-page-header">
              <h1 className="be-page-title">{current?.label}</h1>
              <p className="be-page-subtitle">Hospital administration and patient queue management</p>
            </div>
          )}
          {pages[page]}
        </main>
      </div>
    </div>
  )
}
