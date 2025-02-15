import { AppBar, Toolbar, Typography, IconButton, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Logo from './common/Logo';

interface TopbarProps {
    title?: string;
}

export default function Topbar({ title = "Learning Portal" }: TopbarProps) {
    const navigate = useNavigate();

    return (
        <AppBar 
            position="static" 
            elevation={0}
        >
            <Toolbar sx={{ display: 'flex', alignItems: 'center' }}>
                <IconButton
                    color="inherit"
                    onClick={() => navigate('/')}
                    edge="start"
                    sx={{ 
                        mr: 2,
                        '&:hover': {
                            backgroundColor: 'transparent'
                        }
                    }}
                    disableRipple
                >
                    <Logo color="white" />
                </IconButton>

                {title && (
                    <Box sx={{ flexGrow: 1, textAlign: 'center' }}>
                        <Typography 
                            variant="h5"
                            component="div"
                            sx={{ 
                                color: 'common.white',
                                fontWeight: 500
                            }}
                        >
                            {title}
                        </Typography>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    );
}
