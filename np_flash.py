import machine, neopixel
import time


np = neopixel.NeoPixel(machine.Pin(14), 1)
color = [0, 0, 0]
increment = 1

#orange = (255, 165, 0)
#green = (0, 255, 0)
#red = (255, 0, 0)

def flash_green():
    global np, color, increment
    while True:
        color[1] += increment

        if color[1] >=255:
            color[1] = 255
            increment = -1

        if color[1] <= 0:
            color[1] = 0
            increment = 1

        np.fill(color)
        np.write()
        
        
def flash_red():
    global np, color, increment
    while True:
        color[0] += increment

        if color[0] >=255:
            color[0] = 255
            increment = -1

        if color[0] <= 0:
            color[0] = 0
            increment = 1

        np.fill(color)
        np.write()
        
def flash_orange():
    global np, color, increment
    while True:
        color[0] += increment
        color[1] += increment

        if color[0] >=255:
            color[0] = 255
            color[1] = 255
            increment = -1

        if color[0] <= 0:
            color[0] = 0
            color[1] = 0
            increment = 1

        np.fill(color)
        np.write()
        

        
flash_green()


