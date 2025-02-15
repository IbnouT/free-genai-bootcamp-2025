import { describe, it, expect, beforeEach, vi } from 'vitest'
import { screen, waitFor, fireEvent } from '@testing-library/react'
import LanguageSelectionPage from '../LanguageSelectionPage'
import { renderWithProviders } from '../../../test/utils'

// Mock navigation
const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => ({
    ...(await vi.importActual('react-router-dom')),
    useNavigate: () => mockNavigate
}))

describe('Language Selection', () => {
    beforeEach(() => {
        mockNavigate.mockClear()
        global.fetch = vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve([
                    { code: "ja", active: true },
                    { code: "fr", active: true }
                ])
            }) as any
        )
    })

    it('allows selecting a language', async () => {
        renderWithProviders(<LanguageSelectionPage />)
        
        // Wait for languages to load
        await waitForLanguagesToLoad()
        
        // Select a language
        const languages = await screen.findAllByRole('button')
        fireEvent.click(languages[0])
        
        // Verify language selection triggered navigation
        expect(mockNavigate).toHaveBeenCalled()
    })

    it('handles API errors', async () => {
        global.fetch = vi.fn(() => Promise.reject())
        renderWithProviders(<LanguageSelectionPage />)
        
        // Verify error state
        await waitForLanguagesToLoad()
        expect(mockNavigate).not.toHaveBeenCalled()
    })
})

// Helper to wait for loading to finish
async function waitForLanguagesToLoad() {
    await waitFor(() => {
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument()
    })
} 