import { Box, Button, Typography } from '@mui/material';
import LanguageIcon from '@mui/icons-material/Language';

export default function Header() {
    return (
        <Box 
            sx={{ 
                width: '100%',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '1rem 2rem',
                borderBottom: '1px solid',
                borderColor: 'divider',
                backgroundColor: 'background.paper',
                boxSizing: 'border-box'
            }}
        >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LanguageIcon sx={{ fontSize: 28, color: 'primary.main' }} />
                <Typography 
                    variant="h6" 
                    fontWeight="bold"
                    color="primary"
                >
                    LangLearner
                </Typography>
            </Box>
            
            <Button 
                variant="text"
                sx={{
                    whiteSpace: 'nowrap',
                    minWidth: 80,
                    padding: '6px 16px',
                    marginLeft: 'auto'
                }}
            >
                About
            </Button>
        </Box>
    );
} 