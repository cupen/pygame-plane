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
