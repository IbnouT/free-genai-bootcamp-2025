import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import App from './App'
import Layout from './components/Layout'
import DashboardPage from './pages/Dashboard/DashboardPage'

// Placeholder components for our routes
const StudyActivities = () => <div>Study Activities Page</div>
const Words = () => <div>Words Page</div>
const Groups = () => <div>Groups Page</div>
const Sessions = () => <div>Sessions Page</div>
const Settings = () => <div>Settings Page</div>

function AppRoutes() {
  return (
    <Router>
      <App>
        <Layout>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/study-activities" element={<StudyActivities />} />
            <Route path="/words" element={<Words />} />
            <Route path="/groups" element={<Groups />} />
            <Route path="/sessions" element={<Sessions />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </App>
    </Router>
  )
}

export default AppRoutes 