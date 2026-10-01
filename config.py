"""
config.py - ShadowCost v2.5 Developer-Grade Design System, Tokens, SVG Icons & Global CSS Theme
Enterprise Geospatial Platform Theme (Emergency Deep Dark Recovery + 3D WebGL Canvas)
"""

# Core Mission Statement
MISSION_STATEMENT = (
    "ShadowCost helps planners understand the hidden social, environmental, "
    "mobility, and infrastructure impact of decisions before implementation."
)

# Known Presets matching Mockup & Spatial Engine
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

# Standard Keyless OSM Map Layer Configuration
OSM_TILES = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
OSM_ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
DARK_TILE_CSS = """
<style>
    .leaflet-tile-pane {
        filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3);
    }
    path.leaflet-interactive {
        stroke-dasharray: 6, 6;
    }
</style>
"""

# DARK SPATIAL INTELLIGENCE COLOUR HIERARCHY
DARK_BG = "#070A0F"
PANEL_BG = "#0D131C"
PANEL_SOLID = "#121824"
PANEL_BORDER = "rgba(139, 151, 166, 0.12)"
PRIMARY_TEAL = "#38A169"
DARK_TEAL = "#2F855A"
LIGHT_TEAL = "#48BB78"
PALE_TEAL = "#C6F6D5"
ACCENT_EMERALD = "#38A169"
ACCENT_CYAN = "#319795"
TEXT_PRIMARY = "#E8EEF5"
TEXT_SECONDARY = "#8B97A6"
TEXT_MUTED = "#4A5568"
TEXT_TECH = "#7C8794"

# Spatial Category Map Colors (Solid/Pastel Dark Theme)
CATEGORY_COLORS = {
    "park": ("#48BB78", "rgba(72, 187, 120, 0.25)"),        # Eco Canopies / Green
    "commercial": ("#DD6B20", "rgba(221, 107, 32, 0.22)"),   # Commercial / Amber
    "residential": ("#319795", "rgba(49, 151, 149, 0.22)"),  # Residential / Teal
    "industrial": ("#805AD5", "rgba(128, 90, 213, 0.22)"),   # Industrial / Purple
    "other": ("#718096", "rgba(113, 128, 150, 0.20)"),        # Infrastructure / Gray
    "intervention": ("#E53E3E", "rgba(229, 62, 62, 0.45)"),  # App-made intervention (Contrasting Coral/Crimson)
}

# SVG Line Icons
SVG_ICONS = {
    "logo": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#38A169" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>""",
    "pulse": """<svg width="10" height="10" viewBox="0 0 12 12"><circle cx="6" cy="6" r="4" fill="#48BB78"></circle></svg>""",
    "mobility": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#319795" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>""",
    "environment": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38A169" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>""",
    "social": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8B97A6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""",
    "infrastructure": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#DD6B20" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="8" rx="1"/><path d="M17 14v7"/><path d="M7 14v7"/><path d="M17 3v3"/><path d="M7 3v3"/></svg>""",
    "radar": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38A169" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 12 19 5"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>""",
    "layers": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8B97A6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>""",
    "brief": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E8EEF5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>""",
    "sparkles": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#48BB78" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>""",
    "compass": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38A169" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>""",
}

# STRICT DEEP DARK MINIMAL SPATIAL INTELLIGENCE STYLESHEET
CSS_THEME = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --dark-bg: #070A0F;
    --panel-bg: #0D131C;
    --panel-solid: #121824;
    --panel-border: rgba(139, 151, 166, 0.12);
    --primary-teal: #38A169;
    --bright-teal: #48BB78;
    --pale-teal: #C6F6D5;
    --text-primary: #E8EEF5;
    --text-secondary: #8B97A6;
    --text-muted: #4A5568;
}

body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"], [data-testid="stMainBlockContainer"], .main, section.main {
    background-color: #070A0F !important;
    color: #E8EEF5 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

.main .block-container, .block-container {
    background-color: #070A0F !important;
    max-width: 1560px !important;
    padding-top: 0.5rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer, #MainMenu { 
    display: none !important; 
    background-color: #070A0F !important;
}

