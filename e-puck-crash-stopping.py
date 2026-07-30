from controller import Robot
import random

TIME_STEP = 30


robot = Robot()


# proximity_sensor0 = robot.getDevice("ps0")
# proximity_sensor7 = robot.getDevice("ps7")

# proximity_sensor0.enable(TIME_STEP)
# proximity_sensor7.enable(TIME_STEP)


# proximity_sensor1 = robot.getDevice("ps1")
# proximity_sensor2 = robot.getDevice("ps2")

# proximity_sensor1.enable(TIME_STEP)
# proximity_sensor2.enable(TIME_STEP)
ps = []
for i in range(8):
    sensor = robot.getDevice("ps" + str(i))
    sensor.enable(TIME_STEP)
    ps.append(sensor)


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

#75 is about the lowerst you should set the value
FRONT_THRESHOLD = 90 
SIDE_THRESHOLD = 75

#a helper function to check if the ground is gray
#this is needed to due to the complexity of sensors during movement
BLACK_THRESHOLD = 670 #Black threshold
WHITE_THRESHOLD = 700 #White threshold
gray_count = 0

def is_gray(value):
    global gray_count
    

    if BLACK_THRESHOLD < value < WHITE_THRESHOLD:
        gray_count += 1
    else:
        gray_count = 0
    return gray_count >= 4



while robot.step(TIME_STEP) != -1:

    left_motor.setVelocity(MAX_SPEED)
    right_motor.setVelocity(MAX_SPEED)

    # if is_gray(ground_sensor.getValue()):
        # left_motor.setVelocity(0)
        # right_motor.setVelocity(0)
        # break
    print(ps[5].getValue())
    
    
    if ps[0].getValue() > FRONT_THRESHOLD or ps[7].getValue() > FRONT_THRESHOLD:
        #stop quickly
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
        robot.step(100)
    
    
        # Wall in front: turn right.
        left_motor.setVelocity(TURN_SPEED)
        right_motor.setVelocity(-TURN_SPEED)
        robot.step(725)
    #touching right wall adjust to the side
    elif ps[1].getValue() > SIDE_THRESHOLD or ps[2].getValue() > SIDE_THRESHOLD:
        left_motor.setVelocity(-TURN_SPEED)
        right_motor.setVelocity(TURN_SPEED)
    #touching left wall adjust to the left side
    elif ps[5].getValue() > SIDE_THRESHOLD or ps[6].getValue() > SIDE_THRESHOLD:
        left_motor.setVelocity(TURN_SPEED)
        right_motor.setVelocity(-TURN_SPEED)