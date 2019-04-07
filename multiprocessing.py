#!/usr/bin/python3

import multiprocessing import multiprocessing
from flask_server import *
from ultrasonic import *
def motor_process():
    try:
        while True:
                dist = distance()
                print("Measured Distance = {:.2f} cm".format(dist))
                time.sleep(0.05)

            # Reset by pressing CTRL + C
    except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()


def flask_thread():
    app.run(host='0.0.0.0',port=80,debug=True,processes=2)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=motor_process)
    p1.start()

    p2 = multiprocessing.Process(target=flask_thread)
    p2.start()
    p2.join()
