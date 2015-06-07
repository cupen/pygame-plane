__author__ = 'cupen'

import pygame

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
        # pygame.image.save(bigImage, ".png")
    return bigImage