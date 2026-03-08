from RPLCD.i2c import CharLCD
import time

COLS = 16
ROWS = 2
DELAY = 0.2

MESSAGES = [
    ("Hey y'all", "@bradgarropy"),
    ("The Bad Guys", "@juju"),
]

def write_frame(lcd, frame):
    lcd.home()
    for row in frame:
        lcd.write_string(row.ljust(COLS)[:COLS])
        lcd.crlf()

def scroll_message(lcd, line1, line2):
    padding = ' ' * COLS
    padded_line1 = padding + line1
    padded_line2 = padding + line2
    max_len = max(len(padded_line1), len(padded_line2))

    for i in range(max_len):
        frame = [
            padded_line1[i:i+COLS],
            padded_line2[i:i+COLS],
        ]
        write_frame(lcd, frame)
        time.sleep(DELAY)

def show_messages(lcd):
    while True:
        for line1, line2 in MESSAGES:
            scroll_message(lcd, line1, line2)

if __name__ == "__main__":
    lcd = None

    try:
        lcd = CharLCD(i2c_expander='PCF8574', address=0x27, cols=COLS, rows=ROWS)
        show_messages(lcd)
    finally:
        if lcd:
            lcd.clear()
