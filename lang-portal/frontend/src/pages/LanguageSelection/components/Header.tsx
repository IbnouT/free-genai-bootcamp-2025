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
                padding: {
                    xs: '1rem',
                    sm: '1rem 2rem'
                },
                borderBottom: '1px solid',
                borderColor: 'divider',
                maxWidth: '100vw',  // Ensure it doesn't exceed viewport width
                boxSizing: 'border-box'  // Include padding in width calculation
            }}
        >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LanguageIcon sx={{ fontSize: 32 }} />
                <Typography 
                    variant="h6" 
                    fontWeight="bold"
                    sx={{
                        fontSize: {
                            xs: '1.1rem',
                            sm: '1.25rem'
                        }
                    }}
                >
                    LangLearner
                </Typography>
            </Box>
            
            <Button 
                variant="text"
                sx={{
                    whiteSpace: 'nowrap',  // Prevent text wrapping
                    minWidth: 'auto'  // Allow button to shrink
                }}
            >
                About
            </Button>
        </Box>
    );
} 