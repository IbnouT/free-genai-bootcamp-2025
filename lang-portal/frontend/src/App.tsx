import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { Box, Container } from '@mui/material'
import { theme } from './theme'
import Topbar from './components/Topbar'
import Sidebar from './components/Sidebar'

function App({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Topbar />
      <Box sx={{ 
        display: 'flex',
        minHeight: '100vh'
      }}>
        <Sidebar />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            marginLeft: '240px'  // Match sidebar width
          }}
        >
          {children}
        </Box>
      </Box>
    </ThemeProvider>
  )
}

export default App 