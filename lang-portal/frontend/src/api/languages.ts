import { Language } from '../types/language'
import { ApiError } from '../types/api'
import { config } from '../config'

const BASE_URL = `${config.apiUrl}/languages`

export async function getActiveLanguages(): Promise<{ data?: Language[], error?: ApiError }> {
    console.log('Fetching languages...')
    try {
        const response = await fetch(`${BASE_URL}?active=true`)
        console.log('API Response:', response)
        if (!response.ok) {
            return {
                error: {
                    message: 'Failed to fetch languages',
                    status: response.status
                }
            }
        }
        const data = await response.json()
        console.log('Languages data:', data)
        return { data }
    } catch (error) {
        console.error('Error fetching languages:', error)
        return {
            error: {
                message: 'Network error while fetching languages',
                status: 0
            }
        }
    }
} 