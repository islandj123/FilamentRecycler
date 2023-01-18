#Should cut down imports to only have what is used
import board
import busio as io
import pwmio
from digitalio import DigitalInOut, Direction, Pull
import analogio
import terminalio   
import displayio
import time
import adafruit_thermistor as thermio
import adafruit_displayio_ssd1306 as ssd1306
from adafruit_display_text import label 
from math import ceil, sin, pi
import array
import audiocore
import audiobusio
from collections import deque
import gc
import motor

#Define pins
THERMISTOR = board.A0
HEATER_POT = board.A1
MOTOR_POT = board.A2

DISPLAY_SDA = board.GP0
DISPLAY_SCL = board.GP1
MOTOR_STEP = board.GP2
MOTOR_DIR = board.GP3
HEATER_PWM = board.GP4
BUTTON = board.GP5
BCLK = board.GP6
LRC = board.GP7
DIN = board.GP8

class Button:
    def __init__(self):
        self.pin = DigitalInOut(BUTTON)
        self.pin.direction = Direction.INPUT
        self.pin.pull = Pull.UP

        self.prev_state = False

        #Only trigger on button press, once
        if(self.pin.value != self.prev_state):
            if(self.pin.value):
                self.prev_state = True
            else:
                self.prev_state = False


class Display:
    def __init__(self, SCL, SDA):
        #Stop Displays from displaying shell
        displayio.release_displays()    

        #Initialize i2c for display
        i2c = io.I2C(Display.SCL, Display.SDA)
        display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
        display = ssd1306.SSD1306(display_bus, width=128, height=32)

        # Make a group
        self.main_group = displayio.Group()

        #Create bitmap from file
        bitmap = displayio.OnDiskBitmap("/Logo.bmp")

        #Create a tilegrid to hold bitmap
        bitmap_tile = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

        #Make a palette (all white)
        #color_palette = displayio.Palette(1)
        #color_palette[0] = 0xFFFFFF  # White

        self.text = "The quick brown fox \n jumps over the Auri!"
        self.text_area = label.Label(terminalio.FONT, text=self.text, color=0xFFFF00, x=0, y=0)

        #Attach tiles to group
        self.main_group.append(bitmap_tile)
        self.main_group.append(self.text_area)

        #Show main group
        display.show(self.main_group)


class Heater:
    def __init__(self, control, thermistor, heater):
        self.control = control
        self.thermistor = thermistor
        self.heater = heater
        self.target_temp = 0

        #Initialize pot for heater control
        self.pot = analogio.AnalogIn(Heater.control)

        #Initialize thermistor object
        #(Analog Input, Series Resistance, Nominal Resistance, Nominal Temp, Beta Coeff., side of voltage divider)
        self.thermistor = thermio.Thermistor(Heater.thermistor, 9950.0, 100000.0, 18.0, 3950.0, high_side=False)

        #Initialize pin for heater control
        self.PWM = pwmio.PWMOut(Heater.heater, frequency = 10, duty_cycle = 65535//2, variable_frequency=True, variable_duty_cycle=True)


class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0
    
    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        return output


class Audio:
    def __init__(self, volume, frequency, length):
        #Create audio object
        self.tone = audiobusio.I2SOut(BCLK, LRC, DIN)
        #Create array for storing tone sequence
        self.tone_queue = deque()

    def audioConfig(self, volume, frequency, length):
        self.volume = volume
        self.frequency = frequency
        self.length = length
        #Create new sine wave with parameters
        self.sine_wave = array.array("h", [0] * self.length+1)
        for i in range(self.length):
            self.sine_wave[i] = int((sin(pi * 2 * i / self.length)) * self.volume * (2 ** 15 -1))
        self.sine_wave[self.length] = self.length
        #Potentially have to define new RawSample here as well
        #self.sine_wave_test = audiocore.RawSample(self.sine_wave)
        return self.sine_wave

    def pushTone(self, volume, frequency, length):
        #Create a new sine wave array with appended length
        new_sine = self.audioConfig(volume, frequency, length)
        #Append new sine to tone queue
        self.tone_queue.append(new_sine)
    
    def playTone(self):
        #Dequeue tone queue to get next tone
        sine_wave = self.tone_queue.popleft()
        #Extract sound portion from sine_wave array
        sine_wave_note = audiocore.RawSample(sine_wave[0:len(sine_wave)-2])
        #Extract length from sine_wave array
        length = sine_wave[len(sine_wave)-1]
        #Play tone
        self.tone.play(sine_wave_note, loop=False)
        #Wait for appropriate amount of time
        time.sleep(length)


def main():
    #Create Display object
    display1 = Display(DISPLAY_SCL, DISPLAY_SDA)

    #Create Heater object
    heater1 = Heater(HEATER_POT, THERMISTOR, HEATER_PWM)
    heater1.PWM.duty_cycle = 0 #Use this to control heater power
    heater1.target_temp = 0
    rate = 0

    #Create Motor object
    motor1 = Motor(MOTOR_POT, MOTOR_DIR, MOTOR_STEP)
    motor1.speed = 0

    #Create PID object
    KP = 1.2
    #These values can remain 0, unless a tuned proportional controller is not sufficient
    KI = 0.0005
    KD = 0.01
    pid = PID(KP, KI, KD)

    #Create Audio object
    audio = Audio(0.1, 440, 8000)
    #Queue bootup sequence
    audio.pushTone(0.1, 440, 8000)
    audio.pushTone(0.1, 600, 8000)
    audio.pushTone(0.1, 700, 8000)
    audio.pushTone(0.1, 800, 8000)
    audio.pushTone(0.1, 330, 8000)

    #Draw bootup info screen
    display1.text_area.text = "FilaMaker V0.1"
    #Play bootup sound sequence
    for x in audio.tone_queue:
        audio.playTone()
  

    while True:   
        #Get and convert pot values
        heater1.target_temp = ceil(heater1.pot.value/65535*80)+150
        motor1.speed = ceil(motor1.motor_pot.value/65535*101)-1

        #Change motor speed if target speed has changed
        if(motor1.speed != motor1.getSpeed()):
            motor1.setSpeed(motor1.speed)

        #Regulate heater temperature--------------------------------#
        #First calculate error between desired and actual temperature
        error = heater1.target_temp - heater1.thermistor.temperature
        #Find a correction to apply
        correction = pid.update(error, dt=1)
        #Adjust correction to have desired effect (rate should be 0-1 value)
        rate = correction*0.05
        if(rate > 1):
            rate = 1
        elif(rate < 0):
            rate = 0

        #Final heater control
        if(heater1.thermistor.temperature > heater1.target_temp):
            heater1.PWM.duty_cycle = 0
        elif(heater1.thermistor.temperature < heater1.target_temp):
            heater1.PWM.duty_cycle = rate*(65535)*0.5 #0.5 for testing/safety
        
        #Draw to display
        display1.text_area.text = "Nozzle Temp: {}C ({})\nMotor Speed: {}%".format(heater1.thermistor.temperature, heater1.target_temp, motor1.speed)
        time.sleep(0.01)
        gc.collect()
        #print('{}'.format(gc.mem_free()))
    
if __name__ == "__main__":
    main()
    
