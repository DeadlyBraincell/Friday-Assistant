import time

def set_timer(seconds):
    """Sets a timer and notifies when it ends."""
    print(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Time's up!")