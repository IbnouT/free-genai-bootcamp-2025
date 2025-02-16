import { Card, Box, Typography } from '@mui/material';
import { Language } from '../../../types/language';

interface LanguageCardProps {
    language: Language;
    selected: boolean;
    onSelect: () => void;
}

export default function LanguageCard({ language, selected, onSelect }: LanguageCardProps) {
    return (
        <Card
            onClick={onSelect}
            data-testid="language-card"
            sx={{
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'flex-start',
                padding: 3,
                gap: 3,
                minHeight: 120,
                border: '1px solid',
                borderColor: selected ? 'primary.main' : 'divider',
                borderRadius: '16px',
                backgroundColor: 'background.paper',
                boxShadow: selected ? 2 : 1,
                transition: 'all 0.2s ease-in-out',
                '&:hover': {
                    boxShadow: 2,
                    borderColor: 'primary.light',
                    backgroundColor: 'action.hover'
                }
            }}
        >
            <Box 
                sx={{ 
                    width: { xs: 40, sm: 48 },
                    height: { xs: 40, sm: 48 },
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginTop: 1
                }}
            >
                <img 
                    src={`/src/images/${language.code}.png`} 
                    alt={`${language.name} flag`}
                    style={{ 
                        width: '100%', 
                        height: '100%', 
                        objectFit: 'contain'
                    }}
                />
            </Box>
            
            <Box sx={{ flex: 1 }}>
                <Typography variant="h5" gutterBottom fontWeight="bold">
                    {language.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" lineHeight={1.6}>
                    {language.promo_text}
                </Typography>
            </Box>
        </Card>
    );
} 