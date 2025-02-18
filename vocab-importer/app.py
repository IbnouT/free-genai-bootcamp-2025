"""Main application file for the Vocab Importer."""
import streamlit as st
from components.styles import MAIN_CSS
from components.header import render_header
from components.sidebar import render_sidebar
from components.actions import render_actions
from components.activity import render_activity
from components.stats import render_stats
from components.footer import render_footer

# Page configuration
st.set_page_config(
    page_title="Vocab Importer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply the imported CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# Render header
render_header()

# Render sidebar and get selected language
selected_language, language_code = render_sidebar()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Render action buttons
    generate_btn, import_btn, export_btn = render_actions()

with col2:
    # Recent activity card
    render_activity()

# Render statistics
render_stats()

# Render footer
render_footer()
