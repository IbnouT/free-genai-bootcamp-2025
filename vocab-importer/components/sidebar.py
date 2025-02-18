"""Sidebar component for the application."""
import streamlit as st

def render_sidebar():
    """Render the application sidebar with language selection and quick stats."""
    with st.sidebar:
        st.markdown("# Configuration")
        
        # Language selection with flags
        st.markdown("### Select Language")
        language_options = {
            "Japanese 🇯🇵": "ja",
            "French 🇫🇷": "fr",
            "Arabic 🇸🇦": "ar",
            "Spanish 🇪🇸": "es"
        }
        selected_language = st.radio(
            "",
            options=list(language_options.keys()),
            index=0,
            key="language_select",
            label_visibility="collapsed"
        )
        
        # Divider
        st.divider()
        
        # Quick stats in sidebar
        st.markdown("#### Quick Stats")
        st.markdown(f"**Selected Language**: {selected_language.split()[0]}")
        st.markdown("**Total Words**: 0")
        st.markdown("**Categories**: 0")
        
    return selected_language, language_options[selected_language] 