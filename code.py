import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

import time
import board
import digitalio
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.05)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)

buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

pressed = time.monotonic()

ledCounterAudio = 1
ledCounterVideo = 1

hid = HIDService()

device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "Prototype V1.0"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected")
    print(ble.connections)
    pixels.fill(RED)
    pixels.show()

k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)
while True:
    while not ble.connected:
        pass
    print("Start typing:")

    while ble.connected:
        if time.monotonic() - pressed < 0.2:
            continue
        if buttonA.value:
            print("ButtonA")  # button is pushed
            k.send(Keycode.ALT, Keycode.A)
            ledCounterAudio += 1
            if ledCounterAudio > 2:
                ledCounterAudio = 1

            if ledCounterAudio == 1:
                pixels[0] = GREEN
                pixels[1] = GREEN
                pixels[2] = YELLOW
                pixels[3] = GREEN
                pixels[4] = GREEN
            if ledCounterAudio == 2:
                pixels[0] = RED
                pixels[1] = RED
                pixels[2] = BLUE
                pixels[3] = RED
                pixels[4] = RED
            pixels.show()
            pressed = time.monotonic()

        if buttonB.value:
            print("ButtonB")  # button is pushed
            k.send(Keycode.ALT, Keycode.V)
            ledCounterVideo += 1
            if ledCounterVideo > 2:
                ledCounterVideo = 1
            if ledCounterVideo == 1:
                pixels[5] = GREEN
                pixels[6] = GREEN
                pixels[7] = CYAN
                pixels[8] = GREEN
                pixels[9] = GREEN
            if ledCounterVideo == 2:
                pixels[5] = RED
                pixels[6] = RED
                pixels[7] = PURPLE
                pixels[8] = RED
                pixels[9] = RED
            pixels.show()
            pressed = time.monotonic()
