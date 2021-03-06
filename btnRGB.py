#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
import random

GPIO.setmode(GPIO.BCM)

BLUE = 25
GREEN = 24
RED = 23
BTN1 = 4
BTN2 = 22
BTN3 = 17

GPIO.setup(BLUE, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BTN1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

POWER = False
EXIT = False

def checkBTN1(BTN1):
#    print("Fez clic clac (Oia aqui: {}) no pininho: {}".format(GPIO.input(BTN1), event))
    global POWER
    if POWER:
        print("DESLIGUEI... Ahhh =(")
        POWER = False
    else:
        print("LIGUEI!!! Uhhuul \o/")
        POWER = True

def checkBTN3(BTN3):
    global POWER
    global EXIT
    POWER = False
    EXIT = True

def pisca():
    while True:
        if EXIT: break
        for led in [ BLUE, GREEN, RED ]:
            if POWER:
                GPIO.output(led, True)
                sleep(random.uniform(0.01, 1))
                GPIO.output(led, False)
            else:
                break

def sair(status):
    print("TCHAU... DE NOVOOOOO")
    GPIO.cleanup()
    exit(status)

GPIO.add_event_detect(BTN1, GPIO.BOTH)
GPIO.add_event_callback(BTN1, callback=checkBTN1)

GPIO.add_event_detect(BTN3, GPIO.BOTH)
GPIO.add_event_callback(BTN3, callback=checkBTN3)

try:
    pisca()
except KeyboardInterrupt:
    sair(0)
sair(0)
