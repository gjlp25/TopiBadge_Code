import urequests
from time import sleep
import ujson
from machine import Pin, I2C, Timer, deepsleep
from ssd1306 import SSD1306_I2C
from wifi_manager import WifiManager
import framebuf
import machine, neopixel

i2c = I2C(sda=Pin(4), scl=Pin(5))
btn = Pin(2, Pin.IN, Pin.PULL_UP)
logo = bytearray(b'\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04?\xc4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c?\x82\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x7f\xa8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000v\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00p\x7f\xc0\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x1d?\x80\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x07\x80\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xe0\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x07x\x00\x1f\xe0\xfc\x04\xfc\x0c\x07\xc1\x80`\xfc\x00\x07\x0fp\x00\x0fA\xef\x07\xfe\x0c\x1f\xf0\x80C\xde\x00\x0f?0@\x02\x03\x03\x07\x03\x0c81\x80\xe3\x00\x008\x9f\xb2\x80\x06\x07\x01\x86\x03\x0c0\x00\xc0C\x00\x00\x18\xcf\x9b\xc0\x02\x06\x01\x8e\x01\x8c`\x01\x80c\x00\x00\x00\xf3\x1f\x80\x07\x06\x01\x84\x01\x8c0\x00\x80\xc3\xe0\x00\x00\xf8\x0f\x00\x02\x06\x00\x86\x01\x8c`\x01\x80`\xfc\x02\x80\xfc\x02\x00\x06\x06\x01\x8c\x01\x8c0\x00\xc0\xc0\x0e\r`|\x00\x00\x02\x03\x01\x86\x03\x0c0\x01\x80\xe0\x060\x13N\x00\x00\x07\x03\x03\x07\x07\x0c80\xc1\xc0\x06a#F\x00\x00\x03\xa1\xdf\x0f\xde\x0c\x1dp\xf7c\x9eA\xcf\x02\x00\x00\x01\xf0\xfc\x04\xf8\x0c\x07\xc0>C\xf8\xc0\x1f\x07\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\xf0><\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\xff\xf88\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x7f\xe08\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x04\x00\x08\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
fb = framebuf.FrameBuffer(logo, 128, 28, framebuf.MONO_HLSB)
display_width = 128
display_height = 32
display = SSD1306_I2C(display_width, display_height, i2c)
np = neopixel.NeoPixel(machine.Pin(14), 1)
chase = Pin(12, Pin.OUT)
timer = Timer(0)

orange = (63, 13, 0)
green = (0, 63, 0)
red = (63, 0, 0)
reset = (0, 0, 0)

def debounce(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=handle_interrupt)

def handle_interrupt(pin):
    result_json = httpreq()
    print_to_screen(result_json)
    parse_data(result_json)
    new_price_value()
    print(prev_price + ' prevTS') #troubleshoot
    print(new_price + ' newTS') #troubleshoot
    led_chase()
    deep_sleep()
   
def bootup():
    display.fill(0)
    display.blit(fb, 0, 0)
    display.show()
    
def reset_np():
    np[0] = reset
    np.write()
    
def httpreq():
        url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=TOI.V&apikey=NYCM7O9QFZZ60VAK"
        payload={}
        headers = {}
        response = urequests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        return ujson.loads(response.text)

def parse_data(input_json):
    print(input_json['Global Quote']["01. symbol"])
    print("Price: " + (input_json['Global Quote']["05. price"]))
    print("Change %: " +(input_json['Global Quote']["10. change percent"]))
    global new_price, prev_price
    prev_price = input_json['Global Quote']["08. previous close"]
    new_price = input_json['Global Quote']["05. price"]
   
def new_price_value():
    if new_price < prev_price:
        print("lagâh")
        np[0] = red
        np.write()
    elif new_price == prev_price:
        print("gelêk")
        np[0] = orange
        np.write()
    else:
        print("hogâh")
        np[0] = green
        np.write()

def print_to_screen(input_json):
    display.rotate(True)
    display.fill(0)
    display.text((input_json['Global Quote']["01. symbol"]), 0, 0, 1)
    display.text(("Price: " + (input_json['Global Quote']["05. price"])), 0, 12, 1)
    display.text(("Change: " +(input_json['Global Quote']["10. change percent"])), 0, 24, 1)
    display.show()
    
def print_nw_info():
    display.rotate(True)
    display.fill(0)
    wlan_info = (wm.wlan_sta.ifconfig())
    ip_info = wlan_info[0]
    display.fill(0)
    display.text(("IP address: "), 0, 0, 1)
    display.text((ip_info), 0, 12, 1)
    display.show()
    print("IP address: " + (ip_info)) #TS
    
def led_chase():
    chase.value(1)
    sleep(10)
    chase.value(0)
    
def deep_sleep():
    sleep(10)
    np[0] = reset
    np.write()
    display.poweroff()
    print("Entering Deep Sleep. Press Reset to wake")
    deepsleep()
    
btn.irq(debounce, Pin.IRQ_RISING)
    
wm = WifiManager()
reset_np()
bootup()
wm.connect()
while True:
    if wm.is_connected():
        sleep(3)
        print_nw_info()
        sleep(3)
        display.rotate(True)
        display.fill(0)
        display.text('Connected!', 0, 0, 1)
        display.show()
        print('Connected!')
        sleep(3)
        bootup()
        break
    else:
        print('Disconnected!')
        display.rotate(True)
        display.fill(0)
        display.text('Disonnected!', 0, 16, 1)
        display.show()
    time.sleep(10)