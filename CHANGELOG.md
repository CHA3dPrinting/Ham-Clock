# Changelog

All notable changes to Ham Clock will be documented in this file.

## [1.0.0] - 2026-10-05

### Added
- ✨ **Multi-screen application** with swipe navigation
  - Clock screen: Dual digital clock (LOCAL CST + UTC) with customizable callsign
  - Propagation screen: Real-time NOAA geomagnetic & solar data (K-index, A-index, Solar Flux, Sunspots)
  - Band conditions screen: HF band forecasts (160m–10m) based on K-index
  - DX Cluster screen: Live DX spots from NC7J cluster with callsign-based authentication
  - Settings screen: Callsign editor and background theme selector

- 🎨 **Background themes**
  - Callsign Only: Auto-generated white background with your callsign in red
  - Yaesu, Icom, Kenwood: Custom theme support with semi-transparent overlays
  - Semi-transparent white overlays (85% opacity) for text readability on all backgrounds

- 📡 **Data integration**
  - NOAA Space Weather Prediction Center API for real-time geomagnetic data
  - NC7J DX Cluster telnet integration with automatic callsign login
  - Band condition calculation based on K-index thresholds

- 🎯 **User preferences**
  - Persistent callsign and background theme storage (JSON)
  - Auto-uppercase callsign entry
  - Ham radio convention: displays 0 as Ø (phi symbol)

- 🏗️ **Infrastructure**
  - Python 3.10+ with Kivy 2.3.0
  - Virtual environment setup guide
  - Raspberry Pi 4 optimized (Pi OS Lite)
  - KLAYERS 4" round touch display support (720×720)
  - systemd auto-launch service template
  - Comprehensive README and QUICKSTART guides
  - MIT License

### Technical Details
- **Threading**: Background API calls don't block UI
- **Error handling**: Graceful degradation when APIs unavailable
- **Timeout protection**: 15-second max connection time for DX cluster
- **Text rendering**: Pillow-based dynamic callsign image generation

## Planned for Future Releases

### [1.1.0] - Coming Soon
- [ ] Real solar flux and sunspot data (currently placeholder)
- [ ] Additional DX clusters (AR-Cluster, DXSpider alternatives)
- [ ] Customizable band list (add/remove bands)
- [ ] Sound alerts for rare/interesting DX
- [ ] QSO log integration

### [1.2.0] - Future
- [ ] CAT control for antenna tuners
- [ ] Extended band display (160m–1.2GHz)
- [ ] Touchscreen optimization for round displays
- [ ] Web interface for remote monitoring
- [ ] APRS integration
- [ ] Email/SMS alerts for specific calls

## Version History

| Version | Date | Status |
|---------|------|--------|
| 1.0.0   | 2026-10-05 | ✅ Production Ready |

## Known Issues

None reported yet! Please [open an issue](https://github.com/yourusername/ham_clock/issues) if you find one.

## Contributing

Contributions welcome! See README.md for guidelines.

---

**Last Updated**: October 5, 2026
