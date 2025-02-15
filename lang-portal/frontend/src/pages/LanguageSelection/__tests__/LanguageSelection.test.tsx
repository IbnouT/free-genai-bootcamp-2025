import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import LanguageSelectionPage from '../LanguageSelectionPage'
import { getActiveLanguages } from '../../../api/languages'
import { TestWrapper } from '../../../test/utils'

// Mock the API call
vi.mock('../../../api/languages')

// Mock navigation
const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom')
    return {
        ...actual,
        useNavigate: () => mockNavigate
    }
})

describe('Language Selection', () => {
    beforeEach(() => {
        vi.clearAllMocks()
        // Clear console to avoid noise in tests
        vi.spyOn(console, 'log').mockImplementation(() => {})
        vi.spyOn(console, 'error').mockImplementation(() => {})
    })

    afterEach(() => {
        vi.restoreAllMocks()
    })

    it('allows language selection and navigation', async () => {
        const mockLanguages = [
            { code: 'ja', name: 'Japanese', active: true },
            { code: 'fr', name: 'French', active: true }
        ]
        vi.mocked(getActiveLanguages).mockResolvedValue({ data: mockLanguages })

        render(<LanguageSelectionPage />, { wrapper: TestWrapper })

        // Wait for loading to complete
        await waitFor(() => {
            const languageCards = screen.getAllByTestId('language-card')
            expect(languageCards.length).toBe(mockLanguages.length)
        })

        // Get proceed button and verify initial disabled state
        const proceedButton = screen.getByTestId('proceed-button')
        expect(proceedButton).toBeDisabled()

        // Select first language card
        const languageCards = screen.getAllByTestId('language-card')
        fireEvent.click(languageCards[0])

        // Verify proceed button is now enabled and click it
        expect(proceedButton).not.toBeDisabled()
        fireEvent.click(proceedButton)

        // Verify navigation
        expect(mockNavigate).toHaveBeenCalledWith('/dashboard')
    })

    it('handles API errors', async () => {
        const mockError = { message: 'API Error', status: 500 };
        vi.mocked(getActiveLanguages).mockRejectedValue(mockError);

        render(<LanguageSelectionPage />, { wrapper: TestWrapper });

        await waitFor(() => {
            expect(screen.getByRole('alert')).toBeInTheDocument();
        });
    })
}) 