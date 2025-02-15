import { Box, Button } from '@mui/material';
import Logo from '../../../components/common/Logo';

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
            <Logo />
            
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