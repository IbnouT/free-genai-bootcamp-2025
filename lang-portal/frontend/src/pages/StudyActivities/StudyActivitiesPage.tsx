import { Box } from '@mui/material'
import { PageHeader } from '../../components'
import SchoolIcon from '@mui/icons-material/School'

function StudyActivitiesPage() {
  return (
    <Box 
      sx={{ 
        minHeight: 'calc(100vh - 64px)',  // Full viewport minus topbar
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <PageHeader 
        title="Study Activities" 
        icon={<SchoolIcon />}
        description="Manage and track your learning activities"
      />
      {/* Content */}
    </Box>
  )
}

export default StudyActivitiesPage 