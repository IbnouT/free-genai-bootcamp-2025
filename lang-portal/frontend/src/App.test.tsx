import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from './App'

describe('App', () => {
  it('renders with Material UI theme', () => {
    render(<App />)
    
    // Test that our heading is rendered with Material UI Typography
    const heading = screen.getByRole('heading', { 
      name: /language learning portal/i,
      level: 1
    })
    expect(heading).toBeInTheDocument()
    
    // Test that Container is rendered (check for main landmark)
    const container = screen.getByRole('main')
    expect(container).toBeInTheDocument()
  })
}) 