import { Box, Typography, Paper } from '@mui/material';
import { ReactNode } from 'react';

interface PageHeaderProps {
  title: string;
  icon: ReactNode;
  description?: string;
}

function PageHeader({ title, icon, description }: PageHeaderProps) {
  return (
    <Paper 
      elevation={0}
      sx={{
        ml: 2,
        mb: 2,
        width: '100%',
        bgcolor: 'background.default',
        borderRadius: 0,
        borderBottom: 1,
        borderColor: 'divider',
      }}
    >
      <Box
        sx={{
          p: 2,
          pr: 0,
          display: 'flex',
          alignItems: 'center',
          gap: 2,
        }}
      >
        <Box 
          sx={{ 
            p: 1.5,
            borderRadius: 1.5,
            bgcolor: 'primary.main',
            color: 'white',
            display: 'flex',
            '& > svg': {
              fontSize: 28,
            }
          }}
        >
          {icon}
        </Box>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
          <Typography 
            variant="h5" 
            sx={{ 
              fontWeight: 500,
              lineHeight: 1.2,
            }}
          >
            {title}
          </Typography>
          {description && (
            <Typography 
              variant="body1" 
              color="text.secondary"
              sx={{ lineHeight: 1.2 }}
            >
              {description}
            </Typography>
          )}
        </Box>
      </Box>
    </Paper>
  );
}

export default PageHeader; 