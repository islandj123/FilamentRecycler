#Julian France
#01-2023
#Motor module for Filament Recycler
import pwmio
import analogio
import digitalio

class Motor:
    def __init__(self, control, dir, step):
        self.control = control #ADC Pin that will control motor
        self.dir = dir #GPIO Pin that will set motor rotation direction
        self.step = step #GPIO Pin that will make motor rotate steps
        self.speed = 0 #Arbitrary 0-100 speed value

        #Initialize pot for motor speed control
        self.motor_pot = analogio.AnalogIn(Motor.control)

        #Initailize pwm pin for motor (STEP) control
        self.motor_step = pwmio.PWMOut(Motor.step, frequency = 100, duty_cycle = 65535//2, variable_frequency=True)

        #Initialize high/low pin for motor (DIR) control
        #HIGH is clockwise, LOW is ccw
        self.motor_dir = digitalio.DigitalInOut(Motor.dir)
        self.motor_dir.direction = digitalio.direction.OUTPUT
        self.motor_dir.value = True
        
    #Usage: motorConfig(new analog control, new dir pin, new step pin):
    def motorPinConfig(control, dir, step):
        #Change pot for motor speed control
        Motor.motor_pot = analogio.AnalogIn(control)

        #Change pwm pin for motor (STEP) control
        Motor.motor_step = pwmio.PWMOut(step, frequency = 100, duty_cycle = 65535//2, variable_frequency=True)

        #Change dir pin for motor (DIR) control
        Motor.motor_dir = digitalio.DigitalInOut(dir)
        Motor.motor_dir.direction = digitalio.direction.OUTPUT
        Motor.motor_dir.value = True

        Motor.Stop()

    #Stop's motor by removing PWM HIGH's
    def Stop():
        Motor.motor_step.duty_cycle = 0

    #Start's motor by setting duty cycle to 50%
    def Start():
        Motor.motor_step.duty_cycle = 65535//2

    #Set motor speed from 0 to 100%, negatives permitted
    #Will automatically call start/stop or reverse if necessary
    def setSpeed(motor_speed):
        #Select required direction
        if(motor_speed == 0):
            Motor.Stop()
            return 0
        elif(motor_speed < 0):
            Motor.motor_dir.value = False
        elif(motor_speed > 0):
            Motor.motor_dir.value = True
        else:
            return 1
        
        #Hard limit to speed
        motor_speed = 100 if motor_speed > 100 else -100 if motor_speed < -100 else motor_speed
         
        Motor.Start()
        Motor.motor_step.frequency = 10*motor_speed
        return 0

    def getSpeed():
        return Motor.motor_step.frequency / 10
    



    
         