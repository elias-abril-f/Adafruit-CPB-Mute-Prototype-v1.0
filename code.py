import time
import board
import neopixel
import digitalio

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

#  setup for the onboard neopixels
pixel_pin = board.NEOPIXEL
num_pixels = 10
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)

#  variables for colours, add here any extra colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

#  set up the internal buttons and switch
# (the buttons are pull-down and the switch is up)
buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)

buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

#  HID keyboard input setup
hid = HIDService()
keyboard = Keyboard(hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# BLUETOOTH SETUP
device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "PROTOTYPE V1.1"  # change name here

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected")
    print(ble.connections)

#  state machines
#  for button debouncing
buttonA_pressed = False
buttonB_pressed = False
longPressA = False
longPressB = False
#  default mute states
microphone_mute = True
video_off = True
#  time.monotonic() tracker for debouncing and long press
clock = time.monotonic()


while True:
    while not ble.connected:
        pass
    print("Start typing:")

    while ble.connected:
        #  button debouncing
        if not buttonA.value and buttonA_pressed:
            buttonA_pressed = False
        if not buttonB.value and buttonB_pressed:
            buttonB_pressed = False
        #  colour of the pixels based on different states.
        if microphone_mute:
            if switch.value:
                pixels[5] = OFF
                pixels[6] = OFF
                pixels[7] = RED
                pixels[8] = OFF
                pixels[9] = OFF
                pixels.show()
            if not switch.value:
                pixels[5] = WHITE
                pixels[6] = WHITE
                pixels[7] = RED
                pixels[8] = WHITE
                pixels[9] = WHITE
                pixels.show()

        if video_off:
            if switch.value:
                pixels[0] = OFF
                pixels[1] = OFF
                pixels[2] = RED
                pixels[3] = OFF
                pixels[4] = OFF
                pixels.show()
            if not switch.value:
                pixels[0] = WHITE
                pixels[1] = WHITE
                pixels[2] = RED
                pixels[3] = WHITE
                pixels[4] = WHITE
                pixels.show()

        if not microphone_mute:
            if switch.value:
                pixels[5] = OFF
                pixels[6] = OFF
                pixels[7] = GREEN
                pixels[8] = OFF
                pixels[9] = OFF
                pixels.show()
            if not switch.value:
                pixels[5] = WHITE
                pixels[6] = WHITE
                pixels[7] = GREEN
                pixels[8] = WHITE
                pixels[9] = WHITE
                pixels.show()

        if not video_off:
            if switch.value:
                pixels[0] = OFF
                pixels[1] = OFF
                pixels[2] = GREEN
                pixels[3] = OFF
                pixels[4] = OFF
                pixels.show()
            if not switch.value:
                pixels[0] = WHITE
                pixels[1] = WHITE
                pixels[2] = GREEN
                pixels[3] = WHITE
                pixels[4] = WHITE
                pixels.show()

        #  if you press button a
        if (buttonA.value and not buttonA_pressed):
            buttonA_pressed = True
            clock = time.monotonic()  # start counting the time
            time.sleep(0.3)  # change here for responsiveness of the click
            if buttonA.value and buttonA_pressed:
                print("Long press A")
                while buttonA.value and buttonA_pressed:
                    longPressA = True
                    pixels.brightness += 0.0025
                    pixels.show()
            else:
                if video_off:
                    print("buttonA")
                    video_off = False
                    longPressA = False
                elif not video_off:
                    print("buttonA")
                    video_off = True
                    longPressA = False
                keyboard.send(Keycode.ALT, Keycode.V)

        #  if you press button B
        if (buttonB.value and not buttonB_pressed):
            buttonB_pressed = True
            clock = time.monotonic()
            time.sleep(0.3)
            if buttonB.value and buttonB_pressed:
                print("Long press B")
                while buttonB.value and buttonB_pressed:
                    longPressB = True
                    pixels.brightness -= 0.0025
                    pixels.show()
            else:
                if microphone_mute:
                    print("buttonB")
                    longPressB = True
                    microphone_mute = False
                    longPressB = False
                elif not microphone_mute:
                    print("buttonB")
                    microphone_mute = True
                    longPressB = False
                keyboard.send(Keycode.ALT, Keycode.A)

