import { Card, CardContent, CardActionArea, Typography, Box } from '@mui/material';
import { Language } from '../../../types/language';

interface LanguageCardProps {
    language: Language;
    onSelect: () => void;
}

export default function LanguageCard({ language, onSelect }: LanguageCardProps) {
    return (
        <Card 
            elevation={3}
            sx={{ 
                height: '100%',
                transition: 'transform 0.2s',
                '&:hover': {
                    transform: 'scale(1.02)',
                }
            }}
        >
            <CardActionArea 
                onClick={onSelect}
                sx={{ height: '100%', padding: 2 }}
            >
                <CardContent>
                    <Typography variant="h4" gutterBottom>
                        {language.name}
                    </Typography>
                    <Box sx={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        gap: 1,
                        color: 'text.secondary'
                    }}>
                        <Typography variant="subtitle1">
                            {language.code.toUpperCase()}
                        </Typography>
                    </Box>
                </CardContent>
            </CardActionArea>
        </Card>
    );
} 