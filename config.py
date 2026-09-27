"""
config.py - ShadowCost v2.5 Developer-Grade Design System, Tokens, SVG Icons & Global CSS Theme
Enterprise Geospatial Platform Theme (Linear / Vercel Dark Mode Inspired)
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
</style>
"""

# Design System Color Tokens (Linear / Vercel Dark Mode Inspired)
DARK_BG = "#0B0F17"
PANEL_BG = "rgba(18, 24, 38, 0.9)"
PANEL_BORDER = "#1E293B"
ACCENT_EMERALD = "#10B981"
ACCENT_ROSE = "#FF4757"
ACCENT_CYAN = "#00D2FF"
ACCENT_AMBER = "#FFA500"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#E5E7EB"
TEXT_MUTED = "#9CA3AF"

# Spatial Category Map Colors
CATEGORY_COLORS = {
    "park": ("#10B981", "rgba(16, 185, 129, 0.25)"),        # Environmental / Canopy
    "commercial": ("#FFA500", "rgba(255, 165, 0, 0.25)"),  # Commercial / Activity
    "residential": ("#00D2FF", "rgba(0, 210, 255, 0.25)"), # Residential / Mobility
    "other": ("#9CA3AF", "rgba(156, 163, 175, 0.20)"),       # Infrastructure
}

# SVG Line Icons (Clean Developer Tool Marks)
SVG_ICONS = {
    "logo": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>""",
    "pulse": """<svg width="10" height="10" viewBox="0 0 12 12"><circle cx="6" cy="6" r="4" fill="#10B981"><animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle></svg>""",
    "mobility": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00D2FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>""",
    "environment": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>""",
    "social": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FF4757" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""",
    "infrastructure": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFA500" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="8" rx="1"/><path d="M17 14v7"/><path d="M7 14v7"/><path d="M17 3v3"/><path d="M7 3v3"/></svg>""",
    "radar": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 12 19 5"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>""",
    "layers": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00D2FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>""",
    "brief": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>""",
    "sparkles": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>""",
    "compass": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00D2FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>""",
}

# DEVELOPER-GRADE STYLESHEET WITH MAP IFRAME & LEAFLET DARK CONTAINER RULES
CSS_THEME = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --dark-bg: #0B0F17;
    --panel-bg: rgba(18, 24, 38, 0.9);
    --panel-solid: #121826;
    --panel-border: #1E293B;
    --accent-emerald: #10B981;
    --accent-rose: #FF4757;
    --accent-cyan: #00D2FF;
    --accent-amber: #FFA500;
    --text-primary: #FFFFFF;
    --text-secondary: #E5E7EB;
    --text-muted: #9CA3AF;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: var(--dark-bg) !important;
    background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px) !important;
    background-size: 24px 24px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

header[data-testid="stHeader"], footer, #MainMenu { display:none !important; }

.block-container {
    max-width: 1440px !important;
    padding: 0.5rem 1.5rem 2.5rem !important;
}

/* Glassmorphic Panel Base */
.glass-panel {
    background: var(--panel-bg) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid var(--panel-border) !important;
    border-radius: 8px !important;
    padding: 1.25rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45) !important;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.glass-panel:hover {
    border-color: rgba(16, 185, 129, 0.3) !important;
}

/* Header Navbar */
.nav-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--panel-solid);
    border: 1px solid var(--panel-border);
    border-radius: 8px;
    padding: 0.75rem 1.25rem;
    margin-bottom: 1.25rem;
}

/* Animated LED Pulsing Ring Badge */
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.pulse-ring {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent-emerald);
    animation: pulse 2s infinite;
}

.nav-status {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--accent-emerald);
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
    letter-spacing: 0.05em;
}

/* Keyboard Shortcut Hint Pill */
.kbd-hint {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 4px;
    padding: 0.1rem 0.35rem;
    color: var(--text-muted);
    margin-left: 0.35rem;
}

