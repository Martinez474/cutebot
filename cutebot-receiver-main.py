from microbit import *
from time import sleep_us
from machine import time_pulse_us
import radio

CUTEBOT_ADDR = 0x10

left_light = 0x04
right_light = 0x08


class CUTEBOT(object):
    def __init__(self):
        i2c.init()
        self.__pin_e = pin12
        self.__pin_t = pin8
        self.__pinL = pin13
        self.__pinR = pin14
        self.__pinL.set_pull(self.__pinL.PULL_UP)
        self.__pinR.set_pull(self.__pinR.PULL_UP)

    def set_motors_speed(self, left_wheel_speed: int, right_wheel_speed: int):
        if left_wheel_speed > 100 or left_wheel_speed < -100:
            raise ValueError('left speed error, -100~100')
        if right_wheel_speed > 100 or right_wheel_speed < -100:
            raise ValueError('right speed error, -100~100')

        left_direction = 0x02 if left_wheel_speed > 0 else 0x01
        right_direction = 0x02 if right_wheel_speed > 0 else 0x01

        left_wheel_speed = abs(left_wheel_speed)
        right_wheel_speed = abs(right_wheel_speed)

        i2c.write(CUTEBOT_ADDR, bytearray([0x01, left_direction, left_wheel_speed, 0]))
        i2c.write(CUTEBOT_ADDR, bytearray([0x02, right_direction, right_wheel_speed, 0]))

    def stop(self):
        self.set_motors_speed(0, 0)

    def set_car_light(self, light: int, R: int, G: int, B: int):
        if R > 255 or G > 255 or B > 255:
            raise ValueError('RGB is error')

        i2c.write(CUTEBOT_ADDR, bytearray([light, R, G, B]))

    def get_distance(self, unit: int = 0):
        self.__pin_e.read_digital()
        self.__pin_t.write_digital(1)
        sleep_us(10)
        self.__pin_t.write_digital(0)

        ts = time_pulse_us(self.__pin_e, 1, 25000)

        if ts < 0:
            return None

        distance = round(ts * 34 / 2 / 1000)

        if unit == 0:
            return distance
        elif unit == 1:
            return round(distance / 30.48, 2)

    def is_left_tracker_black(self):
        return self.__pinL.read_digital() == 0

    def is_right_tracker_black(self):
        return self.__pinR.read_digital() == 0

    def get_tracking(self):
        left_black = self.is_left_tracker_black()
        right_black = self.is_right_tracker_black()

        if not left_black and not right_black:
            return 0      # both white
        elif left_black and not right_black:
            return 10     # left black, right white
        elif not left_black and right_black:
            return 1      # left white, right black
        elif left_black and right_black:
            return 11     # both black


ct = CUTEBOT()

radio.on()
radio.config(group=7)

MOVE_SPEED = 30
TURN_SPEED = 25

# Start stopped: both red
ct.set_car_light(left_light, 255, 0, 0)
ct.set_car_light(right_light, 255, 0, 0)
ct.stop()

while True:
    message = radio.receive()

    if message == "forward":
        display.show(Image.ARROW_N)

        # Go = both green
        ct.set_car_light(left_light, 0, 255, 0)
        ct.set_car_light(right_light, 0, 255, 0)

        ct.set_motors_speed(MOVE_SPEED, MOVE_SPEED)

    elif message == "left":
        display.show(Image.ARROW_W)

        # Left turn = left light blue, right light green
        ct.set_car_light(left_light, 0, 0, 255)
        ct.set_car_light(right_light, 0, 255, 0)

        ct.set_motors_speed(-TURN_SPEED, TURN_SPEED)

    elif message == "right":
        display.show(Image.ARROW_E)

        # Right turn = right light blue, left light green
        ct.set_car_light(right_light, 0, 0, 255)
        ct.set_car_light(left_light, 0, 255, 0)

        ct.set_motors_speed(TURN_SPEED, -TURN_SPEED)

    elif message == "stop":
        display.show(Image.SQUARE_SMALL)

        # Stop = both red
        ct.set_car_light(left_light, 255, 0, 0)
        ct.set_car_light(right_light, 255, 0, 0)

        ct.stop()

    sleep(20)