#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Fernando Manfredi <manfredi@gmail.com>
# Contributor, Programmer Expert: Lara Maia <lara@craft.net.br>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    <http://www.gnu.org/licenses/>.
#
# Versão 0.1
#

import RPi.GPIO as GPIO
from time import sleep
import random
from threading import Thread

#Modo da GPIO seguindo a numeração BCM, ao inves da pinagem.
GPIO.setmode(GPIO.BCM)

class Blink(Thread):
    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent

    def run(self):
        while self.parent.running:
            for led in [ self.parent.ledBlue, self.parent.ledGreen, self.parent.ledRed ]:
                if self.parent.start:
                    GPIO.output(led, True)
                    sleep(random.uniform(0.5, 0.1))
                    GPIO.output(led, False)
                else:
                    if not self.parent.running:
                        break
        GPIO.cleanup()

class Game:
    def __init__(self):
        # LEDs/Botões
        self.ledBlue = 25
        self.ledGreen = 24
        self.ledRed = 23

        self.btnGreen = 4
        self.btnYellow = 22
        self.btnRed = 17

        self.start = False
        self.exit = False
        self.points = 0

        self.player = None

        # Setup inicial das funções de cada pino e estado inicial.
        GPIO.setup(self.ledBlue, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ledGreen, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ledRed, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.btnRed, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.btnYellow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.btnGreen, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.btnRed, GPIO.FALLING, callback=self._exit, bouncetime=300)
        GPIO.add_event_detect(self.btnYellow, GPIO.FALLING, callback=self.press_btnYellow, bouncetime=300)
        GPIO.add_event_detect(self.btnGreen, GPIO.FALLING, callback=self.press_btnGreen, bouncetime=1000)

        self.thBlink = Blink(self)

    def main(self):
        # Quem vai jogar?

        self.player = input('Diga seu nome: ')
        if not self.player:
            print('Ok Manézão sem nome, vamos lá')
            self.player = 'Mané'

        self.running = True
        self.thBlink.start()

        print('Para iniciar o jogo, aperte o botão verde e SE PREPARE!')


    def _exit(self, obj=None):
        self.running = False
        self.start = False
        print("TCHAU... :(")
        self.thBlink.join()
        exit(0)

    '''Botão amarelo eh a interface principal do 'jogo', quando
    pressionado compara com o led ligado no momento, se o led
    verde estiver ligado, conita um ponto'''
    def press_btnYellow(self, obj):
        if GPIO.input(self.ledGreen):
            self.points +=1

            if self.points == 1:
                print('Conseguiu 1 pelo menos... Total: {} pontinho'.format(self.points))
            else:
                print('Conseguiu +1, Legal! Total: {} pontos'.format(self.points))
        else:
            print('Errou bobão :P')

    '''Botão verde inicia ou para o jogo alterando a variavel
    global POWER que e lida na função pisca()'''
    def press_btnGreen(self, obj):
        if not self.start:
            print("ATENCÃO! ATENCÃO! ATENCÃO! COMEÇOU!!!")
            print("Quando o led VERDE acender, aperte o botão AMARELO")
            self.start = True # Deve iniciar a thread pisca()
        else: # if self.start = True
            self.start = False # Encerra o jogo
            print("Sistemas desligados...")
            if self.points == 0:
                print("{}, você tentou jogar pelo menos?".format(self.player))
            if self.points >= 1 and self.points <= 10:
                print("{}, poxa, tenta um pouco mais, ne?".format(self.player))
            if self.points >= 11 and self.points <= 20:
                print("Legal {}, ta pegando o jeito.".format(self.player))
            if self.points >= 21:
                print("Uau {}, ta viciado!".format(self.player))

            print("Pontuação final: {}".format(self.points))


if __name__ == '__main__':
    game = Game()
    game.main()
