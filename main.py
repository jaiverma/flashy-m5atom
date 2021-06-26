import machine
import network
import neopixel
import time
import socket
import random
import json
import uasyncio as asyncio

PORT = 10002

LED_PIN = machine.Pin(27)
LED_NP = neopixel.NeoPixel(LED_PIN, 1)
BTN_PIN = machine.Pin(39, machine.Pin.IN)

def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('[+] Connecting to network: {}'.format(ssid))
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            time.sleep(0.5)
            pass
    print('[*] Connected: {}'.format(sta_if.ifconfig()))

async def flash():
    random.seed(time.time())
    def get_rgb():
        # not too bright
        r = random.randint(0, 30)
        g = random.randint(0, 30)
        b = random.randint(0, 30)
        return (r, g, b)

    # flash LEDs in 5 rapid flash cycles
    while True:
        await asyncio.sleep_ms(1000)
        colour = get_rgb()
        for _ in range(5):
            LED_NP[0] = colour
            LED_NP.write()
            await asyncio.sleep_ms(60)
            LED_NP[0] = (0, 0, 0)
            LED_NP.write()
            await asyncio.sleep_ms(60)

async def start_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    conn, addr = s.accept()
    task = None
    while conn:
        # receive one block of input from client and kill connection
        print('[*] Connection from: {}'.format(addr))
        data = conn.recv(1024)
        print('[+] Received: {}'.format(data))
        if data.strip() == b'HELLO':
            task = asyncio.create_task(flash())
        conn.sendall(b'ACK')
        conn.close()
        break
    s.close()
    return task

async def wait_for_task(task):
    # i'm using the m5 atom lite which doesn't support irq callbacks
    # for the inbuilt button, so using a while loop instead :(
    while True:
        if BTN_PIN.value() == 0:
            print('[*] acknowledged, stopping flash...')
            task.cancel()
            break
        await asyncio.sleep_ms(100)

async def async_main():
    # server loop
    # wait for connection, server single client, restart server
    while True:
        hello_task = await start_server(PORT)
        if hello_task is not None:
            asyncio.create_task(wait_for_task(hello_task))
            try:
                await hello_task
            except asyncio.CancelledError:
                pass
            finally:
                LED_NP[0] = (0, 0, 0)
                LED_NP.write()
        print('[+] restarting...')

def main():
    LED_NP[0] = (0, 0, 0)
    LED_NP.write()

    data = None
    with open('/wifi.cfg') as f:
        data = json.load(f)

    connect_wifi(data['ssid'], data['password'])
    asyncio.run(async_main())

main()
