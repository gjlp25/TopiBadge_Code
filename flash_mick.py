import machine, neopixel
import time


np = neopixel.NeoPixel(machine.Pin(14), 1)
color = [0, 0, 0]
increment = 1

#orange = (255, 165, 0)
#green = (0, 255, 0)
#red = (255, 0, 0)

def flash_led(color, wanted_flashes):
    current_flashes = 0
    colors = {
        "red" = [255, 0, 0]
        "green" = [0, 255, 0]
    }

    color_array = colors[color]

    if current_flashes < wanted_flashes:
        match color:
            case "red":
                if color_array[0] ==255:
                    color_array[0] = 0
                if color_array[0] == 0:
                    color_array[0] = 255
                np.fill(color_array)
                np.write()
                current_flashes += 1
            case "green":
                if color_array[1] == 255:
                    color_array[1] = 0
                if color_array[1] == 0:
                    color_array[1] = 255
                np.fill(color_array)
                np.write()
                current_flashes +=1
            case _:
                print("unsupported color HELP")
    else print("Fix you flash logic")