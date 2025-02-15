import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid, Typography, Alert, CircularProgress, Box } from '@mui/material';
import { useLanguage } from '../../context/LanguageContext';
import { Language } from '../../types/language';
import { ApiError } from '../../types/api';
import { getActiveLanguages } from '../../api/languages';
import LanguageCard from './components/LanguageCard';

export default function LanguageSelectionPage() {
    const [languages, setLanguages] = useState<Language[]>([]);
    const { setLanguage } = useLanguage();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<ApiError | null>(null);

    useEffect(() => {
        console.log('LanguageSelectionPage mounted');
        loadLanguages();
    }, []);

    async function loadLanguages() {
        try {
            console.log('Loading languages...');
            const result = await getActiveLanguages();
            console.log('Languages loaded:', result);
            if (result.data) {
                setLanguages(result.data);
            }
        } catch (error) {
            console.error('Failed to load languages:', error);
        } finally {
            setLoading(false);
        }
    }

    const handleLanguageSelect = (code: string) => {
        setLanguage(code);
        navigate('/dashboard');  // Change from '/words' to '/dashboard'
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box p={3}>
                <Alert severity="error">
                    {error.message}
                </Alert>
                <Typography mt={2}>
                    Please try refreshing the page or contact support if the problem persists.
                </Typography>
            </Box>
        );
    }

    if (languages.length === 0) {
        return (
            <Box p={3}>
                <Alert severity="info">
                    No languages are currently available.
                </Alert>
            </Box>
        );
    }

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