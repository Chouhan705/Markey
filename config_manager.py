import os
import json
import sys

# Define the local AppData directory for Markey
APPDATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Markey")
CONFIG_PATH = os.path.join(APPDATA_DIR, "config.json")

DEFAULT_CONFIG = {
    "templates": {
        "1": "### VS Code Error\n```python\n{text}\n```\nPlease analyze this error.",
        "2": "### GitHub Discussion\n> {text}\n\nPlease summarize the key points.",
        "3": "### Website UI Content\n{text}\n\nReview the copy for this layout."
    }
}

def ensure_app_dir():
    """ Ensures the Markey directory exists in AppData """
    if not os.path.exists(APPDATA_DIR):
        os.makedirs(APPDATA_DIR)

def is_first_run():
    """ Returns True if the config file does not exist yet """
    return not os.path.exists(CONFIG_PATH)

def load_config():
    """ Loads configuration or returns the default fallback """
    ensure_app_dir()
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(config_data):
    """ Saves configuration data to the JSON store safely """
    ensure_app_dir()
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config_data, f, indent=4)
        return True
    except Exception as e:
        print(f"[CONFIG ERROR] Failed to save config: {e}")
        return False