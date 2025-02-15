import { Card, CardContent, CardActionArea, Typography } from '@mui/material';
import { Language } from '../../types/language';

interface LanguageCardProps {
    language: Language;
    onSelect: () => void;
}

export default function LanguageCard({ language, onSelect }: LanguageCardProps) {
    return (
        <Card>
            <CardActionArea onClick={onSelect}>
                <CardContent>
                    <Typography variant="h5" component="div">
                        {language.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {language.code.toUpperCase()}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
} 