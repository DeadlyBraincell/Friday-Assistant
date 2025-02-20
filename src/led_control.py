import paho.mqtt.client as mqtt

MQTT_BROKER = "192.168.1.100"
LED_TOPIC = "room/leds"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

def set_led_color(r, g, b):
    """Sets LED color."""
    client.publish(LED_TOPIC, f"{r},{g},{b}")

def set_led_brightness(brightness):
    """Adjusts LED brightness (0-255)."""
    client.publish(LED_TOPIC, f"brightness:{brightness}")