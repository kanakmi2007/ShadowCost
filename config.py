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
        filter: drop-shadow(0 0 6px #00F5A0);
    }
</style>
"""

# DARK SPATIAL INTELLIGENCE COLOUR HIERARCHY
DARK_BG = "#0B0F17"
PANEL_BG = "#121826"
PANEL_SOLID = "#151A21"
PANEL_BORDER = "#2A313A"
PRIMARY_TEAL = "#0F766E"
DARK_TEAL = "#0F766E"
LIGHT_TEAL = "#5EEAD4"
PALE_TEAL = "#CCFBF1"
ACCENT_EMERALD = "#14B8A6"
ACCENT_CYAN = "#00D2FF"
TEXT_PRIMARY = "#E6EDF3"
TEXT_SECONDARY = "#9AA4B2"
TEXT_MUTED = "#6B7280"
TEXT_TECH = "#7C8794"

# Spatial Category Map Colors
CATEGORY_COLORS = {
    "park": ("#00F5A0", "rgba(0, 245, 160, 0.20)"),       # Environmental / Canopy
    "commercial": ("#0F766E", "rgba(15, 118, 110, 0.20)"),  # Commercial / Activity
    "residential": ("#00D2FF", "rgba(0, 210, 255, 0.20)"), # Residential / Mobility
    "other": ("#7C8794", "rgba(124, 135, 148, 0.15)"),       # Infrastructure
}

# SVG Line Icons
SVG_ICONS = {
    "logo": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#14B8A6" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>""",
    "pulse": """<svg width="10" height="10" viewBox="0 0 12 12"><circle cx="6" cy="6" r="4" fill="#00F5A0"><animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/></circle></svg>""",
    "mobility": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00D2FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>""",
    "environment": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00F5A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>""",
    "social": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7C8794" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""",
    "infrastructure": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#14B8A6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="8" rx="1"/><path d="M17 14v7"/><path d="M7 14v7"/><path d="M17 3v3"/><path d="M7 3v3"/></svg>""",
    "radar": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#14B8A6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 12 19 5"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>""",
    "layers": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7C8794" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>""",
    "brief": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E6EDF3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>""",
    "sparkles": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00F5A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>""",
    "compass": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#14B8A6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>""",
}

# STRICT DEEP DARK MINIMAL SPATIAL INTELLIGENCE STYLESHEET (DE-BOXED)
CSS_THEME = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --dark-bg: #0B0F17;
    --panel-bg: #11161D;
    --panel-solid: #151A21;
    --panel-border: rgba(107, 114, 128, 0.15);
    --primary-teal: #0F766E;
    --bright-teal: #14B8A6;
    --pale-teal: #CCFBF1;
    --text-primary: #E6EDF3;
    --text-secondary: #9AA4B2;
    --text-muted: #6B7280;
}

body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"], [data-testid="stMainBlockContainer"], .main, section.main {
    background-color: #0B0F17 !important;
    color: #E6EDF3 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

.main .block-container, .block-container {
    background-color: #0B0F17 !important;
    max-width: 1400px !important;
    padding-top: 0.75rem !important;
    padding-bottom: 2.5rem !important;
}

header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer, #MainMenu { 
    display: none !important; 
    background-color: #0B0F17 !important;
}

/* De-boxed Containers: Remove heavy forced backgrounds & thick borders */
div[data-testid="stVerticalBlock"] > div > div {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.glass-panel, .stCard, div[data-testid="stMetric"], .card-container {
    background-color: #11161D !important;
    border: 1px solid rgba(107, 114, 128, 0.15) !important;
    border-radius: 8px !important;
    color: #E6EDF3 !important;
    box-shadow: none !important;
}

.glass-panel:hover, .stCard:hover {
    border-color: rgba(20, 184, 166, 0.35) !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #E6EDF3 !important;
    font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    font-weight: 600 !important;
}

p, span, label, div {
    color: #9AA4B2 !important;
}

.stMarkdown, .stText {
    color: #9AA4B2 !important;
}

.accent-text, strong {
    color: #14B8A6 !important;
}

input, textarea, div[data-baseweb="select"] {
    background-color: #151A21 !important;
    color: #E6EDF3 !important;
    border: 1px solid rgba(107, 114, 128, 0.20) !important;
    border-radius: 6px !important;
}

div[data-baseweb="select"] > div {
    background-color: #151A21 !important;
    border-color: rgba(107, 114, 128, 0.20) !important;
    color: #E6EDF3 !important;
}

.nav-status {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    color: #14B8A6;
    background: rgba(15, 118, 110, 0.15);
    border: 1px solid rgba(15, 118, 110, 0.3);
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
}

.pulse-ring {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #14B8A6;
}

section[data-testid="stSidebar"] {
    background: #0B0F17 !important;
    border-right: 1px solid rgba(107, 114, 128, 0.15) !important;
}
section[data-testid="stSidebar"] * { color: #9AA4B2 !important; }

/* Refined Minimal Buttons */
.stButton > button {
    border-radius: 6px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 0.35rem 0.75rem !important;
    border: 1px solid rgba(107, 114, 128, 0.20) !important;
    background: #11161D !important;
    color: #9AA4B2 !important;
    transition: all 0.2s ease !important;
    min-height: 2.2rem !important;
}

.stButton > button:hover {
    border-color: rgba(20, 184, 166, 0.4) !important;
    color: #F7F7F5 !important;
    background: #151A21 !important;
}

.stButton > button[kind="primary"] {
    background: #0F766E !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: 1px solid #0F766E !important;
}

.stButton > button[kind="primary"]:hover {
    background: #14B8A6 !important;
    color: #FFFFFF !important;
    border-color: #14B8A6 !important;
}

iframe[data-testid="stIframe"], iframe[title*="streamlit_folium"], div[data-testid="stIFrame"] iframe {
    width: 100% !important;
    height: 550px !important;
    min-height: 550px !important;
    border-radius: 8px !important;
    border: 1px solid rgba(107, 114, 128, 0.15) !important;
    background-color: #0B0F17 !important;
}

.leaflet-container {
    background-color: #0B0F17 !important;
}

.badge, .badge-emerald, .badge-cyan, .badge-rose, .badge-amber, .badge-live {
    background: rgba(15, 118, 110, 0.15) !important;
    color: #14B8A6 !important;
    border: 1px solid rgba(15, 118, 110, 0.3) !important;
    border-radius: 4px !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    padding: 0.18rem 0.55rem !important;
}
</style>
"""
