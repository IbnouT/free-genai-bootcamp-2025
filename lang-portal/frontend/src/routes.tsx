import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
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
    return <Navigate to="/select-language" replace />
  }
  
  return <>{children}</>
}

function AppRoutes() {
  return (
    <Router>
      <App>
        <Routes>
          {/* Public route - Language Selection */}
          <Route path="/select-language" element={<LanguageSelectionPage />} />
          
          {/* Protected routes - require language selection */}
          <Route path="/*" element={
            <ProtectedRoute>
              <Layout>
                <Routes>
                  <Route path="/" element={<Navigate to="/study" replace />} />
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/study-activities" element={<StudyActivitiesPage />} />
                  <Route path="/words" element={<Words />} />
                  <Route path="/groups" element={<Groups />} />
                  <Route path="/sessions" element={<Sessions />} />
                  <Route path="/settings" element={<Settings />} />
                </Routes>
              </Layout>
            </ProtectedRoute>
          } />
        </Routes>
      </App>
    </Router>
  )
}

export default AppRoutes 