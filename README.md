# 🟦 lcd marquee - pi

Python code that runs on a Raspberry Pi to receive real-time messages and display them on an LCD.

🔗 [https://lcd.bradgarropy.com][lcd-web]

![lcd marquee][lcd-marquee]

## Tech Stack

- [Raspberry Pi 5][raspberry-pi]
- [16x2 LCD][lcd]
- [Python][python]
- [RPLCD][rplcd]
- [paho-mqtt][paho-mqtt]
- [HiveMQ][hivemq]

## Development

Clone the repository.

```zsh
git clone https://github.com/bradgarropy/lcd-marquee-pi.git
```

Install dependencies.

```zsh
cd lcd-marquee-pi
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and fill in your MQTT credentials.

```zsh
cp .env.example .env
```

Start the application.

```zsh
python lcd_marquee.py
```

## Web Application

If you're interested in the web side of things, check out the [lcd-marquee-web][lcd-marquee-web] repository for the web application that sends messages to the LCD.

[lcd-marquee]: lcd-marquee.png
[raspberry-pi]: https://raspberrypi.com/products/raspberry-pi-5
[lcd]: https://sunfounder.com/products/i2c-lcd1602-module
[python]: https://python.org
[rplcd]: https://rplcd.readthedocs.io
[paho-mqtt]: https://eclipse.dev/paho/index.php?page=clients/python/index.php
[hivemq]: https://hivemq.com
[lcd-marquee-web]: https://github.com/bradgarropy/lcd-marquee-web
[lcd-web]: https://lcd.bradgarropy.com
