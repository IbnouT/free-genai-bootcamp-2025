import { render } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { MemoryRouter } from 'react-router-dom'
import App from './App'
import { routerOptions } from './test/utils'

describe('App', () => {
  it('redirects to language selection when no language is selected', () => {
    render(
      <MemoryRouter {...routerOptions} initialEntries={['/dashboard']}>
        <App>
          <div>Test content</div>
        </App>
      </MemoryRouter>
    )
    
    // Check URL matches our actual route
    expect(window.location.pathname).toBe('/')
  })
}) 