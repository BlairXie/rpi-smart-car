# --coding: utf-8 --
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#定义 GPIO 引脚

GPIO_IN1 = 14
GPIO_IN2 = 15

GPIO.setup(GPIO_IN1, GPIO.OUT)
GPIO.setup(GPIO_IN2, GPIO.OUT)

GPIO.output(GPIO_IN1,True)
GPIO.output(GPIO_IN2,True)

p = GPIO.PWM(GPIO_IN1, 400) # channel=? frequency=50Hz（需要修改高电平引脚）
p.start(0) #to start PWM

try:
    # while 1:
    #     for dc in range(0,90,2):
    #         p.ChangeDutyCycle(dc)
    #         time.sleep(0.3)
    pass
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    p.stop()
    print("Measurement stopped by User")
    GPIO.cleanup()
