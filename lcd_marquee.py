"""
LCD Marquee - Display MQTT messages on a 16x2 LCD.

Subscribes to MQTT topic and scrolls incoming messages
across the LCD display, one at a time.
"""

import logging
import queue
import time

from RPLCD.i2c import CharLCD

import mqtt_client

# LCD Configuration
COLS = 16
ROWS = 2
DELAY = 0.2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger(__name__)


def write_frame(lcd, frame):
    """Write a single frame (2 lines) to the LCD."""
    lcd.home()
    for row in frame:
        lcd.write_string(row.ljust(COLS)[:COLS])
        lcd.crlf()


def scroll_message(lcd, line1, line2):
    """
    Scroll a message across the LCD from right to left.

    Message starts off-screen right, scrolls until off-screen left.
    """
    padding = " " * COLS
    padded_line1 = padding + line1
    padded_line2 = padding + line2
    max_len = max(len(padded_line1), len(padded_line2))

    for i in range(max_len):
        frame = [
            padded_line1[i : i + COLS],
            padded_line2[i : i + COLS],
        ]
        write_frame(lcd, frame)
        time.sleep(DELAY)


def main():
    lcd = None
    client = None

    try:
        # Initialize LCD
        logger.info("Initializing LCD display...")
        lcd = CharLCD(i2c_expander="PCF8574", address=0x27, cols=COLS, rows=ROWS)
        lcd.clear()
        logger.info("LCD initialized")

        # Initialize and connect MQTT
        client = mqtt_client.create_client()
        mqtt_client.connect(client)

        logger.info("Waiting for messages...")

        # Main loop: pull from queue and display
        while True:
            try:
                # Block until message available (timeout allows Ctrl+C)
                message, twitter = mqtt_client.message_queue.get(timeout=1.0)
                logger.info(f"Displaying: {message} / {twitter}")
                scroll_message(lcd, message, twitter)
                lcd.clear()
            except queue.Empty:
                # No message, keep waiting
                pass

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if client:
            mqtt_client.disconnect(client)
        if lcd:
            lcd.clear()


if __name__ == "__main__":
    main()
