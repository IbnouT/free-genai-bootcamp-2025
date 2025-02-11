import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { Box, Container } from '@mui/material'
import { theme } from './theme'
import Topbar from './components/Topbar'
import Sidebar from './components/Sidebar'

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Topbar />
      <Box sx={{ display: 'flex' }}>
        <Sidebar />
        <Container sx={{ mt: 2 }}>
          {/* Future content will go here */}
        </Container>
      </Box>
    </ThemeProvider>
  )
}

export default App 