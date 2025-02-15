import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid, Typography } from '@mui/material';
import { useLanguage } from '../../context/LanguageContext';
import { Language } from '../../types/language';
import LanguageCard from './LanguageCard';

export default function LanguageSelectionPage() {
    const [languages, setLanguages] = useState<Language[]>([]);
    const { setLanguage } = useLanguage();
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch active languages
        fetch('/api/languages?active=true')
            .then(res => res.json())
            .then(data => setLanguages(data))
            .catch(console.error);
    }, []);

    const handleLanguageSelect = (code: string) => {
        setLanguage(code);
        navigate('/words');  // Redirect to words page after selection
    };

    return (
        <div style={{ padding: '2rem' }}>
            <Typography variant="h4" gutterBottom>
                Select a Language
            </Typography>
            <Grid container spacing={3}>
                {languages.map(lang => (
                    <Grid item xs={12} sm={6} md={4} key={lang.code}>
                        <LanguageCard 
                            language={lang}
                            onSelect={() => handleLanguageSelect(lang.code)}
                        />
                    </Grid>
                ))}
            </Grid>
        </div>
    );
} 