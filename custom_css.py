"""
Custom CSS for Streamlit app with modern gradient styling
"""

def get_custom_css():
    return """
    <style>
        /* Main background with gradient */
        .stApp {
            background: linear-gradient(135deg, #FFE5E2, #FFF0F0);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        /* App container */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            margin: 0 !important;
        }
        
        /* Sidebar styling */
        .css-1d391kg, section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #DD4737 0%, #C13A2B 100%);
            padding: 1rem;
            color: white;
        }
        
        /* Sidebar text styling */
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] .stMarkdown {
            color: white !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #DD4737 0%, #C13A2B 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            width: auto;
            min-width: 200px;
            max-width: 300px;
            margin: 0 auto;
            display: block;
        }
        
        .stButton > button:hover {
            background: linear-gradient(90deg, #C13A2B 0%, #A93226 100%);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }
        
        /* Input fields */
        .stTextArea > div > div > textarea, .stTextInput > div > div > input {
            border-radius: 5px;
            border: 1px solid #ddd;
            padding: 0.5rem;
            background-color: rgba(255, 255, 255, 0.9);
        }
        
        /* Dashboard specification text area */
        .element-container:has(h2:contains("Dashboard Specification")) + .element-container .stTextArea > div > div > textarea {
            max-width: 50% !important;
            margin-left: 4rem !important;
            margin-right: 4rem !important;
            padding: 1rem !important;
        }
        
        /* File uploader styling */
        .element-container:has(h3:contains("Upload Your Data")) + .element-container .stFileUploader {
            padding-left: 2rem !important;
        }
        
        .element-container:has(h3:contains("Upload Your Data")) + .element-container .stFileUploader > div {
            max-width: 80% !important;
        }
        
        /* Select Data Source section */
        .element-container:has(h3:contains("Select Data Source")) {
            padding-left: 5rem !important;
            margin-top: 3rem !important;
        }
        
        /* Radio buttons in Select Data Source */
        .element-container:has(h3:contains("Select Data Source")) + .element-container .stRadio > div {
            padding-left: 5rem !important;
        }
        
        /* Add gap between About section and Select Data Source */
        section[data-testid="stSidebar"] .element-container:has(h3:contains("About")) {
            margin-bottom: 3rem !important;
        }
        
        /* Data frame styling */
        .data-card {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        /* Alert styling */
        .stAlert {
            border-radius: 5px;
            padding: 1rem;
        }
        
        /* Header styling */
        h1, h2, h3 {
            color: #2c3e50;
            font-weight: 600;
        }
        
        /* Markdown text */
        .stMarkdown {
            color: #333;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            white-space: pre-wrap;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 5px 5px 0 0;
            gap: 1rem;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.9);
            border-bottom: 3px solid #DD4737;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 1rem;
            color: #666;
            font-size: 0.8rem;
            margin-top: 2rem;
        }
        
        /* Remove all padding and margins from main content */
        .main .block-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        
        /* Make columns take full width */
        .row-widget.stHorizontal {
            flex-direction: row;
            width: 100% !important;
        }
        
        /* Remove padding from columns */
        .row-widget.stHorizontal > div {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Make sidebar take full height */
        section[data-testid="stSidebar"] {
            height: 100vh !important;
        }
        
        /* Remove padding from sidebar */
        section[data-testid="stSidebar"] > div {
            padding: 0 !important;
        }
        
        /* Make main content take full width */
        .main {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Remove padding from elements */
        .element-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Make charts take full width */
        .stPlotlyChart {
            width: 100% !important;
        }
        
        /* Remove padding from markdown */
        .stMarkdown {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Make buttons take full width */
        .stButton {
            width: 100% !important;
        }
        
        /* Add left padding to content sections */
        .element-container:has(h2) {
            padding-left: 2rem !important;
        }
        
        /* Add left padding to data section */
        .element-container:has(h2:contains("Data")) {
            padding-left: 2rem !important;
        }
        
        /* Add left padding to specification section */
        .element-container:has(h2:contains("Dashboard Specification")) {
            padding-left: 2rem !important;
        }
        
        /* Add left padding to chart section */
        .element-container:has(h2:contains("Quick Chart Generation")) {
            padding-left: 2rem !important;
        }
        
        /* Add left padding to columns */
        .row-widget.stHorizontal > div:first-child {
            padding-left: 2rem !important;
        }
    </style>
    """ 