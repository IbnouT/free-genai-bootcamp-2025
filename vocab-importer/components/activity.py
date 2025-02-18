"""Actions component for the application."""
import streamlit as st

def render_activity():
    # Recent activity card
    st.markdown("""
    <div class="stcard">
        <h3>📋 Recent Activity</h3>
        <p style="color: #a0aec0; margin-bottom: 1.5rem;">No recent activity</p>
    </div>
    """, unsafe_allow_html=True)
    