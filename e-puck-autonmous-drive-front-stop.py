from controller import Robot
import random

TIME_STEP = 30


robot = Robot()


proximity_sensor0 = robot.getDevice("ps0")
proximity_sensor7 = robot.getDevice("ps7")


#motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")


left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))


left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
    
    
    

MAX_SPEED = 6.28
TURN_SPEED = 3.0

FRONT_THRESHOLD = 90 

while robot.step(TIME_STEP) != -1:

    left_speed = 0
    right_speed = 0

    proximity_sensor0_distance = proximity_sensor0.getValue()
    proximity_sensor7_distance = proximity_sensor7.getValue()
    
    front_value = max(proximity_sensor0_distance, proximity_sensor7_distance)
    
    front_wall = front_value > FRONT_THRESHOLD
    

    
    if front_wall:
        # Wall in front: stop
        left_speed = 0
        right_speed = 0
    else:
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED


    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
    
    