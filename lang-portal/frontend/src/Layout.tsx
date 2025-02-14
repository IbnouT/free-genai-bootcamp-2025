import { Box, Typography } from '@mui/material'
import { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

function Layout({ children }: LayoutProps) {
  return (
    <Box sx={{ 
      minHeight: 'calc(100vh - 64px)',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <Box sx={{ flex: 1 }}>
        {children}
      </Box>
      {/* Footer */}
      <Box sx={{ 
        py: 0,
        textAlign: 'center',
        borderTop: '1px solid',
        borderColor: 'divider'
      }}>
        <Typography variant="body2" color="text.secondary">
          © 2024 Language Learning Portal. All rights reserved.
        </Typography>
      </Box>
    </Box>
  )
}

export default Layout 