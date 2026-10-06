"""
Ham Clock - Kivy-based Radio Clock with DX Cluster and Propagation Data
Pi 4 with OS Lite, KLAYERS 4" Round Touch Display

Multi-screen app with swipe navigation:
- Screen 1: Digital dual clock (CST + UTC) + Callsign
- Screen 2: Solar/Geomagnetic data (K-index, A-index)
- Screen 3: HF Band propagation conditions
- Screen 4: DX Cluster spots
- Screen 5: Settings (background selection)
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.graphics import Color, Rectangle

import datetime
import pytz
import requests
import threading
import socket
import time
import json
import os

# Logger configuration handled by Kivy

# Preferences file
PREFS_FILE = 'ham_clock_prefs.json'

def load_prefs():
    """Load user preferences from file, or create defaults from config"""
    if os.path.exists(PREFS_FILE):
        try:
            with open(PREFS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Create defaults (you can edit these)
    defaults = {
        'callsign': 'NOCALL',  # Change this to your callsign
        'background': 'callsign_only',
    }
    return defaults

def save_prefs(prefs):
    """Save user preferences to file"""
    try:
        with open(PREFS_FILE, 'w') as f:
            json.dump(prefs, f)
    except Exception as e:
        Logger.error(f'Failed to save prefs: {e}')


def generate_callsign_background(callsign):
    """Generate a white background with the callsign displayed"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Create backgrounds directory if it doesn't exist
        if not os.path.exists('backgrounds'):
            os.makedirs('backgrounds')
        
        # Create white image 720x720
        img = Image.new('RGB', (720, 720), color='white')
        draw = ImageDraw.Draw(img)
        
        # Display callsign with 0 as Ø (ham radio convention)
        callsign_display = callsign.replace('0', 'Ø')
        
        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        except:
            font = ImageFont.load_default()
        
        # Center the text
        bbox = draw.textbbox((0, 0), callsign_display, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (720 - text_width) // 2
        y = (720 - text_height) // 2
        
        # Draw red callsign (ham radio convention)
        draw.text((x, y), callsign_display, fill='red', font=font)
        
        # Save as callsign_only.png
        img.save('backgrounds/callsign_only.png')
        Logger.info(f'Generated callsign background: {callsign_display}')
    except Exception as e:
        Logger.warning(f'Could not generate callsign background: {e}')





class MainScreen(Screen):
    """Screen 1: Digital dual clock (CST + UTC) with selectable backgrounds"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefs = load_prefs()
        
        # Use FloatLayout for background image
        float_layout = FloatLayout()
        
        # Background image
        self.bg_image = KivyImage(
            source='backgrounds/callsign_only.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        float_layout.add_widget(self.bg_image)
        
        # Semi-transparent white overlay for readability
        overlay = FloatLayout(size_hint=(1, 1))
        with overlay.canvas.before:
            Color(1, 1, 1, 0.85)  # White with 85% opacity
            self.overlay_rect = Rectangle(size=overlay.size, pos=overlay.pos)
        overlay.bind(size=self._update_overlay_rect, pos=self._update_overlay_rect)
        
        # Content layout on top
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(1, 1))
        
        # Callsign display at top
        self.callsign_label = Label(
            text=self.prefs['callsign'],
            font_size='32sp',
            bold=True,
            size_hint_y=0.15,
            color=(0.9, 0.2, 0.2, 1)  # Red for callsign
        )
        main_layout.add_widget(self.callsign_label)
        
        # Time display - Dual digital clocks
        time_layout = GridLayout(cols=2, size_hint_y=0.85, spacing=20, padding=20)
        
        # LOCAL TIME (CST)
        local_box = BoxLayout(orientation='vertical', padding=15, size_hint_x=0.5)
        local_box.add_widget(Label(text='LOCAL (CST)', size_hint_y=0.2, bold=True, font_size='18sp', color=(0, 0, 0, 1)))
        self.local_time = Label(text='--:--:--', size_hint_y=0.8, font_size='48sp', bold=True, color=(0, 0.6, 0, 1))
        local_box.add_widget(self.local_time)
        time_layout.add_widget(local_box)
        
        # UTC TIME
        utc_box = BoxLayout(orientation='vertical', padding=15, size_hint_x=0.5)
        utc_box.add_widget(Label(text='UTC', size_hint_y=0.2, bold=True, font_size='18sp', color=(0, 0, 0, 1)))
        self.utc_time = Label(text='--:--:--', size_hint_y=0.8, font_size='48sp', bold=True, color=(0, 0.6, 0, 1))
        utc_box.add_widget(self.utc_time)
        time_layout.add_widget(utc_box)
        
        main_layout.add_widget(time_layout)
        overlay.add_widget(main_layout)
        float_layout.add_widget(overlay)
        self.add_widget(float_layout)
        
        Clock.schedule_interval(self.update_times, 0.1)  # Update 10x per second for smooth updates
        self.bind(on_enter=self.on_enter)
    
    def _update_overlay_rect(self, instance, value):
        """Update overlay rectangle when size/pos changes"""
        if hasattr(self, 'overlay_rect'):
            self.overlay_rect.pos = instance.pos
            self.overlay_rect.size = instance.size
    
    def on_enter(self, *args):
        """Reload background and callsign when entering screen"""
        self.prefs = load_prefs()
        bg_name = self.prefs.get('background', 'callsign_only')
        try:
            self.bg_image.source = f'backgrounds/{bg_name}.png'
        except:
            pass
        # Display callsign with 0 as Ø (ham radio convention)
        callsign_display = self.prefs['callsign'].replace('0', 'Ø')
        self.callsign_label.text = callsign_display
    
    def update_times(self, dt):
        local_tz = pytz.timezone('US/Central')  # Central Standard Time
        local_time = datetime.datetime.now(local_tz)
        utc_time = datetime.datetime.now(pytz.UTC)
        
        self.local_time.text = local_time.strftime('%H:%M:%S')
        self.utc_time.text = utc_time.strftime('%H:%M:%S')


class PropagationScreen(Screen):
    """Screen 2: Solar/Geomagnetic data"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefs = load_prefs()
        
        # Use FloatLayout for background image
        main_layout = FloatLayout()
        
        # Background image
        self.bg_image = KivyImage(
            source='backgrounds/callsign_only.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        main_layout.add_widget(self.bg_image)
        
        # Semi-transparent white overlay for readability
        overlay = FloatLayout(size_hint=(1, 1))
        with overlay.canvas.before:
            Color(1, 1, 1, 0.85)  # White with 85% opacity
            self.overlay_rect = Rectangle(size=overlay.size, pos=overlay.pos)
        overlay.bind(size=self._update_overlay_rect, pos=self._update_overlay_rect)
        
        # Content layout on top
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))
        
        layout.add_widget(Label(text='Solar & Geomagnetic Conditions', size_hint_y=0.1, bold=True, font_size='16sp', color=(0, 0, 0, 1)))
        
        # Data grid
        data_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.9)
        
        # K-index
        k_box = BoxLayout(orientation='vertical', size_hint_x=0.5)
        k_box.add_widget(Label(text='K-Index', size_hint_y=0.3, bold=True, color=(0, 0, 0, 1)))
        self.k_index = Label(text='--', size_hint_y=0.7, font_size='20sp', color=(0, 0, 0, 1))
        k_box.add_widget(self.k_index)
        data_layout.add_widget(k_box)
        
        # A-index
        a_box = BoxLayout(orientation='vertical', size_hint_x=0.5)
        a_box.add_widget(Label(text='A-Index', size_hint_y=0.3, bold=True, color=(0, 0, 0, 1)))
        self.a_index = Label(text='--', size_hint_y=0.7, font_size='20sp', color=(0, 0, 0, 1))
        a_box.add_widget(self.a_index)
        data_layout.add_widget(a_box)
        
        # Solar Flux
        sf_box = BoxLayout(orientation='vertical')
        sf_box.add_widget(Label(text='Solar Flux', size_hint_y=0.3, bold=True, color=(0, 0, 0, 1)))
        self.solar_flux = Label(text='--', size_hint_y=0.7, font_size='20sp', color=(0, 0, 0, 1))
        sf_box.add_widget(self.solar_flux)
        data_layout.add_widget(sf_box)
        
        # Sunspot Number
        ssn_box = BoxLayout(orientation='vertical')
        ssn_box.add_widget(Label(text='Sunspots', size_hint_y=0.3, bold=True, color=(0, 0, 0, 1)))
        self.sunspot_num = Label(text='--', size_hint_y=0.7, font_size='20sp', color=(0, 0, 0, 1))
        ssn_box.add_widget(self.sunspot_num)
        data_layout.add_widget(ssn_box)
        
        layout.add_widget(data_layout)
        overlay.add_widget(layout)
        main_layout.add_widget(overlay)
        self.add_widget(main_layout)
        
        # Fetch data on screen enter
        self.bind(on_enter=self.on_enter)
    
    def _update_overlay_rect(self, instance, value):
        """Update overlay rectangle when size/pos changes"""
        if hasattr(self, 'overlay_rect'):
            self.overlay_rect.pos = instance.pos
            self.overlay_rect.size = instance.size
    
    def on_enter(self, *args):
        """Reload background when entering screen"""
        self.prefs = load_prefs()
        bg_name = self.prefs.get('background', 'callsign_only')
        try:
            self.bg_image.source = f'backgrounds/{bg_name}.png'
        except:
            pass
        self.fetch_propagation_data()
    
    def fetch_propagation_data(self, *args):
        """Fetch from NOAA Space Weather Prediction Center"""
        thread = threading.Thread(target=self._fetch_data)
        thread.daemon = True
        thread.start()
    
    def _fetch_data(self):
        try:
            # NOAA planetary K-index data
            url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            
            if data and len(data) > 0:
                # Get the latest entry
                latest = data[-1]
                
                # Extract Kp value (0-9 integer scale)
                k_val = latest.get('kp_index')
                if k_val is not None:
                    k_val = int(k_val)
                else:
                    k_val = '--'
                
                # Use estimated_kp for A-index display
                # estimated_kp is a decimal approximation
                a_val = latest.get('estimated_kp')
                if a_val is not None:
                    a_val = float(a_val)
                else:
                    a_val = '--'
                
                Clock.schedule_once(lambda dt: self._update_labels(k_val, a_val), 0)
            else:
                Logger.warning('No data from NOAA')
        except Exception as e:
            Logger.error(f'PropagationScreen fetch error: {e}')
    
    def _update_labels(self, k, a):
        try:
            if k != '--':
                self.k_index.text = str(k)  # Kp is integer 0-9
            else:
                self.k_index.text = '--'
            
            if a != '--':
                self.a_index.text = f'{a:.1f}'  # Estimated Kp as decimal
            else:
                self.a_index.text = '--'
        except Exception as e:
            Logger.error(f'Failed to update labels: {e}')
            self.k_index.text = '--'
            self.a_index.text = '--'
        
        # Solar flux and sunspots - placeholder for now
        self.solar_flux.text = '~150'
        self.sunspot_num.text = '~50'


