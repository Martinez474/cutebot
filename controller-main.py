from microbit import *
import radio

radio.on()
radio.config(group=7)

while True:
    if button_a.is_pressed() and button_b.is_pressed():
        radio.send("forward")
        display.show(Image.ARROW_N)

    elif button_a.is_pressed():
        radio.send("left")
        display.show(Image.ARROW_W)

    elif button_b.is_pressed():
        radio.send("right")
        display.show(Image.ARROW_E)

    else:
        radio.send("stop")
        display.show(Image.SQUARE_SMALL)

    sleep(100)