# coding:utf-8
__author__ = 'cupen'
import pygame
from pygame.rect import Rect

class AnimalSprite(pygame.sprite.Sprite):
    """
    :type image: pygame.surface.Surface
    """
    def __init__(self, image, animConfig = ()):
        """
        :param animConfig: 动画配置。
            比如 ((4,4), (12,13,14,15)) 表示横向切割4块，纵向切割4块， 播放按块的编号进行
        """
        super(AnimalSprite, self).__init__()
        self.image = image
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

class Plane(AnimalSprite):
    def __init__(self, image,position = (0,0), animConfig = ()):
        super(Plane, self).__init__(image, animConfig)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.speed = 4
        self.status = {"up":False, "down": False, "left":False, "right": False}
        pass

    def create_bullet(self, image, area):
        bullet = Bullet(image, area)
        bullet.rect.x = self.rect.x + ((self.rect.width - bullet.rect.width) / 2)
        bullet.rect.y = self.rect.y
        bullet.speedX = 0
        bullet.speedY = -(self.speed * 2)
        return bullet

    def handleEvent(self, e):
        if e.key == pygame.K_w:
            self.status['up']   = (e.type == pygame.KEYDOWN)
        elif e.key == pygame.K_s:
            self.status['down'] = (e.type == pygame.KEYDOWN)
        elif e.key == pygame.K_a:
            self.status['left'] = (e.type == pygame.KEYDOWN)
        elif e.key == pygame.K_d:
            self.status['right'] = (e.type == pygame.KEYDOWN)
        elif e.key == pygame.K_j:
            pass
        pass

    def add_bullet(self, bulletSprite):
        for group in self.groups():
            group.add(bulletSprite)
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
    def __init__(self, image, position = (0,0), speed = 5):
        super(Enemy, self).__init__(image, position)
        self.speed = speed
        pass

    def update(self):
        self.rect.y += self.speed
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, area):
        super(Bullet, self).__init__()
        self.image = image
        self.rect = image.get_rect()
        self.speedX = 0
        self.speedY = 0
        self.areaRect = area
        pass

    def update(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        # 子弹出界(bullet is out of area)
        if not self.areaRect.contains(self.rect):
            self.kill()
        pass

class Background(pygame.sprite.Sprite):
    def __init__(self, images, width, height, speed = 2):
        super(Background, self).__init__()
        self.image = merge_image(*images)
        self.image = merge_image(self.image, images[0])
        multiple = width / self.image.get_width()
        newWidth = width
        newHeight = int(self.image.get_height() * multiple)
        self.image = self.image = pygame.transform.scale(self.image, (newWidth, newHeight))
        self.rect = self.image.get_rect()

        self.screenWidth = width
        self.screenHeight = height
        self.speed = speed
        self.resetImagePostion()
        pass

    def resetImagePostion(self):
        self.rect.y = (self.screenHeight - self.rect.height)
        pass

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 0:
            print(self.rect)
            self.resetImagePostion()
            print(self.rect)

        # if self.rect.y > 0:
        #     self.image = self.__images[0]
        #     self.__images[0] = self.__images[1]
        #     self.__images[1] = self.image
        #     self.resetCurImage()
        pass

def merge_image(*images):
    w = 0
    h = 0
    for image in images:
        w = image.get_width()
        h += image.get_height()

    bigImage = pygame.Surface((w, h))
    _y = 0
    for image in images:
        _rect = image.get_rect()
        _rect.x = 0
        _rect.y = _y
        _y += image.get_height()
        print(_rect)
        bigImage.blit(image, _rect)
        # pygame.image.save(bigImage, "wokao.png")
    return bigImage