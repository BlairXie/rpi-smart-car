# --coding: utf-8 --
import RPi.GPIO as GPIO
import time
import sys
from ultrasonic import distance
GPIO.setmode(GPIO.BCM)
#定义 GPIO 引脚


GPIO_IN1 = 14
GPIO_IN2 = 15
GPIO_IN3 = 18
GPIO_IN4 = 23
ENA = 7
ENB = 8
run_flag = 0

GPIO.setwarnings(False)
GPIO.setup(GPIO_IN1, GPIO.OUT)
GPIO.setup(GPIO_IN2, GPIO.OUT)
GPIO.setup(GPIO_IN3, GPIO.OUT)
GPIO.setup(GPIO_IN4, GPIO.OUT)
GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(ENB,GPIO.OUT)

p1 = GPIO.PWM(ENA, 200) #
p2 = GPIO.PWM(ENB, 200) #
p1.start(31) #to start PWM
p2.start(35)
def forward():
    GPIO.output(GPIO_IN1,False)
    GPIO.output(GPIO_IN2,True)
    GPIO.output(GPIO_IN3,True)
    GPIO.output(GPIO_IN4,False)
def backward():
    GPIO.output(GPIO_IN1,True)
    GPIO.output(GPIO_IN2,False)
    GPIO.output(GPIO_IN3,False)
    GPIO.output(GPIO_IN4,True)

def turnLeft():
    GPIO.output(GPIO_IN1,True)
    GPIO.output(GPIO_IN2,False)
    GPIO.output(GPIO_IN3,True)
    GPIO.output(GPIO_IN4,False)

def turnRight():
    GPIO.output(GPIO_IN1,False)
    GPIO.output(GPIO_IN2,True)
    GPIO.output(GPIO_IN3,False)
    GPIO.output(GPIO_IN4,True)

def pause():
    GPIO.output(GPIO_IN1,False)
    GPIO.output(GPIO_IN2,False)
    GPIO.output(GPIO_IN3,False)
    GPIO.output(GPIO_IN4,False)

def forward_avoid_obstacle():
    dist = distance()
    print("Measured Distance = {:.2f} cm".format(dist))
    if(dist < 25 ):
        backward()
        time.sleep(0.2)
        p1.ChangeDutyCycle(41)#50
        p2.ChangeDutyCycle(48)#57
        turnLeft()
        time.sleep(0.2)
        return
    else:
        p1.ChangeDutyCycle(31)#41
        p2.ChangeDutyCycle(35)#48
        forward()
    time.sleep(0.08)


def motion_ctrol(share_state):
    global run_flag
    try:
        while 1:
            try:
                run_flag = share_state.value
            except:
                pass
            if run_flag == 0:
                pause()
                print("pause")
            elif run_flag == 1:
                forward_avoid_obstacle()
                print('move forward')
            elif run_flag == 2:
                turnLeft()
                time.sleep(1)
                print("turn left")
                pause()
                time.sleep(1)
                run_flag = 1
            elif run_flag == 3:
                turnRight()
                time.sleep(1)
                print("turn right")
                pause()
                time.sleep(1)
                run_flag = 1

            # exit by pressing CTRL + C
    except KeyboardInterrupt:
        p1.stop()
        p2.stop()
        print("Measurement stopped by User")
        GPIO.cleanup()
        sys.exit(0)
