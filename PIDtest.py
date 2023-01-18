#PID testing file
import time
import random


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


def main():
    #Create PID object
    KP = 1.2
    #These values can remain 0, unless a tuned proportional controller is not suffficient
    KI = 0.006 #0.0006 is good
    KD = 0.05 #0.01 is good
    pid = PID(KP, KI, KD)
        
    actual = 20
    target = 120
    rate = 0
    power = 1



    timer = 0

    while(True):
        #First calculate error between desired and actual temperature
        error = target - actual
        #Find a correction to 
        correction = pid.update(error, dt=1)

        #Should be value between 0 and 1
        rate = correction*0.05
        if(rate > 1):
            rate = 1
        elif(rate < 0):
            rate = 0


        actual = actual + power*rate - 0.1*random.randrange(1, 3, 1)

        #print("Rate: " + str(round(rate, 2)) + "/ Actual: " + str(round(actual, 2)))
        
        f = open("example.txt", "r")
        contents = f.readlines()
        print(contents)
        if(len(contents) < 10):
            f = open("example.txt", "a") 
            f.write(str(round(timer, 2)) + "," + str(round(actual, 2)) + "\n")
        else:
            f = open("example.txt", "w")
            contents.pop(0)
            f.write(contents[0] + contents[1] + contents[2] + contents[3] + contents[4] + contents[5] + contents[6] + contents[7] + 
            contents[8] + str(round(timer, 2)) + "," + str(round(actual, 2)) + "\n")
        f.close()

        timer = timer + 0.201
        time.sleep(0.2)

if __name__ == "__main__":
    main()