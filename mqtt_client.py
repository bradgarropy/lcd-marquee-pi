"""
MQTT client for LCD Marquee.

Handles connection to HiveMQ broker, TLS setup, authentication,
and message processing. Messages are placed in a thread-safe queue
for consumption by the main LCD display loop.
"""

import json
import logging
import os
import queue
import ssl

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Module logger
logger = logging.getLogger(__name__)

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_PORT = 8883
MQTT_TOPIC = "lcd-marquee/messages"

# Thread-safe queue shared with main module
message_queue = queue.Queue()


def on_connect(client, userdata, flags, reason_code, properties):
    """
    Called when connected to the broker.

    Subscribe here so we auto-resubscribe after reconnection.
    """
    if reason_code == 0:
        logger.info("Connected to MQTT broker")
        logger.info(f"Subscribing to topic: {MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Connection failed with reason code: {reason_code}")


def on_disconnect(client, userdata, flags, reason_code, properties):
    """
    Called when disconnected from the broker.

    paho-mqtt handles reconnection automatically with loop_start().
    """
    if reason_code == 0:
        logger.info("Disconnected cleanly")
    else:
        logger.warning(f"Unexpected disconnect (code {reason_code}), reconnecting...")


def on_message(client, userdata, msg):
    """
    Called when a message arrives on a subscribed topic.

    Parses JSON payload and queues it for LCD display.
    Expected format: {"message": "string", "twitter": "string"}
    """
    try:
        payload = json.loads(msg.payload.decode())
        message = payload.get("message", "")
        twitter = payload.get("twitter", "")
        logger.info(f"Received: {message} / {twitter}")
        message_queue.put((message, twitter))
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON received: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


def create_client():
    """
    Create and configure MQTT client with TLS and authentication.

    Returns a configured client ready to connect.
    """
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Authentication
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # TLS for secure connection (required for port 8883)
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)

    # Assign callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    return client


def connect(client):
    """Connect to the broker and start the background network loop."""
    logger.info(f"Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()


def disconnect(client):
    """Stop the network loop and disconnect cleanly."""
    logger.info("Disconnecting from MQTT broker...")
    client.loop_stop()
    client.disconnect()
