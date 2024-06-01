import board
import time
import digitalio
import busio
import analogio
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from config import channel, left_fader_cc, middle_fader_cc, right_fader_cc

#MIDI settings
#channel
#channel = 1
#cc
#left_fader_cc = 2
#middle_fader_cc = 11
#right_fader_cc = 1

#pins
left_fader = board.GP28
middle_fader = board.GP27
right_fader = board.GP26
midi_out_pin = board.GP4

#variable set up
analog_pins = [left_fader, middle_fader, right_fader]
analog_in = [analogio.AnalogIn(a_in) for a_in in analog_pins]
fader_out = [0] * len(analog_pins)
fader_cc = [left_fader_cc, middle_fader_cc, right_fader_cc]

#error handling
if type(channel) != int:
    channel = 1
channel = max(0, min(15, channel - 1))
default_cc = [2,11,1]
for i, fader in enumerate(fader_cc):
    if type(fader) != int:
        fader = default_cc[i]
    fader = max(0, min(127, fader))

#midi uart setup
midiuart = busio.UART(midi_out_pin, baudrate=31250)    
hex_dict_cc = [0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF]

#Functions
#send midi data
def send_midi_control(control, value, channel):
    global midiuart    
    midiuart.write(bytes([hex_dict_cc[channel], fader_cc[i], fader_out[i]]))
    midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=channel)
    midi.send([ControlChange(control, value)])

while True:
#read fader inputs
    for i, fader in enumerate(analog_in):
        fader_out[i] = int((fader.value - 1792) / 480)
        fader_out[i] = max(0, min(127, fader_out[i]))

#send midi data
    for i, fader in enumerate(fader_out):
        send_midi_control(fader_cc[i], fader_out[i], channel)
        
    time.sleep(0.001)