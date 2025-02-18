from app.dependencies import admin_only

def test_admin_only():
    """Test the admin_only dependency."""
    # Currently returns True as it's a placeholder
    assert admin_only() is True

def test_admin_only_future_implementation(monkeypatch):
    """Test the admin_only dependency with mocked environment."""
    # Test with development environment
    monkeypatch.setenv("ENVIRONMENT", "development")
    assert admin_only() is True
    
    # Note: When proper admin authentication is implemented,
    # this test should be updated to include authentication checks 