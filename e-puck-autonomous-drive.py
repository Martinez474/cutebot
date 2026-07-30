from controller import Robot
import random

TIME_STEP = 30

robot = Robot()


#motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")


left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))


left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
    

MAX_SPEED = 6.28


while robot.step(TIME_STEP) != -1:

    left_speed = MAX_SPEED
    right_speed = MAX_SPEED


    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
    
    