/* Step Progress Drawer */
.step-drawer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--panel-solid);
    border: 1px solid var(--panel-border);
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    margin-bottom: 1.25rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.step-item { color: var(--text-muted); display: flex; align-items: center; gap: 0.5rem; }
.step-item.active { color: var(--accent-emerald); }
.step-divider { flex-grow: 1; height: 1px; background: var(--panel-border); margin: 0 1rem; }

/* Numeric KPI Values in JetBrains Mono */
.metric-mono {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.03em !important;
}

/* Native Streamlit Metric Overrides */
[data-testid="stMetric"] {
    background: var(--panel-bg) !important;
    border: 1px solid var(--panel-border) !important;
    border-radius: 8px !important;
    padding: 1rem 1.15rem !important;
    backdrop-filter: blur(12px) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* Sidebar Dark Styling */
section[data-testid="stSidebar"] {
    background: #0B0F17 !important;
    border-right: 1px solid var(--panel-border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-secondary) !important; }

/* Buttons & Inputs */
.stButton > button {
    border-radius: 6px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 0.35rem 0.45rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    border: 1px solid var(--panel-border) !important;
    background: var(--panel-solid) !important;
    color: #FFFFFF !important;
    transition: all 0.2s ease !important;
    min-height: 2.3rem !important;
}
.stButton > button p, .stButton > button span {
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
}
.stButton > button:hover {
    border-color: var(--accent-emerald) !important;
    color: var(--accent-emerald) !important;
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.25) !important;
}
.stButton > button[kind="primary"] {
    background: var(--accent-emerald) !important;
    color: #0B0F17 !important;
    font-weight: 700 !important;
    border: 1px solid var(--accent-emerald) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #059669 !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.4) !important;
}

/* Download Buttons */
.stDownloadButton > button {
    border-radius: 6px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, var(--accent-emerald), #059669) !important;
    color: #0B0F17 !important;
    border: none !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.4) !important;
    color: #FFFFFF !important;
}

/* EXPLICIT MAP IFRAME & LEAFLET DARK CONTAINER STYLING */
iframe[data-testid="stIframe"], iframe[title*="streamlit_folium"], div[data-testid="stIFrame"] iframe {
    width: 100% !important;
    height: 550px !important;
    min-height: 550px !important;
    border-radius: 8px !important;
    border: 1px solid #1E293B !important;
    background-color: #0d1117 !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
}
.leaflet-container {
    background-color: #0d1117 !important;
}

/* Map HUD Bar Overlay */
.map-hud-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(18, 24, 38, 0.95);
    border: 1px solid var(--panel-border);
    border-top: none;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
    padding: 0.4rem 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
}

/* Selectbox & Inputs */
div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {
    background-color: var(--panel-solid) !important;
    border-color: var(--panel-border) !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}

/* Native Tabs Styling */
button[data-baseweb="tab"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    border-radius: 6px !important;
}
button[aria-selected="true"] {
    color: var(--accent-emerald) !important;
    background: rgba(16, 185, 129, 0.1) !important;
    border-bottom: 2px solid var(--accent-emerald) !important;
}

/* Badge System */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.badge-emerald { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.35); }
.badge-cyan { background: rgba(0, 210, 255, 0.15); color: #00D2FF; border: 1px solid rgba(0, 210, 255, 0.35); }
.badge-amber { background: rgba(255, 165, 0, 0.15); color: #FFA500; border: 1px solid rgba(255, 165, 0, 0.35); }
.badge-rose { background: rgba(255, 71, 87, 0.15); color: #FF4757; border: 1px solid rgba(255, 71, 87, 0.35); }

/* Dense Evidence Table with Sticky Headers & Status Badges */
.dark-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    color: var(--text-secondary);
}
.dark-table th {
    position: sticky;
    top: 0;
    background: #121826;
    font-family: 'Space Grotesk', sans-serif;
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    padding: 0.6rem 0.8rem;
    text-align: left;
    border-bottom: 1px solid var(--panel-border);
}
.dark-table tr:hover { background: rgba(255, 255, 255, 0.03); }
.dark-table td {
    padding: 0.65rem 0.8rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.mono { font-family: 'JetBrains Mono', monospace !important; }
</style>
"""
