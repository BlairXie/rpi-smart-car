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
p1.start(40) #to start PWM
p2.start(50)

def forward():
    GPIO.output(GPIO_IN1,False)
    GPIO.output(GPIO_IN2,True)
    GPIO.output(GPIO_IN3,True)
    GPIO.output(GPIO_IN4,False)

def turnLeft():
    GPIO.output(GPIO_IN1,False)
    GPIO.output(GPIO_IN2,False)
    GPIO.output(GPIO_IN3,True)
    GPIO.output(GPIO_IN4,False)

def turnRight():
    GPIO.output(GPIO_IN1,False)
    GPIO.output(GPIO_IN2,True)
    GPIO.output(GPIO_IN3,False)
    GPIO.output(GPIO_IN4,False)

def forward_avoid_obstacle():
    dist = distance()
    print("Measured Distance = {:.2f} cm".format(dist))
    if(dis < 10 ):
        turnLeft()
        time.sleep(1)
    else:
        forward()


try:
    while 1:
        forward_avoid_obstacle()

# Reset by pressing CTRL + C
except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    print("Measurement stopped by User")
    GPIO.cleanup()
