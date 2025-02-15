import { createRoot } from 'react-dom/client';
import AppRoutes from './routes';
import { LanguageProvider } from './context/LanguageContext';

const root = createRoot(document.getElementById('root')!);
root.render(
  <LanguageProvider>
    <AppRoutes />
  </LanguageProvider>
); 