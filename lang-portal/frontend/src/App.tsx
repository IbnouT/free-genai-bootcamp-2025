import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { Typography, Container } from '@mui/material'
import { theme } from './theme'

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container>
        <Typography variant="h3" component="h1">
          Language Learning Portal
        </Typography>
      </Container>
    </ThemeProvider>
  )
}

export default App 