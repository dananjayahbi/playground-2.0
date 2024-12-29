import os
import json
from PIL import Image

DEFAULT_DIR = "default"
DEFAULT_JSON_PATH = os.path.join(DEFAULT_DIR, "settings.json")
DEFAULT_IMAGE_PATH = os.path.join(DEFAULT_DIR, "default_background.png")

def ensure_default_directory():
    """Ensure the default directory and its contents exist."""
    if not os.path.exists(DEFAULT_DIR):
        os.makedirs(DEFAULT_DIR)
    
    # Create a white default background image if it doesn't exist
    if not os.path.exists(DEFAULT_IMAGE_PATH):
        image = Image.new("RGB", (1080, 1350), color="white")
        image.save(DEFAULT_IMAGE_PATH)
    
    # Create a default JSON settings file if it doesn't exist
    if not os.path.exists(DEFAULT_JSON_PATH):
        default_settings = {
            "background_image": DEFAULT_IMAGE_PATH,
            "fb_width": 1080,
            "fb_height": 1350,
            "quote_text": "Default Quote",
            "signature_text": "Your Name",
            "quote_color": "#000000",
            "signature_color": "#000000"
        }
        with open(DEFAULT_JSON_PATH, "w") as f:
            json.dump(default_settings, f)

def load_default_settings():
    """Load default settings from JSON."""
    if not os.path.exists(DEFAULT_JSON_PATH):
        ensure_default_directory()  # Create defaults if missing
    with open(DEFAULT_JSON_PATH, "r") as f:
        return json.load(f)

def save_default_settings(settings, background_image_path):
    """Save default settings and update background image."""
    ensure_default_directory()
    
    # Save updated background image
    if background_image_path:
        image = Image.open(background_image_path)
        image.save(DEFAULT_IMAGE_PATH)
        settings["background_image"] = DEFAULT_IMAGE_PATH
    
    # Save updated settings
    with open(DEFAULT_JSON_PATH, "w") as f:
        json.dump(settings, f)
