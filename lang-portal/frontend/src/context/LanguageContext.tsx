import { createContext, useContext, useState, ReactNode } from 'react';

interface LanguageContextType {
    currentLanguage: string | null;
    setLanguage: (code: string) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [currentLanguage, setCurrentLanguage] = useState<string | null>(() => {
        // Try to get from sessionStorage on init
        return sessionStorage.getItem('selectedLanguage');
    });

    const setLanguage = (code: string) => {
        sessionStorage.setItem('selectedLanguage', code);
        setCurrentLanguage(code);
    };

    return (
        <LanguageContext.Provider value={{ currentLanguage, setLanguage }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const context = useContext(LanguageContext);
    if (context === undefined) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
} 