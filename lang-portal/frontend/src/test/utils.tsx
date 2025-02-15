import { ReactElement } from 'react'
import { render } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
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