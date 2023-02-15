
import sys
import os
import time
import asyncio


import pygame

import pygame.vidcap as camera


pygame.display.set_caption("pycon fr 2023 IoT test")
screen = pygame.display.set_mode((640, 400))


from telemetrix_aio import telemetrix_aio


DIGITAL_PIN = 2  # LED pin on esp8266


async def the_callback(data):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
    print(f'Motor {data[1]} absolute motion completed at: {date}.')


async def running_callback(data):
    if data[1]:
        print('The motor is running.')
    else:
        print('The motor IS NOT running.')

async def step_absolute(board):

    # create an accelstepper instance for a TB6600 motor driver
    #motor = await board.set_pin_mode_stepper(interface=2, pin1=8, pin2=9)

    # if you are using a 28BYJ-48 Stepper Motor with ULN2003
    # comment out the line above and uncomment out the line below.
    motor = await board.set_pin_mode_stepper(interface=4, pin1=16, pin2=5, pin3=4, pin4=0)

    await board.stepper_is_running(motor, callback=running_callback)
    await asyncio.sleep(.2)

    # set the max speed and acceleration
    await board.stepper_set_max_speed(motor, 100)
    await board.stepper_set_acceleration(motor, 400)

    # set the absolute position in steps


    # run the motor

    for way in (1,-1,1,-1,1,-1):
        print('Starting motor...')
        await board.stepper_move_to(motor, way * 50)
        await board.stepper_run(motor, completion_callback=the_callback)
        await asyncio.sleep(.2)
        await board.stepper_is_running(motor, callback=running_callback)
        await asyncio.sleep(3)
        await board.stepper_stop(motor)
        await asyncio.sleep(2)


async def blink(board, pin):

    # set the pin mode
    await board.set_pin_mode_digital_output(pin)

    # toggle the pin 4 times and exit
    for x in range(2):
        print('ON')
        await board.digital_write(pin, 0)
        await asyncio.sleep(2)
        print('OFF')
        await board.digital_write(pin, 1)
        await asyncio.sleep(2)


if 0:

    def video_capture(screen):
        skip = 0
        while not aio.exit:
            skip +=1
            if skip==2:
                surf = pygame.image.load( "/dev/video0" )
                screen.blit( surf, (320, 0) )
                pygame.display.update()
                skip=0
            yield aio

else:
    # workaround fd starve with pygame.image.load
    from PIL import Image

    def video_capture(screen):
        conv = True
        while not aio.exit:

            if conv : #not os.path.isfile("/dev/video0.bmp"):
                surf = pygame.image.load( "/dev/video0" )
                im = Image.open("/dev/video0")
                im.save("/dev/video0.bmp")
                conv = False
            else:
                surf = pygame.image.load_basic("/dev/video0.bmp")
                screen.blit( surf, (320, 0) )
                pygame.display.update()
                os.unlink("/dev/video0.bmp")
                del surf
                conv = True
            yield aio

async def main():
    global screen

    # default to localhost for telemetrix target.
    if sys.argv[-1].endswith('.py'):
        ip_addr = '127.0.0.1'
    else:
        ip_addr = sys.argv[-1]


    # default websocket mode is wss:// change it when on lan.
    if sys.platform in ('emscripten',):
        print('Using websocket')
        if ip_addr.startswith('192.168.') or ip_addr in ('localhost','127.0.0.1'):
            window.MM.set_socket("ws://")
            print(f"Board (Web)socket : {ip_addr}:31335 not using ssl")

    else:
        print(f"Board socket : {ip_addr}:31335")



    # init camera
    cam = camera.Camera( camera.list_cameras()[0], (320,200), 0 )
    await cam.start()

    # let camera start, and esp8266 time to boot
    await asyncio.sleep(2)



    # instantiate telemetrix_aio

    board = telemetrix_aio.TelemetrixAIO(ip_address=ip_addr, autostart=False)



    await board.start_aio()




    # start the video loopback thread

    import aio.gthread
    from threading import Thread
    Thread(target=video_capture, args=[screen]).start()



    await blink(board, DIGITAL_PIN)
    await step_absolute(board)

asyncio.run( main() )

