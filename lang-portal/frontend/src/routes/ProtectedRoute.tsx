import { Navigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { ReactNode } from 'react';

interface ProtectedRouteProps {
    children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
    const { currentLanguage } = useLanguage();

    if (!currentLanguage) {
        return <Navigate to="/select-language" replace />;
    }

    return <>{children}</>;
} 