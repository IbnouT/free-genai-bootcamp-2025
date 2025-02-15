import { Routes, Route, Navigate } from 'react-router-dom'
import App from './App'
import Layout from './components/Layout'
import DashboardPage from './pages/Dashboard/DashboardPage'
import StudyActivitiesPage from './pages/StudyActivities/StudyActivitiesPage'
import LanguageSelectionPage from './pages/LanguageSelection/LanguageSelectionPage'
import { useLanguage } from './context/LanguageContext'

// Placeholder components for our routes
const Words = () => <div>Words Page</div>
const Groups = () => <div>Groups Page</div>
const Sessions = () => <div>Sessions Page</div>
const Settings = () => <div>Settings Page</div>

// Protected route wrapper
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { currentLanguage } = useLanguage()
  
  if (!currentLanguage) {
    return <Navigate to="/languages" replace />
  }
  
  return <>{children}</>
}

function AppRoutes() {
  return (
    <Routes>
      {/* Add root redirect */}
      <Route path="/" element={<Navigate to="/languages" replace />} />
      
      {/* Language Selection */}
      <Route path="/languages" element={<LanguageSelectionPage />} />
      
      {/* Protected routes */}
      <Route path="/*" element={
        <ProtectedRoute>
          <App>
            <Routes>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/study-activities" element={<StudyActivitiesPage />} />
              <Route path="/words" element={<Words />} />
              <Route path="/groups" element={<Groups />} />
              <Route path="/sessions" element={<Sessions />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </App>
        </ProtectedRoute>
      } />
    </Routes>
  )
}

export default AppRoutes 