/* Integrated Spatial Layout Containers */
div[data-testid="stVerticalBlock"] > div > div {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.glass-panel, .stCard, div[data-testid="stMetric"], .card-container {
    background-color: #0D131C !important;
    border: 1px solid rgba(139, 151, 166, 0.12) !important;
    border-radius: 6px !important;
    color: #E8EEF5 !important;
    box-shadow: none !important;
}

.glass-panel:hover, .stCard:hover {
    border-color: rgba(56, 161, 105, 0.3) !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #E8EEF5 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
}

p, label, div {
    color: #8B97A6;
    font-family: 'Inter', sans-serif;
}

.stMarkdown, .stText {
    color: #8B97A6 !important;
    font-family: 'Inter', sans-serif !important;
}

.accent-text, strong {
    color: #38A169 !important;
}

input, textarea, div[data-baseweb="select"] {
    background-color: #0D131C !important;
    color: #E8EEF5 !important;
    border: 1px solid rgba(139, 151, 166, 0.18) !important;
    border-radius: 5px !important;
    font-family: 'Inter', sans-serif !important;
}

div[data-baseweb="select"] > div {
    background-color: #0D131C !important;
    border-color: rgba(139, 151, 166, 0.18) !important;
    color: #E8EEF5 !important;
    font-family: 'Inter', sans-serif !important;
}

.pulse-ring {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #38A169;
}

section[data-testid="stSidebar"] {
    background: #070A0F !important;
    border-right: 1px solid rgba(139, 151, 166, 0.12) !important;
}
section[data-testid="stSidebar"] * { color: #8B97A6 !important; font-family: 'Inter', sans-serif !important; }

/* Refined Spatial Control Buttons & Navigation Tabs */
.stButton > button {
    border-radius: 5px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 0.35rem 0.65rem !important;
    border: 1px solid rgba(139, 151, 166, 0.22) !important;
    background: #0D131C !important;
    color: #C5D1E0 !important;
    transition: all 0.2s ease !important;
    min-height: 2.2rem !important;
    white-space: nowrap !important;
}

.stButton > button * {
    color: inherit !important;
}

.stButton > button:hover {
    border-color: rgba(56, 161, 105, 0.5) !important;
    color: #FFFFFF !important;
    background: #161F2E !important;
}

.stButton > button[kind="primary"],
.stButton > button[kind="primary"] *,
.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span,
.stButton > button[kind="primary"] div {
    background: #38A169 !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    border: 1px solid #38A169 !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[kind="primary"]:hover *,
.stButton > button[kind="primary"]:hover p,
.stButton > button[kind="primary"]:hover span,
.stButton > button[kind="primary"]:hover div {
    background: #2F855A !important;
    color: #FFFFFF !important;
    border-color: #2F855A !important;
}

/* Full Width Navbar Tab Buttons (No Text Clipping + High Contrast White Text for Active Tab) */
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"] {
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    padding: 0.35rem 0.6rem !important;
    font-size: 13px !important;
    min-height: 2.2rem !important;
    width: 100% !important;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"][kind="secondary"],
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"][kind="secondary"] *,
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"][kind="secondary"] p {
    background: #0D131C !important;
    border: 1px solid rgba(139, 151, 166, 0.22) !important;
    border-radius: 5px !important;
    color: #C5D1E0 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"][kind="secondary"]:hover,
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"][kind="secondary"]:hover * {
    color: #FFFFFF !important;
    background: #161F2E !important;
    border-color: rgba(56, 161, 105, 0.5) !important;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"][kind="primary"],
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"][kind="primary"] *,
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] button[key^="global_tab_"][kind="primary"] p {
    background: #38A169 !important;
    border: 1px solid #38A169 !important;
    border-radius: 5px !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
}

iframe[data-testid="stIframe"], iframe[title*="streamlit_folium"], div[data-testid="stIFrame"] iframe {
    width: 100% !important;
    border-radius: 6px !important;
    border: 1px solid rgba(139, 151, 166, 0.12) !important;
    background-color: #070A0F !important;
}

.leaflet-container {
    background-color: #070A0F !important;
}

/* Rich Solid & Pastel Accent Badges */
.badge {
    background: rgba(56, 161, 105, 0.15) !important;
    color: #48BB78 !important;
    border: 1px solid rgba(56, 161, 105, 0.3) !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    padding: 0.15rem 0.5rem !important;
}

.badge-emerald {
    background: rgba(56, 161, 105, 0.15) !important;
    color: #48BB78 !important;
    border: 1px solid rgba(56, 161, 105, 0.3) !important;
}

.badge-cyan {
    background: rgba(49, 151, 149, 0.15) !important;
    color: #319795 !important;
    border: 1px solid rgba(49, 151, 149, 0.3) !important;
}

.badge-amber {
    background: rgba(214, 158, 46, 0.15) !important;
    color: #D69E2E !important;
    border: 1px solid rgba(214, 158, 46, 0.3) !important;
}

.badge-rose {
    background: rgba(229, 62, 62, 0.15) !important;
    color: #E53E3E !important;
    border: 1px solid rgba(229, 62, 62, 0.3) !important;
}

.badge-indigo {
    background: rgba(90, 103, 216, 0.15) !important;
    color: #5A67D8 !important;
    border: 1px solid rgba(90, 103, 216, 0.3) !important;
}

.badge-purple {
    background: rgba(128, 90, 213, 0.15) !important;
    color: #805AD5 !important;
    border: 1px solid rgba(128, 90, 213, 0.3) !important;
}

.badge-live {
    background: rgba(56, 161, 105, 0.2) !important;
    color: #38A169 !important;
    border: 1px solid #38A169 !important;
}

div[data-testid="stExpander"] {
    background-color: #0D131C !important;
    border: 1px solid rgba(139, 151, 166, 0.15) !important;
    border-radius: 6px !important;
}

div[data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p {
    color: #E8EEF5 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
</style>
"""


