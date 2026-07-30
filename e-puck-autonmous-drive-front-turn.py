from controller import Robot
import random

TIME_STEP = 30


robot = Robot()


proximity_sensor0 = robot.getDevice("ps0")
proximity_sensor7 = robot.getDevice("ps7")

proximity_sensor0.enable(TIME_STEP)
proximity_sensor7.enable(TIME_STEP)


proximity_sensor1 = robot.getDevice("ps1")
proximity_sensor2 = robot.getDevice("ps2")

proximity_sensor1.enable(TIME_STEP)
proximity_sensor2.enable(TIME_STEP)


#motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")


left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))


left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
    
#ground sensor
ground_sensor = robot.getDevice("gs1")
ground_sensor.enable(TIME_STEP)

MAX_SPEED = 6.28
TURN_SPEED = 3.0

FRONT_THRESHOLD = 90 


#a helper function to check if the ground is gray
#this is needed to due to the complexity of sensors during movement
BLACK_THRESHOLD = 670 #Black threshold
WHITE_THRESHOLD = 700 #White threshold

#not needed to understand function too complex (code below this)
gray_count = 0

def is_gray(value):
    global gray_count

    if BLACK_THRESHOLD < value < WHITE_THRESHOLD:
        gray_count += 1
    else:
        gray_count = 0
    return gray_count >= 4

#not needed to understand function too complex (code above this)

while robot.step(TIME_STEP) != -1:

    proximity_sensor0_distance = proximity_sensor0.getValue()
    proximity_sensor7_distance = proximity_sensor7.getValue()
    
    #move forward
    left_motor.setVelocity(MAX_SPEED)
    right_motor.setVelocity(MAX_SPEED)

    #We found the goal now we stop
    if is_gray(ground_sensor.getValue()):
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
        break
    
    #Check to see if either of our front sensors see a wall and if so
    #follow our movement routine
    if proximity_sensor0_distance > FRONT_THRESHOLD or proximity_sensor7_distance > FRONT_THRESHOLD:
        #stop quickly
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
        robot.step(100)
    
        # Wall in front: turn right.
        left_motor.setVelocity(TURN_SPEED)
        right_motor.setVelocity(-TURN_SPEED)
        robot.step(725)
        
        #go forward
        left_motor.setVelocity(MAX_SPEED)
        right_motor.setVelocity(MAX_SPEED)
        robot.step(1000)
        
        #go left
        left_motor.setVelocity(-TURN_SPEED)
        right_motor.setVelocity(TURN_SPEED)
        robot.step(725)    