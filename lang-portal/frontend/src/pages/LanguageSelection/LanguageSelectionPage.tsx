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
        } catch (err) {
            console.error('Failed to load languages:', err);
            setError(err as ApiError);
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
            overflow: 'auto'
        }}>
            <Header />
            
            <Box 
                sx={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    padding: {
                        xs: '2rem 1rem',
                        sm: '2rem',
                        md: '2rem'
                    },
                    width: '100%',
                    maxWidth: '1200px',
                    mx: 'auto',
                    boxSizing: 'border-box'
                }}
            >
                <Box sx={{ width: '100%' }}>
                    <Typography 
                        variant="h2" 
                        gutterBottom 
                        sx={{ 
                            textAlign: 'center',
                            fontWeight: 'bold',
                            mb: 4,
                            fontSize: {
                                xs: '1.75rem',
                                sm: '2.25rem',
                                md: '2.75rem'
                            }
                        }}
                    >
                        Select your learning language
                    </Typography>
                    
                    <Box 
                        sx={{ 
                            width: '100%',
                            maxWidth: '900px',
                            mx: 'auto',
                            mb: 4
                        }}
                    >
                        <Grid 
                            container 
                            spacing={3}
                            justifyContent="center"
                        >
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
                    </Box>

                    <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                        <Button
                            variant="contained"
                            size="large"
                            disabled={!selectedLanguage}
                            onClick={handleStartSession}
                            data-testid="proceed-button"
                            sx={{
                                py: 1.25,
                                px: 4,
                                borderRadius: 50,
                                fontSize: '0.9rem',
                                textTransform: 'uppercase',
                                minWidth: {
                                    xs: '90%',
                                    sm: 250
                                }
                            }}
                        >
                            Proceed to Session Start
                        </Button>
                    </Box>
                </Box>
            </Box>

            <Box 
                sx={{ 
                    padding: '1rem',
                    textAlign: 'center',
                    borderTop: '1px solid',
                    borderColor: 'divider',
                    backgroundColor: 'background.paper'
                }}
            >
                <Typography variant="body2" color="text.secondary">
                    © {new Date().getFullYear()} LangLearning. All rights reserved.
                </Typography>
            </Box>
        </Box>
    );
} 