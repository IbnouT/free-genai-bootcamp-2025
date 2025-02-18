import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Vocab Importer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main content styling */
    .main {
        padding: 2rem;
    }
    
    /* Custom title styling */
    .title-container {
        padding: 1.5rem 0;
        text-align: center;
        background: linear-gradient(90deg, #1E3D59 0%, #2E5E88 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .title {
        color: white;
        font-size: 3rem !important;
        font-weight: 600;
        margin: 0;
        padding: 0;
    }
    
    .subtitle {
        color: #E0E0E0;
        font-size: 1.2rem !important;
        margin-top: 1rem;
    }
    
    /* Card styling */
    .stcard {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    
    /* Language selector styling */
    .language-select {
        margin-top: 1rem;
    }
    
    /* Stats container */
    .stats-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        flex: 1;
        min-width: 200px;
    }
</style>
""", unsafe_allow_html=True)

# Custom title with gradient background
st.markdown("""
<div class="title-container">
    <h1 class="title">📚 Vocab Importer</h1>
    <p class="subtitle">Generate and manage vocabulary lists for multiple languages</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Configuration")
    
    # Language selection with flags
    st.markdown("#### Select Language")
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

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Main actions card
    st.markdown("""
    <div class="stcard">
        <h3>🎯 Actions</h3>
        <p>Choose an action to get started:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.button("🔨 Generate Words", use_container_width=True)
    with col_b:
        st.button("📥 Import List", use_container_width=True)
    with col_c:
        st.button("📤 Export List", use_container_width=True)

with col2:
    # Recent activity card
    st.markdown("""
    <div class="stcard">
        <h3>📋 Recent Activity</h3>
        <p>No recent activity</p>
    </div>
    """, unsafe_allow_html=True)

# Stats section
st.markdown("### 📊 Statistics")
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <h4>Total Words</h4>
        <h2>0</h2>
    </div>
    <div class="stat-card">
        <h4>Categories</h4>
        <h2>0</h2>
    </div>
    <div class="stat-card">
        <h4>Last Updated</h4>
        <h2>Never</h2>
    </div>
</div>
""", unsafe_allow_html=True)

# Coming soon features
with st.expander("🚀 Coming Soon Features"):
    st.markdown("""
    - ✨ Advanced word generation with categories
    - 📊 Detailed statistics and progress tracking
    - 🔄 Batch import/export functionality
    - 🎯 Custom vocabulary lists
    - 🔍 Search and filter capabilities
    """)

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit • [Documentation](https://github.com/yourusername/vocab-importer) • [Report an Issue](https://github.com/yourusername/vocab-importer/issues)",
    unsafe_allow_html=True
)
