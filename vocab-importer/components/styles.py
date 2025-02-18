"""Module containing all CSS styles for the application."""

MAIN_CSS = """
<style>
    /* Main content styling */
    .main {
        padding: 2rem;
    }
    
    /* Custom title styling */
    .title-container {
        text-align: center;
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
        color: #a0aec0;
        font-size: 1.2rem !important;
        margin-top: 0;
    }
    
    /* Card styling */
    .stcard {
        background-color: #1b1b1d;
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
        margin: 1rem 0;
    }
    
    .stat-card {
        background-color: #1b1b1d;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        flex: 1;
        min-width: 200px;
    }
</style>
""" 