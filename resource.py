# coding:utf-8
import os
import pygame
import sys
from pygame.rect import Rect

__author__ = 'cupen'
from xml.dom import minidom

class TextureConfig:
    def __init__(self, configFile):
        self.xmldoc = minidom.parse(configFile)
        self.imageDict = {}
        for i in self.xmldoc.getElementsByTagName("TextureAtlas"):
            imageName = i.getAttribute('imagePath')
            if imageName not in self.imageDict:
                self.imageDict[imageName] = {}

            for subtt in i.getElementsByTagName("SubTexture"):
                _subttData = {}
                for _tmp in ('name','x','y','width','height'):
                    _subttData[_tmp] = subtt.getAttribute(_tmp)
                    if _subttData[_tmp].isalnum():
                        _subttData[_tmp] = int(_subttData[_tmp])

                subImageName = _subttData['name']
                self.imageDict[imageName][subImageName] = _subttData
        pass

    def getSubTexture(self, imageName, subImageName):
        if imageName not in self.imageDict:
            return None

        return self.imageDict[imageName].get(subImageName, None)

imageDict = {}
tConfig = None

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)

def load():
    global imageDict, tConfig
    tConfig = TextureConfig(find_data_file("assets/plane.xml"))
    planeImage = pygame.image.load(find_data_file("assets/plane.png")).convert_alpha()
    # TODO：待重构，改为懒加载（change to lazy load）
    for i in ('hero_1','hero_2', 'bullet_0', 'bullet_0', 'enemy_b', 'enemy_m', 'enemy_s', 'explosion_01', 'explosion_02', 'explosion_03'):
        subimageData = tConfig.getSubTexture('plane.png', i)
        if not subimageData:
            print("Unexist sub-image:plane.png,",i)
            sys.exit()

        tmpRect = Rect(subimageData['x'], subimageData['y'], subimageData['width'], subimageData['height'])
        imageDict[i] = planeImage.subsurface(tmpRect).convert_alpha()
    pass

def getSurface(imageName):
    global imageDict
    if imageName not in imageDict:
        imageDict[imageName] = pygame.image.load(find_data_file("assets/"+ imageName)).convert_alpha()
    return imageDict[imageName]

def getSound():
    pass




