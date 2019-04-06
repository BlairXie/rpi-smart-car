# --coding: utf-8 --
import RPi.GPIO as GPIO
import time
from ultrasonic import distance
GPIO.setmode(GPIO.BCM)
#定义 GPIO 引脚

GPIO_IN1 = 14
GPIO_IN2 = 15
GPIO_IN3 = 18
GPIO_IN4 = 23
ENA = 7
ENB = 8

GPIO.setwarnings(False)
GPIO.setup(GPIO_IN1, GPIO.OUT)
GPIO.setup(GPIO_IN2, GPIO.OUT)
GPIO.setup(GPIO_IN3, GPIO.OUT)
GPIO.setup(GPIO_IN4, GPIO.OUT)
GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(ENB,GPIO.OUT)

p1 = GPIO.PWM(ENA, 200) # channel=? frequency=50Hz（需要修改高电平引脚）
p2 = GPIO.PWM(ENB, 200) # channel=? frequency=50Hz（需要修改高电平引脚）
p1.start(41) #to start PWM
p2.start(48)
pre_distance = 0
turn_flag = 1 # 1代表 turn left , 0 代表 turn right

def forward():
    GPIO.output(GPIO_IN1,False)
    GPIO.output(GPIO_IN2,True)
    GPIO.output(GPIO_IN3,True)
    GPIO.output(GPIO_IN4,False)

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

def forward_avoid_obstacle():
    global pre_distance
    global turn_flag
    dist = distance()
    print("Measured Distance = {:.2f} cm".format(dist))
    if(dist < 25 ):
        if dist < pre_distance - 1.5:
            turn_flag = not turn_flag
        if turn_flag:
            turnLeft()
        else:
            turnRight()
        pre_distance = dist
    else:
        pre_distance =0
        turn_flag = 1
        forward()
    time.sleep(0.08)


try:
    while 1:
        forward_avoid_obstacle()

# Reset by pressing CTRL + C
except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    print("Measurement stopped by User")
    GPIO.cleanup()
