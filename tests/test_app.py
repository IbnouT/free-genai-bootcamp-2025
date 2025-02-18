import pytest
from streamlit.testing.v1 import AppTest
import os

@pytest.fixture
def app_test():
    """Fixture that provides a Streamlit app test instance."""
    app_path = os.path.join(os.path.dirname(__file__), "..", "app.py")
    return AppTest.from_file(app_path)

def test_basic_app_structure(app_test: AppTest):
    """Test that the app has the essential structural elements for user interaction."""
    app_test.run()
    
    # Verify sidebar exists and is interactive
    assert len(app_test.sidebar) > 0, "App should have a sidebar for configuration"
    
    # Verify main content area exists
    assert len(app_test.main) > 0, "App should have a main content area"

def test_language_selection_functionality(app_test: AppTest):
    """Test that users can select different languages."""
    app_test.run()
    
    # Find language selection widget in sidebar
    language_widgets = [
        element for element in app_test.sidebar
        if hasattr(element, 'type') and element.type == "radio"
    ]
    assert len(language_widgets) > 0, "Language selection should be available"
    
    # Verify we can select different languages
    language_widget = language_widgets[0]
    assert len(language_widget.options) >= 4, "Should support at least 4 languages"

def test_core_actions_availability(app_test: AppTest):
    """Test that core actions for vocabulary management are available."""
    app_test.run()
    
    # Count action buttons (without checking specific labels)
    action_buttons = [
        element for element in app_test.main
        if hasattr(element, 'type') and element.type == "button"
    ]
    
    # We should have at least the core actions (generate, import, export)
    assert len(action_buttons) >= 3, "Core vocabulary management actions should be available"
    
    # Verify buttons are interactive (have click handlers)
    for button in action_buttons:
        assert hasattr(button, 'click'), "Action buttons should be interactive"

def test_future_features_discoverability(app_test: AppTest):
    """Test that users can discover planned future features."""
    app_test.run()
    
    # Find any expandable/collapsible sections
    expandable_sections = [
        element for element in app_test.main
        if hasattr(element, 'type') and element.type in ["expander", "expandable"]
    ]
    
    # Verify at least one expandable section exists for feature discovery
    assert len(expandable_sections) > 0, "App should have discoverable future features"

def test_statistics_visibility(app_test: AppTest):
    """Test that vocabulary statistics are visible to users."""
    app_test.run()
    
    # Look for numerical values in the main content
    # This avoids checking specific stat names or layout
    numerical_elements = [
        element for element in app_test.main
        if hasattr(element, 'value') and isinstance(element.value, str) 
        and any(char.isdigit() for char in element.value)
    ]
    
    assert len(numerical_elements) > 0, "Statistics should be visible to users"

def test_help_and_documentation_access(app_test: AppTest):
    """Test that users can access help and documentation."""
    app_test.run()
    
    # Look for any links or help text without checking specific URLs
    help_elements = [
        element for element in app_test.main
        if hasattr(element, 'value') and isinstance(element.value, str)
        and ('documentation' in element.value.lower() or 'help' in element.value.lower())
    ]
    
    assert len(help_elements) > 0, "Help and documentation should be accessible" 