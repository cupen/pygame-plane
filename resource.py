# coding:utf-8
import os
import pygame
import sys
from pygame.rect import Rect
from xml.dom import minidom

__author__ = 'cupen'

ROOT_PATH = None
if getattr(sys, 'frozen', False):
    ROOT_PATH = os.path.dirname(sys.executable)
else:
    ROOT_PATH = os.path.dirname(__file__)

ASSETS_DIR = os.path.join(ROOT_PATH, 'assets')

class TextureConfig:

    def loadConfig(self, configFile):
        self.xmldoc = minidom.parse(os.path.join(ASSETS_DIR, configFile))
        self.imageDict = {}
        for ttAtlas in self.xmldoc.getElementsByTagName("TextureAtlas"):
            imageName = ttAtlas.getAttribute('imagePath')
            if imageName in self.imageDict:
                raise ValueError("Duplicate image name:%s"%imageName)

            self.imageDict[imageName] = {}
            for subtt in ttAtlas.getElementsByTagName("SubTexture"):
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

class Assets:
    __tconfig = TextureConfig()
    __imageDict = {}

    @classmethod
    def init(cls):
        cls.__tconfig.loadConfig("plane.xml")
        pass

    @classmethod
    def loadImage(cls, name):
        if name in cls.__imageDict:
            return cls.__imageDict[name]

        pathList = name.split("#")
        if len(pathList) == 1:
            cls.__imageDict[name] = pygame.image.load(os.path.join(ASSETS_DIR,name)).convert_alpha()
        elif len(pathList) == 2:
            parrentImage = cls.loadImage(pathList[0])
            subttData = cls.__tconfig.getSubTexture(pathList[0], pathList[1])
            tmpRect = Rect(subttData['x'], subttData['y'], subttData['width'], subttData['height'])
            cls.__imageDict[name] = parrentImage.subsurface(tmpRect).convert_alpha()
        else:
            raise ValueError("Invalid image name:%s"%name)

        return cls.__imageDict[name]

    @classmethod
    def loadMP3(cls, name):
        pass

Assets.init()