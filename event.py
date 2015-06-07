# coding:utf-8
__author__ = 'cupen'
from pygame.constants import USEREVENT


ENEMY_REFRESH = USEREVENT + 1
MUSIC_IS_STOP = USEREVENT + 2
PLAYER_FIRE = USEREVENT + 3
TIMER = (USEREVENT + 4, USEREVENT + 100)

def isTimer(eventType):
    return TIMER[0] <= eventType <= TIMER[1]