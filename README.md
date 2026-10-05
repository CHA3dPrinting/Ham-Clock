# Ham Clock 🎙️

A Kivy-based amateur radio clock application with real-time DX cluster spots, propagation data, and HF band conditions. Designed for Raspberry Pi 4 with a round touch display, but runs on any Linux system with Kivy.

## Features

✨ **Multi-Screen Application** (swipe left/right to navigate)
- **Clock Screen**: Dual digital clock (LOCAL CST + UTC) with customizable callsign display
- **Propagation Screen**: Real-time K-index, A-index, Solar Flux, and Sunspot data from NOAA
- **Band Conditions Screen**: HF band propagation forecasts (160m–10m) based on K-index
- **DX Cluster Screen**: Live DX spots from NC7J cluster (dxc.nc7j.com:7373)
- **Settings Screen**: Callsign editor and background theme selector

## Hardware Support

- **Raspberry Pi 4** (tested and recommended)
- **KLAYERS 4" Round DSI Capacitive Touch Display** (720×720, 10-point touch)
- Pi OS Lite (headless)
- Runs on any Linux desktop with Kivy installed

## Project Structure

```
ham_clock/
├── ham_clock_main.py          # Main application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICKSTART.md              # Quick setup guide
├── LICENSE                    # MIT License
├── backgrounds/               # Background image directory
│   └── callsign_only.png     # Auto-generated callsign background
└── ham_clock_prefs.json       # User preferences (created at runtime)
```

## Installation

### Prerequisites
- Python 3.10+
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/CHA3dPrinting/Ham-Clock.git
cd Ham-Clock
```

2. **Create virtual environment**
```bash
python3 -m venv ham_clock_env
source ham_clock_env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python3 ham_clock_main.py
```

## Running on Raspberry Pi

### First-time Pi Setup

1. **Install Pi OS Lite** on microSD card
2. **Update system**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Install Python and dependencies**
```bash
sudo apt install python3-pip python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev -y
```

4. **Clone and setup**
```bash
cd ~
git clone https://github.com/CHA3dPrinting/Ham-Clock.git
cd Ham-Clock
python3 -m venv ham_clock_env
source ham_clock_env/bin/activate
pip install -r requirements.txt
```

5. **Run on startup** (optional)
Edit `/etc/rc.local` or create a systemd service to auto-launch on boot.

## Configuration

### User Preferences

The app stores user settings in `ham_clock_prefs.json`:

```json
{
  "callsign": "YOUR_CALLSIGN",
  "background": "callsign_only"
}
```

- **callsign**: Your amateur radio callsign (auto-uppercase)
- **background**: One of: `callsign_only`, `yaesu`, `icom`, `kenwood`

### Background Themes

- **Callsign Only**: White background with your callsign in big red letters (with 0 displayed as Ø per ham radio convention)
- **Yaesu**: Orange and white vintage radio aesthetic
- **Icom**: Pink modern aesthetic
- **Kenwood**: Black and white minimal aesthetic

All background images are included in the repository in the `backgrounds/` directory. To customize, replace:
- `backgrounds/yaesu.png`
- `backgrounds/icom.png`
- `backgrounds/kenwood.png`

with your own 720×720 PNG images.

## Data Sources

- **K-Index & A-Index**: NOAA Space Weather Prediction Center (SWPC)
  - API: `https://services.swpc.noaa.gov/json/planetary_k_index_1m.json`
  - Updates: Real-time, refreshed when screen is entered

- **DX Cluster Spots**: NC7J DX Cluster
  - Server: `dxc.nc7j.com:7373` (Telnet)
  - Authentication: Uses your saved callsign
  - Spots: Last 10 recent DX spots

- **Solar Flux & Sunspots**: Placeholder data (currently ~150 and ~50)

## Usage

### On Desktop/Laptop
```bash
source ham_clock_env/bin/activate
python3 ham_clock_main.py
```

### On Raspberry Pi
```bash
cd ~/ham_clock
source ham_clock_env/bin/activate
python3 ham_clock_main.py
```

### Navigation
- **Swipe Left**: Next screen
- **Swipe Right**: Previous screen
- **Settings**: Edit callsign, select background theme

## Troubleshooting

### Text is hard to read on colored backgrounds
- The app automatically adds a semi-transparent white overlay (85% opacity) over all backgrounds for readability

### DX Cluster shows "No recent DX spots available"
- Check internet connectivity
- Verify the NC7J cluster is online: `telnet dxc.nc7j.com 7373`
- Check that your callsign is set in Settings

### Callsign background not generating
- Ensure Pillow is installed: `pip install Pillow`
- The `backgrounds/` directory must be writable
- Save your callsign in Settings to regenerate the image

### Propagation data not updating
- Check NOAA API availability
- Ensure internet connectivity
- Data refreshes when you enter the Propagation screen

## Development

### Running with logging
```bash
python3 -u ham_clock_main.py 2>&1 | tee ham_clock.log
```

### Code structure
- `MainScreen`: Dual clock + callsign display
- `PropagationScreen`: NOAA geomagnetic/solar data
- `BandScreen`: HF band conditions based on K-index
- `DXClusterScreen`: Live telnet to NC7J cluster
- `SettingsScreen`: User preferences
- `HamClockScreenManager`: Screen navigation with swipe detection

### Adding new data sources
1. Create new Screen subclass
2. Implement `_fetch_data()` for API calls (in thread)
3. Update `HamClockScreenManager.screens_list` to include new screen
4. Add to `QUICKSTART.md` documentation

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Credits

Built with:
- **Kivy**: Python UI framework
- **Requests**: HTTP library
- **Pillow**: Image processing
- **NOAA**: Space weather data
- **NC7J**: DX Cluster

## Contact & Support

For issues, questions, or feature requests, please open a GitHub issue.

---

**Last Updated**: October 5, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
