# Display Brightness Control Feature

## Overview
Added display brightness control to Ham Clock with auto-initialization, user-adjustable slider, and preference persistence.

## Implementation Details

### 1. Brightness Control Function
**File**: `ham_clock_main.py` (lines 70-105)

Function: `set_brightness(brightness_value)`
- **Input**: Integer 0-255 (maps to 0-100%)
- **Behavior**:
  - Finds backlight device in `/sys/class/backlight/`
  - Reads `max_brightness` from device
  - Scales input 0-255 to device's max range
  - Writes value to brightness file
  - Handles permission errors gracefully

**Example**:
```python
set_brightness(255)  # Set to 100%
set_brightness(128)  # Set to ~50%
set_brightness(0)    # Set to 0%
```

### 2. Preferences Structure
**Default Brightness**: 100 (out of 255 = ~39%)

Added to `load_prefs()` defaults:
```python
'brightness': 100,  # Display brightness 0-255
```

### 3. Application Initialization
**File**: `ham_clock_main.py` (HamClockApp class)

On app startup (`build()` method):
```python
brightness = prefs.get('brightness', 100)
set_brightness(brightness)
```

This auto-initializes display brightness to the saved preference (or 100 if new).

### 4. Settings Screen UI
**File**: `ham_clock_main.py` (SettingsScreen class, lines 646-669)

Added brightness section between Timezone and Background sections:

#### Components:
1. **Label**: "Display Brightness:" (0.08 size_hint_y)
2. **BoxLayout Container** (0.15 size_hint_y):
   - **Slider** (size_hint_x=0.7):
     - Range: 0-255
     - Current value: loaded from prefs
     - Event: `bind(value=self.on_brightness_change)`
   - **Percentage Label** (size_hint_x=0.3):
     - Displays: "{percentage}%" (e.g., "50%")
     - Updates in real-time with slider

#### Layout Adjustments:
- Background button grid reduced from `size_hint_y=0.44` to `0.28`
- Accommodates new 0.15 height brightness section

### 5. Brightness Slider Callback
**File**: `ham_clock_main.py` (lines 740-750)

Method: `SettingsScreen.on_brightness_change(instance, value)`

**Actions**:
1. Convert slider value to integer
2. Save to prefs: `self.prefs['brightness'] = brightness_value`
3. Persist: `save_prefs(self.prefs)`
4. Update percentage label in real-time
5. Apply brightness immediately: `set_brightness(brightness_value)`
6. Log change: `Logger.info(f'Brightness changed to: {percentage}%')`

### 6. File Modifications

#### Imports Added:
```python
from kivy.uix.slider import Slider
```

#### Functions Added:
- `set_brightness(brightness_value)` - Hardware brightness control
- `SettingsScreen.on_brightness_change()` - Slider callback

#### Preferences:
- Added 'brightness' key with default value 100

#### App Initialization:
- Added brightness initialization on app startup

## User Workflow

### First Launch:
1. App starts
2. Brightness auto-initialized to 100
3. Preference saved in ham_clock_prefs.json

### Adjusting Brightness:
1. Swipe to Settings screen
2. Slide "Display Brightness" slider (0-100%)
3. Percentage updates in real-time
4. Brightness changes immediately on device
5. Preference automatically saved

### Resuming Previous Session:
1. App loads saved brightness preference
2. Auto-initializes to previously set value
3. No manual adjustment needed

## Technical Notes

### Brightness Scaling:
- **Input range**: 0-255 (Kivy slider standard)
- **Output range**: 0-max_brightness (device-dependent)
- **Formula**: `actual = (input / 255) * max_brightness`

### Backlight Device Detection:
- Searches `/sys/class/backlight/` for first available device
- Examples: `rpi_backlight`, `pwmchip0`, platform-specific drivers
- For Waveshare DSI display on CM4: Typically uses software backlight

### Permission Handling:
- If permission denied, logs warning with solution:
  ```bash
  sudo chmod 666 /sys/class/backlight/*/brightness
  ```
- Continues app execution without crashing
- Gracefully handles missing backlight device

## Testing Checklist

- [ ] App starts and brightness set to last saved value
- [ ] Settings screen displays brightness slider
- [ ] Slider moves smoothly 0-100%
- [ ] Percentage label updates in real-time
- [ ] Display brightness changes immediately when adjusting slider
- [ ] Preference persists after app restart
- [ ] Touch responsiveness maintained while adjusting
- [ ] Handles permission errors gracefully
- [ ] Works with Waveshare DSI display on CM4

## Files Changed
1. `ham_clock_main.py` - Main implementation
2. Preferences system auto-updated on first run

## References
- Kivy Slider widget: https://kivy.org/doc/stable/api-kivy.uix.slider.html
- Linux backlight interface: `/sys/class/backlight/`
- Waveshare DSI Display: Configuration via device tree overlay
