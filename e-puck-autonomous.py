from controller import Robot
import random

TIME_STEP = 30


robot = Robot()


# Enable all 8 proximity sensors.
ps = []
for i in range(8):
    sensor = robot.getDevice("ps" + str(i))
    sensor.enable(TIME_STEP)
    ps.append(sensor)

# Get and enable the three ground sensors.
ground_sensors = []
for i in range(3):
    sensor = robot.getDevice("gs" + str(i))
    sensor.enable(TIME_STEP)
    ground_sensors.append(sensor)


#motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")


left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))


left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

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
    
    
    

MAX_SPEED = 6.28
TURN_SPEED = 3.0

FRONT_THRESHOLD = 90 

LEFT_THRESHOLD = 70 
RIGHT_THRESHOLD = 70 

while robot.step(TIME_STEP) != -1:

    left_value = ground_sensors[0].getValue()
    center_value = ground_sensors[1].getValue()
    right_value = ground_sensors[2].getValue()
    
    
    if is_gray(center_value):
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
        break
        

    left_speed = 0
    right_speed = 0
    
    front_value = max(ps[0].getValue(), ps[7].getValue())
    left_value = max(ps[5].getValue(), ps[6].getValue())
    right_value = max(ps[1].getValue(), ps[2].getValue())
    # print(ps[0].getValue(), ps[7].getValue(), ps[5].getValue(), ps[6].getValue())
    
    front_wall = front_value > FRONT_THRESHOLD
    left_wall = left_value > LEFT_THRESHOLD
    right_wall = right_value > RIGHT_THRESHOLD
    
    randChange = random.random()
    chance_For_Right = 0
    chance_For_Left = 0.5
    

    
    if front_wall or (randChange < chance_For_Right and not right_wall):
        # Wall in front: turn right.
        left_speed = TURN_SPEED
        right_speed = -TURN_SPEED
    elif not left_wall and randChange < chance_For_Left:
        # No wall on the left: turn left to find the wall.
        left_speed = -TURN_SPEED
        right_speed = TURN_SPEED
    else:
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED


    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
    
    