"""Statistics component for the application."""
import streamlit as st

def render_stats():
    """Render the statistics section with cards showing various metrics."""
    st.markdown("#### 📊 Statistics")
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <h3 style="color: #a0aec0;">Total Words</h4>
            <h2 style="color: #a0aec0;">0</h2>
        </div>
        <div class="stat-card">
            <h3 style="color: #a0aec0;">Categories</h4>
            <h2 style="color: #a0aec0;">0</h2>
        </div>
        <div class="stat-card">
            <h3 style="color: #a0aec0;">Last Updated</h4>
            <h2 style="color: #a0aec0;">Never</h2>
        </div>
    </div>
    """, unsafe_allow_html=True) 