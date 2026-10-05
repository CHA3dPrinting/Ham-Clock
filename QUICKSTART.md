# Ham Clock - Quick Start Guide

Get Ham Clock running in 5 minutes.

## On Your Laptop/Desktop

### 1. Clone and Setup
```bash
git clone https://github.com/CHA3dPrinting/Ham-Clock.git
cd Ham-Clock
python3 -m venv ham_clock_env
source ham_clock_env/bin/activate
pip install -r requirements.txt
```

### 2. Run
```bash
python3 ham_clock_main.py
```

### 3. Configure
1. Swipe to **Settings** (rightmost screen)
2. Enter your **callsign** → tap **Save**
3. Select a **background** theme
4. Swipe through screens to see data

**Done!** ✅

---

## On Raspberry Pi

### 1. Install OS
- Burn Pi OS Lite to microSD card
- SSH into Pi or connect HDMI + keyboard

### 2. Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev -y
```

### 3. Clone Ham Clock
```bash
cd ~
git clone https://github.com/CHA3dPrinting/Ham-Clock.git
cd Ham-Clock
python3 -m venv ham_clock_env
source ham_clock_env/bin/activate
pip install -r requirements.txt
```

### 4. First Run
```bash
python3 ham_clock_main.py
```

### 5. Auto-Launch on Boot (Optional)

**Option A: systemd service**
```bash
sudo nano /etc/systemd/system/ham-clock.service
```

Paste:
```ini
[Unit]
Description=Ham Clock
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ham_clock
Environment="DISPLAY=:0"
ExecStart=/home/pi/ham_clock/ham_clock_env/bin/python3 /home/pi/ham_clock/ham_clock_main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ham-clock
sudo systemctl start ham-clock
```

Check status:
```bash
sudo systemctl status ham-clock
```

**Option B: rc.local**
```bash
sudo nano /etc/rc.local
```

Add before `exit 0`:
```bash
cd /home/pi/ham_clock && source ham_clock_env/bin/activate && python3 ham_clock_main.py &
```

---

## First Time Setup Checklist

- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install requirements
- [ ] Run application
- [ ] Set callsign in Settings
- [ ] Select background theme
- [ ] Verify clock displays (should show LOCAL CST + UTC)
- [ ] Check Propagation data loads
- [ ] Check Band Conditions update
- [ ] Verify DX Cluster connects and shows spots
- [ ] (Pi only) Configure auto-launch

---

## Troubleshooting

### "No module named kivy"
```bash
source ham_clock_env/bin/activate
pip install -r requirements.txt
```

### "Cannot connect to display"
On Pi, install Xvfb if running headless:
```bash
sudo apt install xvfb -y
DISPLAY=:99 Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
python3 ham_clock_main.py
```

### DX Cluster shows no spots
- Wait 10-15 seconds for connection
- Check internet: `ping 8.8.8.8`
- Verify cluster is online: `telnet dxc.nc7j.com 7373`

### Text is hard to read
- Background overlay is intentionally semi-transparent (85% opacity) so backgrounds show through
- All text should be readable on any background
- If not, please open a GitHub issue with a screenshot

---

## Next Steps

- Read **README.md** for full documentation
- Customize background images in `backgrounds/` directory
- Run in verbose mode for debugging:
  ```bash
  python3 -u ham_clock_main.py 2>&1 | tee ham_clock.log
  ```

---

**Enjoy your Ham Clock!** 🎙️