class BandScreen(Screen):
    """Screen 3: HF Band propagation conditions"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefs = load_prefs()
        
        # Use FloatLayout for background image
        main_layout = FloatLayout()
        
        # Background image
        self.bg_image = KivyImage(
            source='backgrounds/callsign_only.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        main_layout.add_widget(self.bg_image)
        
        # Semi-transparent white overlay for readability
        overlay = FloatLayout(size_hint=(1, 1))
        with overlay.canvas.before:
            Color(1, 1, 1, 0.85)  # White with 85% opacity
            self.overlay_rect = Rectangle(size=overlay.size, pos=overlay.pos)
        overlay.bind(size=self._update_overlay_rect, pos=self._update_overlay_rect)
        
        # Content layout on top
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))
        
        layout.add_widget(Label(text='HF Band Conditions', size_hint_y=0.1, bold=True, font_size='16sp', color=(0, 0, 0, 1)))
        
        # Scrollable band list
        scroll = ScrollView()
        bands_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        bands_layout.bind(minimum_height=bands_layout.setter('height'))
        
        self.band_labels = {}
        bands = ['160m', '80m', '40m', '20m', '17m', '15m', '12m', '10m']
        
        for band in bands:
            band_box = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
            band_box.add_widget(Label(text=band, size_hint_y=0.4, bold=True, color=(0, 0, 0, 1)))
            
            status_label = Label(text='--', size_hint_y=0.6, font_size='14sp', color=(0, 0, 0, 1))
            self.band_labels[band] = status_label
            band_box.add_widget(status_label)
            
            bands_layout.add_widget(band_box)
        
        scroll.add_widget(bands_layout)
        layout.add_widget(scroll)
        overlay.add_widget(layout)
        main_layout.add_widget(overlay)
        self.add_widget(main_layout)
        
        self.bind(on_enter=self.on_enter)
    
    def _update_overlay_rect(self, instance, value):
        """Update overlay rectangle when size/pos changes"""
        if hasattr(self, 'overlay_rect'):
            self.overlay_rect.pos = instance.pos
            self.overlay_rect.size = instance.size
    
    def on_enter(self, *args):
        """Reload background when entering screen"""
        self.prefs = load_prefs()
        bg_name = self.prefs.get('background', 'callsign_only')
        try:
            self.bg_image.source = f'backgrounds/{bg_name}.png'
        except:
            pass
        self.update_band_conditions()
    
    def update_band_conditions(self, *args):
        """Simple band conditions based on K-index"""
        thread = threading.Thread(target=self._fetch_and_update)
        thread.daemon = True
        thread.start()
    
    def _fetch_and_update(self):
        try:
            # Fetch K-index
            url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            
            if data:
                k_val = float(data[-1].get('kp_index', 4))
                
                # Simple propagation model based on K-index
                conditions = {
                    '160m': 'Fair' if k_val < 6 else 'Poor',
                    '80m': 'Good' if k_val < 5 else 'Fair',
                    '40m': 'Good' if k_val < 7 else 'Fair',
                    '20m': 'Excellent' if k_val < 6 else 'Good',
                    '17m': 'Excellent' if k_val < 5 else 'Good',
                    '15m': 'Excellent' if k_val < 4 else 'Good',
                    '12m': 'Very Good' if k_val < 5 else 'Good',
                    '10m': 'Fair' if k_val < 4 else 'Poor',
                }
                
                for band, status in conditions.items():
                    Clock.schedule_once(lambda dt, b=band, s=status: 
                                      setattr(self.band_labels[b], 'text', s), 0)
        except Exception as e:
            Logger.error(f'BandScreen: {e}')








class SettingsScreen(Screen):
    """Screen 5: Settings - Callsign and background selection"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefs = load_prefs()
        
        # Use FloatLayout for background image
        main_layout = FloatLayout()
        
        # Background image
        self.bg_image = KivyImage(
            source='backgrounds/callsign_only.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        main_layout.add_widget(self.bg_image)
        
        # Semi-transparent white overlay for readability
        overlay = FloatLayout(size_hint=(1, 1))
        with overlay.canvas.before:
            Color(1, 1, 1, 0.85)  # White with 85% opacity
            self.overlay_rect = Rectangle(size=overlay.size, pos=overlay.pos)
        overlay.bind(size=self._update_overlay_rect, pos=self._update_overlay_rect)
        
        # Content layout on top
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(1, 1))
        
        # Title
        layout.add_widget(Label(text='Settings', size_hint_y=0.08, bold=True, font_size='20sp', color=(0, 0, 0, 1)))
        
        # ===== CALLSIGN SECTION =====
        layout.add_widget(Label(text='Your Callsign:', size_hint_y=0.08, bold=True, font_size='14sp', color=(0, 0, 0, 1)))
        
        # Callsign input
        callsign_box = BoxLayout(size_hint_y=0.12, spacing=10)
        self.callsign_input = TextInput(
            text=self.prefs['callsign'],
            multiline=False,
            size_hint_x=0.7,
            font_size='16sp',
            foreground_color=(0, 0, 0, 1)  # Black text in input
        )
        callsign_box.add_widget(self.callsign_input)
        
        save_btn = Button(text='Save', size_hint_x=0.3)
        save_btn.bind(on_press=self.save_callsign)
        callsign_box.add_widget(save_btn)
        
        layout.add_widget(callsign_box)
        
        # ===== BACKGROUND SECTION =====
        layout.add_widget(Label(text='Select Background:', size_hint_y=0.08, bold=True, font_size='14sp', color=(0, 0, 0, 1)))
        
        # Button grid for backgrounds
        button_layout = GridLayout(cols=2, size_hint_y=0.56, spacing=10, padding=10)
        
        backgrounds = [
            ('Callsign Only', 'callsign_only'),
            ('Yaesu', 'yaesu'),
            ('Icom', 'icom'),
            ('Kenwood', 'kenwood'),
        ]
        
        for label, bg_name in backgrounds:
            btn = Button(text=label, size_hint_y=None, height=60)
            btn.bind(on_press=lambda instance, name=bg_name: self.select_background(name))
            button_layout.add_widget(btn)
        
        layout.add_widget(button_layout)
        overlay.add_widget(layout)
        main_layout.add_widget(overlay)
        self.add_widget(main_layout)
        
        self.bind(on_enter=self.on_enter)
    
    def _update_overlay_rect(self, instance, value):
        """Update overlay rectangle when size/pos changes"""
        if hasattr(self, 'overlay_rect'):
            self.overlay_rect.pos = instance.pos
            self.overlay_rect.size = instance.size
    
    def on_enter(self, *args):
        """Refresh when entering"""
        self.prefs = load_prefs()
        self.callsign_input.text = self.prefs['callsign']
        # Reload background
        bg_name = self.prefs.get('background', 'callsign_only')
        try:
            self.bg_image.source = f'backgrounds/{bg_name}.png'
        except:
            pass
    
    def save_callsign(self, instance):
        """Save callsign to preferences"""
        new_callsign = self.callsign_input.text.strip().upper()
        if new_callsign:
            self.prefs['callsign'] = new_callsign
            save_prefs(self.prefs)
            # Generate callsign background image
            generate_callsign_background(new_callsign)
            Logger.info(f'Callsign saved: {new_callsign}')
        else:
            self.callsign_input.text = self.prefs['callsign']  # Reset if empty
    
    def select_background(self, bg_name):
        """Save background preference and update main screen"""
        self.prefs['background'] = bg_name
        save_prefs(self.prefs)
        
        # Notify main screen to update
        Logger.info(f'Background changed to: {bg_name}')


