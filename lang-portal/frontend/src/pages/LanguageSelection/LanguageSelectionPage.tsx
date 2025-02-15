import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid, Typography, Alert, CircularProgress, Box, Button } from '@mui/material';
import { useLanguage } from '../../context/LanguageContext';
import { Language } from '../../types/language';
import { ApiError } from '../../types/api';
import { getActiveLanguages } from '../../api/languages';
import LanguageCard from './components/LanguageCard';
import Header from './components/Header';

export default function LanguageSelectionPage() {
    const [languages, setLanguages] = useState<Language[]>([]);
    const { setLanguage } = useLanguage();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<ApiError | null>(null);
    const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);

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
        setSelectedLanguage(code);
    };

    const handleStartSession = () => {
        if (selectedLanguage) {
            setLanguage(selectedLanguage);
            navigate('/dashboard');
        }
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
        <Box sx={{ 
            minHeight: '100vh', 
            display: 'flex', 
            flexDirection: 'column',
            maxWidth: '100vw',  // Ensure it doesn't exceed viewport width
            overflow: 'hidden'  // Prevent horizontal scrolling
        }}>
            <Header />
            
            <Box 
                sx={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    padding: {
                        xs: '2rem 1rem',
                        sm: '3rem 2rem',
                        md: '4rem 2rem'
                    },
                    maxWidth: 1200,
                    margin: '0 auto',
                    width: '100%',
                    boxSizing: 'border-box'  // Include padding in width calculation
                }}
            >
                <Typography 
                    variant="h2" 
                    gutterBottom 
                    sx={{ 
                        textAlign: 'center',
                        fontWeight: 'bold',
                        mb: 6,
                        fontSize: {
                            xs: '2rem',    // smaller on mobile
                            sm: '2.5rem',
                            md: '3rem'
                        }
                    }}
                >
                    Select your learning language
                </Typography>
                
                <Grid container spacing={3} sx={{ width: '100%' }}>
                    {languages.map(lang => (
                        <Grid item xs={12} md={6} key={lang.code}>
                            <LanguageCard 
                                language={lang}
                                selected={selectedLanguage === lang.code}
                                onSelect={() => handleLanguageSelect(lang.code)}
                            />
                        </Grid>
                    ))}
                </Grid>

                <Button
                    variant="contained"
                    size="large"
                    disabled={!selectedLanguage}
                    onClick={handleStartSession}
                    sx={{
                        mt: 6,
                        py: 2,
                        px: 6,
                        borderRadius: 50,
                        fontSize: '1rem',
                        textTransform: 'uppercase',
                        backgroundColor: '#1976d2',
                        '&:hover': {
                            backgroundColor: '#1565c0'
                        }
                    }}
                >
                    Proceed to Session Start
                </Button>
            </Box>

            <Box 
                sx={{ 
                    padding: '1rem',
                    textAlign: 'center',
                    borderTop: '1px solid',
                    borderColor: 'divider'
                }}
            >
                <Typography variant="body2" color="text.secondary">
                    © {new Date().getFullYear()} LangLearning. All rights reserved.
                </Typography>
            </Box>
        </Box>
    );
} 