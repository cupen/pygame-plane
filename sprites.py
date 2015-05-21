from pygame.rect import Rect

__author__ = 'cupen'
import pygame

class AnimalSprite(pygame.sprite.Sprite):
    """
    :type image: pygame.surface.Surface
    """
    def __init__(self, imageFile, animConfig = ()):
        """
        :param animConfig: 动画配置。
            比如 ((4,4), (12,13,14,15)) 表示横向切割4块，纵向切割4块， 播放按块的编号进行
        """
        super(AnimalSprite, self).__init__()
        self.image = pygame.image.load(imageFile).convert_alpha()
        self.rect = self.image.get_rect()
        self.__animImages = None
        self.__animImagesIdx = 0

        if len(animConfig) > 0:
            _wCount = animConfig[0][0]
            _hCount = animConfig[0][1]
            _w = self.rect.width  / _wCount
            _h = self.rect.height / _hCount
            _list = []
            for i in animConfig[1]:
                _tmpRect = Rect(int(i % _wCount) * _w, int((i / _hCount)) * _h, _w, _h)
                print(i, _tmpRect)
                _list.append(self.image.subsurface(_tmpRect))
            self.__animImages = tuple(_list)
            self.image = self.__animImages[0]
            self.rect = self.image.get_rect()
            pass

    def update(self):
        self.__animImagesIdx += 1
        self.__animImagesIdx %= len(self.__animImages)
        self.image = self.__animImages[self.__animImagesIdx]
    pass

class Plane(AnimalSprite):

    def __init__(self, imageFile,position = (0,0), animConfig = ()):
        super(Plane, self).__init__(imageFile, animConfig)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.speed = 2
        self.status = {"up":False, "down": False, "left":False, "right": False}
        pass

    def handleEvent(self, e):
        if e.key == pygame.K_w:
            self.status['up']   = (e.type == pygame.KEYDOWN)
        elif e.key == pygame.K_s:
            self.status['down'] = (e.type == pygame.KEYDOWN)
        elif e.key == pygame.K_a:
            self.status['left'] = (e.type == pygame.KEYDOWN)
        elif e.key == pygame.K_d:
            self.status['right'] = (e.type == pygame.KEYDOWN)
        pass

    def update(self):
        super(Plane, self).update()
        # print(self.status)
        for key, value in self.status.items():
            if not value:
                continue

            if key == 'up':
                self.move_up()
            elif key == 'down':
                self.move_down()
            elif key == 'left':
                self.move_left()
            elif key == 'right':
                self.move_right()
        pass

    def move_up(self):
        self.rect.y -= self.speed
        pass

    def move_down(self):
        self.rect.y += self.speed
        pass

    def move_left(self):
        self.rect.x -= self.speed
        pass

    def move_right(self):
        self.rect.x += self.speed
        pass

class Player(Plane):
    pass

class Enemy(Plane):
    """
    AI
    """
    pass