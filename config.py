"""
Ham Clock Configuration
Customize settings here without modifying the main app
"""

# TIME SETTINGS
LOCAL_TIMEZONE = 'US/Central'  # Change to your timezone
# Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

# DX CLUSTER SETTINGS
DX_CLUSTER_HOST = 'ar-cluster.net'
DX_CLUSTER_PORT = 7373
DX_CLUSTER_TIMEOUT = 10  # seconds

# Alternative clusters:
# 'dxc.oh2nkg.fi' (Europe)
# 'vk6rbp.dxcluster.com' (Australia)
# Check http://www.dxcluster.info for more

# DISPLAY SETTINGS
WINDOW_WIDTH = 800  # Adjust if using different display
WINDOW_HEIGHT = 800

# UI COLORS (RGB 0-1 scale)
COLORS = {
    'background': (0.05, 0.05, 0.1),  # Dark blue
    'text': (0.9, 0.9, 0.9),          # Light gray
    'accent': (1.0, 0.2, 0.2),        # Red (second hand)
    'border': (0.8, 0.8, 0.8),        # Light gray
}

# SWIPE SETTINGS
SWIPE_THRESHOLD = 100  # pixels to detect swipe
SWIPE_ANIMATION_DURATION = 0.3  # seconds

# NETWORK SETTINGS
REQUEST_TIMEOUT = 5  # seconds for API calls
FETCH_INTERVAL = 60  # seconds between data refreshes

# PROPAGATION DATA SOURCES
# NOAA Space Weather Prediction Center
SWPC_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

# BAND REFERENCE (can add more bands)
HF_BANDS = {
    '160m': {'freq': '1.8-2.0', 'mode': 'CW/SSB'},
    '80m': {'freq': '3.5-4.0', 'mode': 'CW/SSB'},
    '60m': {'freq': '5.3-5.4', 'mode': 'CW/SSB'},
    '40m': {'freq': '7.0-7.3', 'mode': 'CW/SSB'},
    '30m': {'freq': '10.1-10.15', 'mode': 'CW only'},
    '20m': {'freq': '14.0-14.35', 'mode': 'CW/SSB'},
    '17m': {'freq': '18.068-18.168', 'mode': 'CW/SSB'},
    '15m': {'freq': '21.0-21.45', 'mode': 'CW/SSB'},
    '12m': {'freq': '24.89-24.99', 'mode': 'CW/SSB'},
    '10m': {'freq': '28.0-29.7', 'mode': 'CW/SSB'},
}

# SCREEN ORDER (change to reorder screens or disable some)
SCREENS_ENABLED = [
    'main',          # Analog clock + time
    'propagation',   # Solar/geomagnetic
    'bands',         # HF band conditions
    'dxcluster',     # DX cluster spots
    'reference',     # Band reference
]

# LOGGING
LOG_LEVEL = 'info'  # 'debug', 'info', 'warning', 'error'
LOG_FILE = '/home/pi/ham_clock/ham_clock.log'  # Optional: None to disable file logging

# CALL SIGN (for future display personalization)
MY_CALLSIGN = 'NOCALL'  # Change this!
