__author__ = 'cupen'
import sys
import pygame
from pygame.rect import Rect
pygame.init()
screen = pygame.display.set_mode((640, 480))

from sprites import Plane
from resource import TextureConfig
from control import Control

tConfig = TextureConfig("assets/plane.xml")


planeImage = pygame.image.load("assets/plane.png").convert_alpha()
imageDict = {}
for i in ('hero_1','hero_2'):
    subimageData = tConfig.getSubTexture('plane.png', i)
    if not subimageData:
        print("Unexist sub-image:plane.png,",i)
        sys.exit()

    tmpRect = Rect(subimageData['x'], subimageData['y'], subimageData['width'], subimageData['height'])
    imageDict[i] = planeImage.subsurface(tmpRect).convert_alpha()
    pass

for i in ('bg_01.jpg','bg_02.jpg'):
    imageDict[i] = pygame.image.load("assets/"+i).convert()
    pass


background = imageDict['bg_01.jpg']
screen.blit(background, (0, 0))

game = Control()
player = Plane('images/player.png', animConfig=((4,4), (12,13,14,15)))
sprites = pygame.sprite.Group()
sprites.add(player)

game.listen_keyboard( pygame.K_w, lambda e:player.handleEvent(e))
game.listen_keyboard( pygame.K_s, lambda e:player.handleEvent(e))
game.listen_keyboard( pygame.K_a, lambda e:player.handleEvent(e))
game.listen_keyboard( pygame.K_d, lambda e:player.handleEvent(e))

fps = 70
delayMiliSeconds = int(1000 / fps)

player.rect.x = int((screen.get_width() + player.rect.width) / 2)
player.rect.y = screen.get_height() - player.rect.height

while not game.is_stop():
    pygame.display.update()
    pygame.time.delay(delayMiliSeconds)

    game.update()
    sprites.update()
    sprites.clear(screen, background)
    sprites.draw(screen)
    pass

pygame.quit()

