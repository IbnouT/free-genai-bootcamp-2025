"""Footer component for the application."""
import streamlit as st

def render_footer():
    """Render the application footer with features list and links."""
    # Coming soon features
    with st.expander("🚀 Coming Soon Features"):
        st.markdown("""
        - ✨ Advanced word generation with categories
        - 📊 Detailed statistics and progress tracking
        - 🔄 Batch import/export functionality
        - 🎯 Custom vocabulary lists
        - 🔍 Search and filter capabilities
        """)

    # Footer links
    st.markdown("---")
    st.markdown(
        "Made with ❤️ using Streamlit • [Documentation](https://github.com/yourusername/vocab-importer) • [Report an Issue](https://github.com/yourusername/vocab-importer/issues)",
        unsafe_allow_html=True
    ) 