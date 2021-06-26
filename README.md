# micropython flashy

Flash the in-built LED of the **M5 Atom Lite** based on data sent to a TCP socket
server. Stop flashing when button is pressed. Something like a light based
pager. Used in combination with my discord bot.

Place this at `/main.py` on the ESP32 using,
```sh
$ ampy --port /dev/ttyUSB0 put main.py
```

Create a file called `wifi.cfg` which contains `ssid` and `password` of your
wireless network. It should look like,
```json
{
    "ssid" : "your ssid here",
    "password" : "your password here"
}
```

Place this at `/wifi.cfg` on the ESP32 using,
```sh
$ ampy --port /dev/ttyUSB0 put main.py
```

Schematics for the M5 Atom Lite are here, [https://docs.m5stack.com/en/core/atom_lite](https://docs.m5stack.com/en/core/atom_lite)

