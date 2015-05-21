__author__ = 'cupen'

import pygame


class Control:

    STATUS_RUNNING = 0
    STATUS_STOP    = 1
    STATUS_PAUSE   = 2

    def __init__(self):
        self.__listener = {}
        self.__status = Control.STATUS_RUNNING
        pass

    def is_stop(self):
        return self.__status == Control.STATUS_STOP

    def is_pause(self):
        return self.__status == Control.STATUS_PAUSE

    def listen_keyboard(self, keyCode, callback):
        if keyCode in self.__listener:
            print("Dumplicate key:", keyCode)
            return
        self.__listener[keyCode] = callback
        pass

    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.__status = Control.STATUS_STOP
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                self.call_listener(e)
        pass

    def call_listener(self, event):
        # print(event)
        if event.key not in self.__listener:
            return

        callback = self.__listener[event.key]
        callback(event)
        return