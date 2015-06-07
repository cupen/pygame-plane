# coding:utf-8

__author__ = 'cupen'
from resource import Assets
import pygame
from sprites import Plane
from engine import GameEngine

game = GameEngine()
game.set_background(['bg_01.jpg', 'bg_02.jpg'], width=640, height=480)
game.play_music('assets/Devil May Cry - Vergil Battle 2.mp3')

playerImage = Assets.loadImage("player.png")

player = Plane(playerImage, animConfig=((4,4), (12,13,14,15)))
game.add_player(player)
game.setEnemyCountPerSeconds(3)
game.setPlayerBulletCountPerSeconds(10)
game.listen_keyboard( pygame.K_w, lambda e:player.handleEvent(e) )
game.listen_keyboard( pygame.K_s, lambda e:player.handleEvent(e) )
game.listen_keyboard( pygame.K_a, lambda e:player.handleEvent(e) )
game.listen_keyboard( pygame.K_d, lambda e:player.handleEvent(e) )
# game.listen_keyboard( pygame.K_j, lambda e:game.handle_event(e) )

game.run(fps = 100)
game.close()