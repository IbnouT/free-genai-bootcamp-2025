import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import App from './App'

// Placeholder components for our routes
const Dashboard = () => <div>Dashboard Page</div>
const StudyActivities = () => <div>Study Activities Page</div>
const Words = () => <div>Words Page</div>
const Groups = () => <div>Groups Page</div>
const Sessions = () => <div>Sessions Page</div>
const Settings = () => <div>Settings Page</div>

function AppRoutes() {
  return (
    <Router>
      <App>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/study-activities" element={<StudyActivities />} />
          <Route path="/words" element={<Words />} />
          <Route path="/groups" element={<Groups />} />
          <Route path="/sessions" element={<Sessions />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </App>
    </Router>
  )
}

export default AppRoutes 