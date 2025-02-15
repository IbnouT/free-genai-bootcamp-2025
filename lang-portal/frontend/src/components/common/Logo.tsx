import { Box, Typography } from '@mui/material';
import LanguageIcon from '@mui/icons-material/Language';

interface LogoProps {
    variant?: 'default' | 'small';
    color?: 'primary' | 'white';
}

export default function Logo({ variant = 'default', color = 'primary' }: LogoProps) {
    return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <LanguageIcon 
                sx={{ 
                    fontSize: variant === 'small' ? 24 : 28,
                    color: color === 'primary' ? 'primary.main' : 'common.white'
                }} 
            />
            <Typography 
                variant={variant === 'small' ? 'subtitle1' : 'h6'}
                fontWeight="bold"
                color={color === 'primary' ? 'primary.main' : 'common.white'}
            >
                LangLearner
            </Typography>
        </Box>
    );
} 