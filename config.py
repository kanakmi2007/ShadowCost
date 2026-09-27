"""
config.py - ShadowCost Color System, Design Tokens, & Global Constants
"""

# Core Mission Statement
MISSION_STATEMENT = (
    "ShadowCost helps planners understand the social, environmental, "
    "and mobility consequences of infrastructure decisions before implementation."
)

# Known Presets matching Mockup 2:
KNOWN_CITIES = {
    "saket, new delhi": (28.5241, 77.2181, "Saket, South Delhi, Delhi, 110017, India"),
    "saket": (28.5241, 77.2181, "Saket, South Delhi, Delhi, 110017, India"),
    "koramangala, bengaluru": (12.9352, 77.6245, "Koramangala, Bengaluru, Karnataka, 560034, India"),
    "koramangala": (12.9352, 77.6245, "Koramangala, Bengaluru, Karnataka, 560034, India"),
    "bandra west, mumbai": (19.0600, 72.8362, "Bandra West, Mumbai, Maharashtra, 400050, India"),
    "bandra west": (19.0600, 72.8362, "Bandra West, Mumbai, Maharashtra, 400050, India"),
    "salt lake, kolkata": (22.5867, 88.4171, "Salt Lake City, Bidhannagar, Kolkata, West Bengal, 700091, India"),
    "salt lake": (22.5867, 88.4171, "Salt Lake City, Bidhannagar, Kolkata, West Bengal, 700091, India"),
    "lower manhattan, new york": (40.7128, -74.0060, "Lower Manhattan, New York, NY, 10007, USA"),
    "times square, new york": (40.7589, -73.9851, "Times Square, Manhattan, New York, NY, 10036, USA"),
    "london": (51.5074, -0.1278, "London, Greater London, England, UK"),
}

# Map Colors (Teal + Grayscale Palette)
# Primary Teal: #0F766E, Bright Teal: #14B8A6, Pale Teal: #CCFBF1
CATEGORY_COLORS = {
    "park": ("#0F766E", "#CCFBF1"),         # Environmental (Primary Teal + Pale Teal fill)
    "commercial": ("#2A2A2A", "#E5E7EB"),   # Charcoal / Light Grey
    "residential": ("#0F766E", "#99F6E4"),  # Teal accent
    "other": ("#4B5563", "#F7F7F5"),        # Dark Grey / Off-White
}

# TEAL + GREY + BLACK + WHITE Global CSS Theme
CSS_THEME = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
    --black-deep: #111111;
    --charcoal: #2A2A2A;
    --grey-dark: #4B5563;
    --grey-med: #6B7280;
    --grey-light: #E5E7EB;
    --off-white: #F7F7F5;
    --white: #FFFFFF;
    --teal-primary: #0F766E;
    --teal-bright: #14B8A6;
    --teal-pale: #CCFBF1;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: #F7F7F5 !important;
    color: #111111 !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

header[data-testid="stHeader"], footer, #MainMenu { display:none !important; }
.block-container { max-width: 1380px !important; padding: 0.75rem 2rem 3rem !important; }

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #2A2A2A;
}
section[data-testid="stSidebar"] * { color: #F7F7F5 !important; }
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
section[data-testid="stSidebar"] .stNumberInput input {
    background: #2A2A2A !important;
    border-color: #4B5563 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}

/* Native Metric Cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 1rem 1.15rem !important;
    box-shadow: 0 1px 3px rgba(17, 17, 17, 0.03) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    color: #4B5563 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    color: #111111 !important;
    letter-spacing: -0.03em !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #0F766E !important;
}

/* Native Buttons & High-Contrast Export Buttons */
.stButton > button {
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border: 1px solid #6B7280 !important;
    background: #FFFFFF !important;
    color: #111111 !important;
    transition: all 0.15s ease !important;
    min-height: 2.5rem !important;
}
.stButton > button:hover {
    border-color: #0F766E !important;
    color: #0F766E !important;
    background: #F7F7F5 !important;
}
.stButton > button[kind="primary"] {
    background: #0F766E !important;
    color: #FFFFFF !important;
    border-color: #0F766E !important;
}
.stButton > button[kind="primary"]:hover {
    background: #14B8A6 !important;
    border-color: #14B8A6 !important;
    color: #FFFFFF !important;
}

/* Download Buttons styling */
.stDownloadButton > button {
    border-radius: 9px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    border: 1px solid #0F766E !important;
    background: #0F766E !important;
    color: #FFFFFF !important;
    min-height: 2.5rem !important;
}
.stDownloadButton > button:hover {
    background: #14B8A6 !important;
    border-color: #14B8A6 !important;
    color: #FFFFFF !important;
}

/* Map iFrame */
iframe[title*="streamlit_folium"], div[data-testid="stIFrame"] iframe {
    border-radius: 12px !important;
    border: 1px solid #E5E7EB !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    color: #111111 !important;
    background: #FFFFFF !important;
    border-radius: 8px !important;
}
</style>
"""
