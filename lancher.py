from pygame.constants import USEREVENT

__author__ = 'cupen'
import pygame
from sprites import Plane
from engine import GameEngine

game = GameEngine()
game.set_background(['bg_01.jpg', 'bg_02.jpg'], width=640, height=480)
game.play_music('assets/Devil May Cry - Vergil Battle 2.mp3')

playerImage = game.srcLoader.getSurface("player.png")
player = Plane(playerImage, animConfig=((4,4), (12,13,14,15)))
game.add_player(player)
game.set_enemy_count_per_seconds(3)
game.listen_keyboard( pygame.K_w, lambda e:player.handleEvent(e) )
game.listen_keyboard( pygame.K_s, lambda e:player.handleEvent(e) )
game.listen_keyboard( pygame.K_a, lambda e:player.handleEvent(e) )
game.listen_keyboard( pygame.K_d, lambda e:player.handleEvent(e) )
game.listen_keyboard( pygame.K_j, lambda e:game.handle_event(e) )
game.listen_keyboard( pygame.K_j, lambda e:game.handle_event(e) )
game.listen_keyboard( pygame.K_j, lambda e:game.handle_event(e) )



game.run(fps = 70)
game.close()