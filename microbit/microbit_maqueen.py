from microbit import *
from micropython import const
import music

I2C_ADDR = const(16)
SPEED = const(50)
SERVO_STEP_DELAY = 10
MOVEMENT_DURATION = 2000

# Initialize UART and I2C
uart.init(115200)
i2c.init()

# Movement functions
def drive():
    i2c.write(I2C_ADDR, bytes((0, 0, SPEED)))
    i2c.write(I2C_ADDR, bytes((2, 0, SPEED * 1,8)))

def turn_right():
    i2c.write(I2C_ADDR, bytes((0, 0, SPEED * 2)))
    i2c.write(I2C_ADDR, bytes((2, 1, SPEED * 2)))

def turn_left():
    i2c.write(I2C_ADDR, bytes((0, 1, SPEED * 2)))
    i2c.write(I2C_ADDR, bytes((2, 0, SPEED * 2)))

def stop():
    i2c.write(I2C_ADDR, bytes((0, 0, 0)))
    i2c.write(I2C_ADDR, bytes((2, 0, 0)))

def reverse():
    i2c.write(I2C_ADDR, bytes((0, 1, SPEED)))
    i2c.write(I2C_ADDR, bytes((2, 1, SPEED)))
    for _ in range(int(MOVEMENT_DURATION / 500)):
        music.play('C4:1')
        sleep(500)

def set_servo_angle(pin, angle):
    duty = angle
    pin.write_analog(duty)

def smooth_servo_move(pin, start_angle, end_angle, step_delay):
    step = 1 if start_angle < end_angle else -1
    for angle in range(start_angle, end_angle + step, step):
        set_servo_angle(pin, angle)
        sleep(step_delay)

def raise_loader():
    smooth_servo_move(pin1, 90, 50, SERVO_STEP_DELAY)

def lower_loader():
    smooth_servo_move(pin1, 50, 90, SERVO_STEP_DELAY)

def catapult():
    smooth_servo_move(pin1, 90, 50, 0)

# Movement command mapping
MOVEMENTS = {
    'drive': (drive, Image.ARROW_N),
    'reverse': (reverse, Image.ARROW_S),
    'right': (turn_right, Image.ARROW_E),
    'left': (turn_left, Image.ARROW_W),
    'stop': (stop, Image.SQUARE),
    'loader_up': (raise_loader, Image.TARGET),
    'loader_down': (lower_loader, Image.TARGET)
}

def movement(msg_str):
    for command, (action, image) in MOVEMENTS.items():
        if command in msg_str:
            display.show(image)
            action()
            sleep(MOVEMENT_DURATION)
            stop()
            display.show(Image.SQUARE)
            break

while True:
    if uart.any():
        msg_bytes = uart.read()
        msg_str = str(msg_bytes)
        movement(msg_str)