import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'

function Topbar() {
  return (
    <AppBar 
      position="static" 
      elevation={0}  // Remove shadow
    >
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Language Learning Portal
        </Typography>
      </Toolbar>
    </AppBar>
  )
}

export default Topbar
