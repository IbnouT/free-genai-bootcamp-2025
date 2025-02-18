"""Header component for the application."""
import streamlit as st

def render_header():
    """Render the application header with title and subtitle."""
    st.markdown("""
    <div class="title-container">
        <h1 class="title">📚 Vocab Importer</h1>
        <p class="subtitle">Generate and manage vocabulary lists for multiple languages</p>
    </div>
    """, unsafe_allow_html=True)