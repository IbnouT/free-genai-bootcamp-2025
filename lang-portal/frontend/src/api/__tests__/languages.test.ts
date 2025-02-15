import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { getActiveLanguages } from '../languages'

describe('Language API', () => {
    const mockLanguages = [
        { code: "ja", name: "Japanese", active: true },
        { code: "fr", name: "French", active: true }
    ]

    beforeEach(() => {
        global.fetch = vi.fn()
    })

    afterEach(() => {
        vi.clearAllMocks()
    })

    it('returns languages on successful fetch', async () => {
        global.fetch = vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockLanguages)
            }) as any
        )

        const result = await getActiveLanguages()
        expect(result.data).toEqual(mockLanguages)
        expect(result.error).toBeUndefined()
    })

    it('returns error on failed fetch', async () => {
        global.fetch = vi.fn(() =>
            Promise.resolve({
                ok: false,
                status: 500
            }) as any
        )

        const result = await getActiveLanguages()
        expect(result.data).toBeUndefined()
        expect(result.error).toBeDefined()
        expect(result.error?.status).toBe(500)
    })
}) 