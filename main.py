from microbit import *
import utime

# Pin Definitions
servo_pin = pin0
sensor_pin = pin1
led_pin = pin2

# Constants
roundmax = 30

# Variables
val = 0
pos = 0
qround = 0

def setup():
    led_pin.write_digital(0)  # LED off
    uart.init(baudrate=9600, tx=pin0, rx=pin1)  # Initialize UART communication

def loop():
    global val, pos, qround
    
    val = sensor_pin.read_digital()
    
    if val == 1:  # Check if the input is HIGH
        led_pin.write_digital(0)  # LED is off
        detach_servo()
    else:
        led_pin.write_digital(1)  # LED is turned on
        attach_servo()
        for pos in range(0, 91, 1):
            servo_write(pos)
            utime.sleep_ms(2)
        for pos in range(90, -1, -1):
            servo_write(pos)
            utime.sleep_ms(2)
        detach_servo()
    
    if qround == roundmax:
        qround = 0
    if qround == 0:
        locate = get_location()
        if locate == "NULL":
            locate = locate + "|" + str(utime.ticks_us())
            print(locate)
        else:
            print(locate)
        
        # Send location to ESP8266 via UART
        uart.write(locate + "\n")

    qround += 1
    utime.sleep_ms(50)

def attach_servo():
    servo_pin.set_analog_period(20)

def detach_servo():
    servo_pin.write_digital(0)

def servo_write(angle):
    pulse_width = int((angle * 9.444) + 600)
    servo_pin.write_analog(pulse_width)

def get_location():
    # Implement the GPS code here using the appropriate GPS library for micro:bit
    # For demonstration, let's return a dummy value
    return "51.508131|-0.128002"  # Example: London coordinates

setup()

while True:
    loop()
