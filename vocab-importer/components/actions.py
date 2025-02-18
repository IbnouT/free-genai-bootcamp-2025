"""Actions component for the application."""
import streamlit as st

def render_actions():
    """Render the main action buttons for vocabulary management."""
    # Main actions card
    st.markdown("""
    <div class="stcard">
        <h3>🎯 Actions</h3>
        <p style="color: #a0aec0; margin-bottom: 1.5rem;">Choose an action to get started:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        generate_btn = st.button("🔨 Generate Words", use_container_width=True)
    with col_b:
        import_btn = st.button("📥 Import List", use_container_width=True)
    with col_c:
        export_btn = st.button("📤 Export List", use_container_width=True)
        
    return generate_btn, import_btn, export_btn 