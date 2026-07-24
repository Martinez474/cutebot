from controller import Robot, Keyboard


TIME_STEP = 30


robot = Robot()


keyboard = Keyboard()
keyboard.enable(TIME_STEP)


sensor0 = robot.getDevice("ps0")
sensor7 = robot.getDevice("ps7")

sensor0.enable(TIME_STEP)
sensor7.enable(TIME_STEP)

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")


left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))


left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)


MAX_SPEED = 6.28
TURN_SPEED = 3.0
THRESHOLD = 200


while robot.step(TIME_STEP) != -1:
    key = keyboard.getKey()

    left_speed = 0.0
    right_speed = 0.0

    is_Past_Threshold = (
        sensor0.getValue() < THRESHOLD and sensor7.getValue() < THRESHOLD
    )

    if key == Keyboard.UP and is_Past_Threshold:
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED

    elif key == Keyboard.DOWN:
        left_speed = -MAX_SPEED
        right_speed = -MAX_SPEED

    elif key == Keyboard.LEFT:
        left_speed = -TURN_SPEED
        right_speed = TURN_SPEED

    elif key == Keyboard.RIGHT:
        left_speed = TURN_SPEED
        right_speed = -TURN_SPEED

    elif key == ord(" "):
        left_speed = 0.0
        right_speed = 0.0

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
