import { Typography, Box } from '@mui/material'
import DashboardIcon from '@mui/icons-material/Dashboard'
import { PageHeader } from '../../components'

function DashboardPage() {
  return (
    <Box>
      <PageHeader 
        title="Dashboard" 
        icon={<DashboardIcon />}
        description="Overview of your learning progress and activities"
      />
      
      <Box sx={{ px: 3 }}>  {/* Add padding container for content */}
        {/* Temporary content for scroll testing */}
        {[...Array(20)].map((_, index) => (
          <Box key={index} sx={{ mb: 4 }}>
            <Typography variant="h6">
              Section {index + 1}
            </Typography>
            <Typography>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do 
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim 
              ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut 
              aliquip ex ea commodo consequat.
            </Typography>
          </Box>
        ))}
      </Box>
    </Box>
  )
}

export default DashboardPage 