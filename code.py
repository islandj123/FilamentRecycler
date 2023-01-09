#Should cut down imports to only have what is used
import board
import busio as io
import pwmio
import digitalio
import analogio
import terminalio
import displayio
import time
import adafruit_thermistor as thermio
import adafruit_displayio_ssd1306 as ssd1306
from adafruit_display_text import label 
from math import ceil
import gc

#Define pins
THERMISTOR = board.A0
HEATER_POT = board.A1
MOTOR_POT = board.A2

DISPLAY_SDA = board.GP0
DISPLAY_SCL = board.GP1
MOTOR_STEP = board.GP2
MOTOR_DIR = board.GP3
HEATER_PWM = board.GP4


def displayInit():
    #Stop Displays from displaying shell
    displayio.release_displays()

    #Initialize i2c for display
    i2c = io.I2C(DISPLAY_SCL, DISPLAY_SDA)
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
    display = ssd1306.SSD1306(display_bus, width=128, height=32)

    # Make the display context
    main_group = displayio.Group()
    display.show(main_group)

    color_bitmap = displayio.Bitmap(128, 32, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White

    text = "The quick brown fox \n jumps over the Auri!"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=3, y=4)
    main_group.append(text_area)


def heaterInit():
    #Initialize pot for heater control
    heater_pot = analogio.AnalogIn(HEATER_POT)

    #Initialize thermistor object
    thermistor = thermio.Thermistor(THERMISTOR, 9950.0, 100000.0, 18.0, 3950.0, high_side=False)

    #Initialize pin for heater control
    heater_pwm = pwmio.PWMOut(HEATER_PWM, frequency = 10, duty_cycle = 65535//2, variable_frequency=True)


#Set motor speed from 0 to 100%, negatives allowed
#Will automatically call start/stop/reverse if necessary
def setMotorSpeed(motor_speed):
    #Select required direction
    if(motor_speed == 0):
        stopMotor()
        return 0
    elif(motor_speed < 0):
        motor_dir.value = False
    elif(motor_speed > 0):
        motor_dir.value = True
    else:
        return 1
    
    #Hard limit to speed
    #motor_speed = 100 if motor_speed > 100
    #motor_speed = -100 if motor_speed < -100
    
    startMotor()
    motor_step.frequency = 10*motor_speed
    return 0
    
    
def stopMotor():
    motor_step.duty_cycle = 0


def startMotor():
    motor_step.duty_cycle = 65535//2


def motorInit()
    #Initialize pot for motor speed control
    motor_pot = analogio.AnalogIn(MOTOR_POT)

    #Initailize pwm pin for motor (STEP) control
    motor_step = pwmio.PWMOut(MOTOR_STEP, frequency = 100, duty_cycle = 65535//2, variable_frequency=True)

    #Initialize high/low pin for motor (DIR) control
    #HIGH is clockwise, LOW is ccw
    motor_dir = digitalio.DigitalInOut(MOTOR_DIR)
    motor_dir.direction = digitalio.direction.OUTPUT
    motor_dir.value = True

    stopMotor()
    

def main():
    displayInit()
    heaterInit()
    motorInit()

    #Draw bootup info screen
    text_area.text = "FilaMaker V0.1"
    time.sleep(2.0)
    
    PWM = 0.35
    prev_motor_speed = 150

    while True:
        #Switch heater pin to HIGH
        #heater_pwm.value = True
        #print('Pin Output: {}'.format(pin.value))
        #print('Thermistor Temp: {} C'.format(thermistor.temperature))
        
        #Regulate heater temperature
        if(thermistor.temperature > 40):
            PWM = 0
        else:
            PWM = 0.35
        
        #Switch heater pin to LOW
        #heater_pwm.value = False
        #print('Pin Output: {}'.format(pin.value))
        
        #Get and convert pot values
        target_temp = ceil(heater_pot.value/65535*80)+150
        motor_speed = ceil(motor_pot.value/65535*101)-1
        
        #Set new target temp if necessary
        if(motor_speed != prev_motor_speed):
            setMotorSpeed(motor_speed)
            prev_motor_speed = motor_speed
            
        #Draw to display
        text_area.text = "Nozzle Temp: {}C ({})\nMotor Speed: {}%".format(thermistor.temperature, target_temp, motor_speed)
        time.sleep(0.05)
        gc.collect()
        #print('{}'.format(gc.mem_free()))
    
if __name__ == "__main__":
    main()
    
