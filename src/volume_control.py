import os

def set_volume(level):
    """Adjusts system volume."""
    os.system(f"amixer set Master {level}%")
