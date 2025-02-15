import { Language } from '../types/language'
import { ApiError } from '../types/api'

const BASE_URL = '/languages'  // Base URL for language endpoints

export async function getActiveLanguages(): Promise<{ data?: Language[], error?: ApiError }> {
    try {
        const response = await fetch(`${BASE_URL}?active=true`)
        if (!response.ok) {
            return {
                error: {
                    message: 'Failed to fetch languages',
                    status: response.status
                }
            }
        }
        const data = await response.json()
        return { data }
    } catch (e) {
        return {
            error: {
                message: 'Network error while fetching languages',
                status: 0
            }
        }
    }
} 