class DXClusterScreen(Screen):
    """Screen 4: DX Cluster spots from NC7J cluster"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefs = load_prefs()  # Load callsign from prefs
        
        # Use FloatLayout for background image
        main_layout = FloatLayout()
        
        # Background image
        self.bg_image = KivyImage(
            source='backgrounds/callsign_only.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        main_layout.add_widget(self.bg_image)
        
        # Semi-transparent white overlay for readability
        overlay = FloatLayout(size_hint=(1, 1))
        with overlay.canvas.before:
            Color(1, 1, 1, 0.85)  # White with 85% opacity
            self.overlay_rect = Rectangle(size=overlay.size, pos=overlay.pos)
        overlay.bind(size=self._update_overlay_rect, pos=self._update_overlay_rect)
        
        # Content layout on top
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))
        
        # Header with title and live indicator
        header_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        header_layout.add_widget(Label(text='DX Cluster Spots (NC7J)', size_hint_x=0.8, bold=True, font_size='16sp', color=(0, 0, 0, 1)))
        self.live_indicator = Label(text='', size_hint_x=0.2, bold=True, font_size='14sp', color=(0, 1, 0, 1))
        header_layout.add_widget(self.live_indicator)
        layout.add_widget(header_layout)
        
        # Track seen spots for highlighting new ones
        self.seen_spots = set()
        
        # Scrollable spot list
        scroll = ScrollView()
        self.spots_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.spots_layout.bind(minimum_height=self.spots_layout.setter('height'))
        
        scroll.add_widget(self.spots_layout)
        layout.add_widget(scroll)
        overlay.add_widget(layout)
        main_layout.add_widget(overlay)
        self.add_widget(main_layout)
        
        self.bind(on_enter=self.on_enter)
    
    def _update_overlay_rect(self, instance, value):
        """Update overlay rectangle when size/pos changes"""
        if hasattr(self, 'overlay_rect'):
            self.overlay_rect.pos = instance.pos
            self.overlay_rect.size = instance.size
    
    def on_enter(self, *args):
        """Reload background and start live updates when entering screen"""
        self.prefs = load_prefs()
        bg_name = self.prefs.get('background', 'callsign_only')
        try:
            self.bg_image.source = f'backgrounds/{bg_name}.png'
        except:
            pass
        self.fetch_dx_spots()
        # Start auto-refresh every 10 seconds while viewing this screen
        self.refresh_event = Clock.schedule_interval(self.fetch_dx_spots, 10)
    
    def on_leave(self, *args):
        """Stop live updates when leaving screen"""
        if hasattr(self, 'refresh_event'):
            self.refresh_event.cancel()
    
    def fetch_dx_spots(self, *args):
        """Connect to DX Cluster and fetch recent spots"""
        thread = threading.Thread(target=self._fetch_cluster_data)
        thread.daemon = True
        thread.start()
    
    def _fetch_cluster_data(self):
        """Connect to NC7J DX Cluster with callsign login"""
        try:
            # NC7J Cluster: dxc.nc7j.com
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect(('dxc.nc7j.com', 7373))
            
            spots_data = []
            buffer = ''
            start_time = time.time()
            banner_done = False
            logged_in = False
            rate_limited = False
            callsign = self.prefs.get('callsign', 'NOCALL')
            
            # Read initial banner and send login
            while time.time() - start_time < 15:
                try:
                    data = sock.recv(2048).decode('utf-8', errors='ignore')
                    if data:
                        buffer += data
                        
                        # Look for login prompt
                        if not logged_in and 'login:' in buffer.lower():
                            # Send callsign
                            sock.send((callsign + '\n').encode('utf-8'))
                            logged_in = True
                            buffer = ''  # Clear buffer after login
                            time.sleep(0.5)  # Wait a moment for server response
                            # Request recent DX spots
                            sock.send(b'show/dx 10\n')
                            continue
                        
                        # Check for rate limit message
                        if logged_in and 'temporarily delayed' in buffer.lower() or 'retry in' in buffer.lower():
                            rate_limited = True
                            # Extract retry time if possible
                            import re
                            match = re.search(r'retry in (\d+) seconds', buffer.lower())
                            if match:
                                retry_seconds = int(match.group(1))
                                retry_minutes = retry_seconds // 60
                                spots_data = [f'NC7J Rate Limited - Retry in {retry_minutes}m {retry_seconds % 60}s']
                            else:
                                spots_data = ['NC7J Rate Limited - Please retry in a few minutes']
                            raise StopIteration()
                        
                        # After login, process lines for DX spots
                        if logged_in:
                            lines = buffer.split('\n')
                            
                            for line in lines[:-1]:  # Process all complete lines
                                line = line.strip()
                                
                                # Skip empty lines
                                if not line:
                                    continue
                                
                                # Skip obvious banner/server messages
                                if any(skip in line.lower() for skip in [
                                    'login:', 'hello', 'system operator', 'de ', 'connected',
                                    'cluster', 'manual', 'located', 'callsign:', 'enter',
                                    'please', 'password', '***', 'skimmer', 'ar-cluster',
                                    'utah', 'syracuse', 'http://', 'welcome', 'ar6'
                                ]):
                                    continue
                                
                                # Look for actual DX spots
                                # Real spots typically contain: callsign, frequency, and other info
                                # They usually have patterns like "de W5XYZ: 14005.0" or "DX de"
                                if len(line) > 15 and 'de ' in line.lower():
                                    # This looks like a real DX spot
                                    spots_data.append(line)
                                    if len(spots_data) >= 10:
                                        raise StopIteration()
                                elif len(line) > 20 and any(freq_pattern in line for freq_pattern in ['.0', '.5', '000', '100', '200', '300', '400', '500', '600', '700', '800', '900']):
                                    # Might be a spot with frequency info
                                    if any(c.isdigit() for c in line) and any(c.isalpha() for c in line):
                                        if not line.startswith('>'):
                                            spots_data.append(line)
                                            if len(spots_data) >= 10:
                                                raise StopIteration()
                            
                            buffer = lines[-1]  # Keep incomplete line
                except socket.timeout:
                    break
                except StopIteration:
                    break
            
            sock.close()
            
            if not spots_data and not rate_limited:
                status = 'No recent DX spots available' if logged_in else 'Failed to connect to cluster'
                spots_data = [status]
            
            # Update UI
            Clock.schedule_once(lambda dt: self._update_spots(spots_data), 0)
        except Exception as e:
            error_msg = str(e)
            Logger.error(f'DXClusterScreen: {error_msg}')
            Clock.schedule_once(lambda dt: self._update_spots([f'Error: {error_msg}']), 0)
    
    def _update_spots(self, spots):
        """Update spots display with new spots highlighted at top"""
        if not spots:
            self.spots_layout.clear_widgets()
            self.spots_layout.add_widget(Label(text='No spots available', size_hint_y=None, height=30, color=(0, 0, 0, 1)))
            self.live_indicator.text = '●'  # Pulsing indicator
        else:
            # Find which spots are new
            new_spot_strings = []
            for spot in spots[-15:]:  # Keep last 15
                if spot and spot not in self.seen_spots:
                    new_spot_strings.append(spot)
                    self.seen_spots.add(spot)
            
            # Keep seen_spots from growing too large
            if len(self.seen_spots) > 100:
                # Keep only the 100 most recent
                self.seen_spots = self.seen_spots.copy()
            
            # Clear and rebuild display - new spots at top with green highlight
            self.spots_layout.clear_widgets()
            
            # Add new spots first (with highlight)
            for spot in new_spot_strings:
                if spot:
                    spot_widget = FloatLayout(size_hint_y=None, height=22)
                    with spot_widget.canvas.before:
                        Color(0, 1, 0, 0.2)  # Green with 20% opacity for new spots
                        spot_widget.rect = Rectangle(size=spot_widget.size, pos=spot_widget.pos)
                    spot_widget.bind(size=self._update_spot_rect, pos=self._update_spot_rect)
                    
                    spot_label = Label(text=spot[:70], size_hint_y=None, height=22, 
                                     font_size='10sp', text_size=(self.width - 20, None), color=(0, 0, 0, 1))
                    spot_widget.add_widget(spot_label)
                    self.spots_layout.add_widget(spot_widget)
            
            # Add existing spots (no highlight)
            for spot in spots[-15:]:
                if spot and spot not in new_spot_strings:
                    spot_label = Label(text=spot[:70], size_hint_y=None, height=22, 
                                     font_size='10sp', text_size=(self.width - 20, None), color=(0, 0, 0, 1))
                    self.spots_layout.add_widget(spot_label)
            
            # Update live indicator
            self.live_indicator.text = '● LIVE'
    
    def _update_spot_rect(self, instance, value):
        """Update spot background rectangle"""
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size


class HamClockScreenManager(ScreenManager):
    """Screen manager with swipe navigation"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set white background for all screens
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.screens_list = [
            MainScreen(name='main'),
            PropagationScreen(name='propagation'),
            BandScreen(name='bands'),
            DXClusterScreen(name='dxcluster'),
            SettingsScreen(name='settings'),
        ]
        
        for screen in self.screens_list:
            self.add_widget(screen)
        
        self.current = 'main'
        self.touch_start_x = 0
    
    def _update_rect(self, instance, value):
        """Update background rectangle when size/pos changes"""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_touch_down(self, touch):
        self.touch_start_x = touch.x
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        # Detect swipe
        swipe_distance = touch.x - self.touch_start_x
        swipe_threshold = 100
        
        if abs(swipe_distance) > swipe_threshold:
            current_index = [s.name for s in self.screens_list].index(self.current)
            
            if swipe_distance > 0:  # Swipe right (previous)
                new_index = (current_index - 1) % len(self.screens_list)
            else:  # Swipe left (next)
                new_index = (current_index + 1) % len(self.screens_list)
            
            self.current = self.screens_list[new_index].name
        
        return super().on_touch_up(touch)


class HamClockApp(App):
    """Main Kivy application"""
    
    def build(self):
        self.title = 'Ham Clock'
        # Generate callsign background on startup
        prefs = load_prefs()
        generate_callsign_background(prefs.get('callsign', 'NOCALL'))
        return HamClockScreenManager()


if __name__ == '__main__':
    HamClockApp().run()
