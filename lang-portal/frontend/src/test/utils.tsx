import { ReactElement, ReactNode } from 'react'
import { render } from '@testing-library/react'
import { MemoryRouter, BrowserRouter } from 'react-router-dom'
import { LanguageProvider } from '../context/LanguageContext'

// Configure router with future flags
export const routerOptions = {
  future: {
    v7_startTransition: true,
    v7_relativeSplatPath: true
  }
}

export function renderWithProviders(ui: ReactElement) {
  const wrappedComponent = (
    <MemoryRouter {...routerOptions}>
      <LanguageProvider>{ui}</LanguageProvider>
    </MemoryRouter>
  )
  return render(wrappedComponent)
}

// Create a custom router with future flags enabled
const CustomRouter = ({ children }: { children: ReactNode }) => (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        {children}
    </BrowserRouter>
);

export const TestWrapper = ({ children }: { children: ReactNode }) => (
    <CustomRouter>
        <LanguageProvider>
            {children}
        </LanguageProvider>
    </CustomRouter>
); 