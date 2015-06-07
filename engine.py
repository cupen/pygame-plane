# coding:utf-8
import event
import random
import pygame
from resource import Assets
from sprites import Background, Bullet, Enemy


__author__ = 'cupen'

class GameEngine:
    STATUS_RUNNING = 0
    STATUS_STOP    = 1
    STATUS_PAUSE   = 2

    def __init__(self):
        pygame.init()
        self.__listener = {}
        self.__userEventDict = {}
        self.__userEventCode = 0
        self.__status = GameEngine.STATUS_RUNNING
        self.planeGroup = pygame.sprite.Group()
        self.bulletGroup = pygame.sprite.Group()
        self.background = None
        self.screen = None
        self.player = None
        self.__spriteGroups = (self.planeGroup, self.bulletGroup)
        pass

    def addTimer(self, delay, callback):
        if self.__userEventCode == 0:
            self.__userEventCode = event.TIMER[0]
        else:
            self.__userEventCode += 1

        if self.__userEventCode > event.TIMER[1]:
                raise Exception("Invalide anonymity userevent:%s"%self.__userEventCode)

        self.__userEventDict[self.__userEventCode] = callback
        pygame.time.set_timer(self.__userEventCode, delay)
        pass

    def setEnemyCountPerSeconds(self, count):
        self.addTimer(
            int(1000 / count),
            lambda :self.refresh_enemy()
        )
        pass

    def setPlayerBulletCountPerSeconds(self, count = 1):
        self.addTimer(
            int(1000 / count),
            lambda :self.bulletGroup.add(
                self.player.create_bullet(
                    Assets.loadImage("plane.png#bullet_0"),
                    self.screen.get_rect()
                )
            )
        )
        pass

    def add_player(self, plane):
        self.player = plane
        plane.rect.center = self.screen.get_rect().center
        plane.rect.y = self.screen.get_height() - plane.rect.height
        self.add_plane(plane)
        pass

    def add_enemy(self, plane):
        self.add_plane(plane)
        pass

    def handle_event(self, e):
        if e.key == pygame.K_j:
            image = Assets.loadImage("plane.png#bullet_0")
            bullet = self.player.create_bullet(image, self.screen.get_rect())
            self.bulletGroup.add(bullet)
        pass

    def set_background(self, imageNameList, width, height):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_icon(Assets.loadImage("icon48x48.png"))
        _list = []
        for tmp in imageNameList:
            image = Assets.loadImage(tmp)
            _list.append(image)
        self.background = Background(_list, width=width, height=height)
        self.screen.blit(self.background.image, (self.background.rect.x, self.background.rect.y) )
        pass

    def create_sprite(self, imageName, spriteClass = pygame.sprite.Sprite):
        surface = Assets.loadImage(imageName)
        return spriteClass(surface)

    def add_plane(self, sprite):
        self.planeGroup.add(sprite)
        pass

    def play_music(self, musicFile):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play()

        # TODO: holy shit! 播完不知道怎么重放，endevent看起来木起作用
        for i in range(30):
            pygame.mixer.music.queue(musicFile)

        pygame.mixer.music.set_endevent(event.MUSIC_IS_STOP)
        pass

    def is_stop(self):
        return self.__status == GameEngine.STATUS_STOP

    def is_pause(self):
        return self.__status == GameEngine.STATUS_PAUSE

    def refresh_enemy(self):
        enemyList = (
            Assets.loadImage("plane.png#enemy_b"),
            Assets.loadImage("plane.png#enemy_m"),
            Assets.loadImage("plane.png#enemy_s"),
        )
        enemyImage = enemyList[ random.randint(0, len(enemyList) -1) ]
        x = random.randint(0, self.screen.get_width() + enemyImage.get_width() - 1)
        y = -(enemyImage.get_height())
        enemy = Enemy(enemyImage, position = (x, y), speed = random.randint(2, 8))
        self.add_enemy(enemy)
        pass

    def listen_keyboard(self, keyCode, callback):
        if keyCode in self.__listener:
            print("Duplicate key:", keyCode)
            return
        self.__listener[keyCode] = callback
        pass

    def update(self):
        for e in pygame.event.get():
            # print(e)
            if e.type == pygame.QUIT:
                self.__status = GameEngine.STATUS_STOP
            elif event.isTimer(e.type):
                self.__userEventDict[e.type]()
            elif e.type == event.MUSIC_IS_STOP:
                pygame.mixer.music.rewind()
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                self.call_listener(e)
        # for tmp in self.__spriteGroups:
            # tmp.clear(self.screen, self.background.image)
        self.background.update()
        self.screen.blit(self.background.image, (self.background.rect.x, self.background.rect.y) )

        for tmp in self.__spriteGroups:
            tmp.update()
            tmp.draw(self.screen)

        for bullet in self.bulletGroup:
            for enemy in self.planeGroup:
                if enemy == self.player:
                    continue

                if not self.screen.get_rect().colliderect(enemy.rect):
                    enemy.kill()
                    continue

                if bullet.rect.colliderect(enemy.rect):
                    enemy.kill()
                    bullet.kill()
        pass

    def call_listener(self, event):
        # print(event)
        if event.key not in self.__listener:
            return

        callback = self.__listener[event.key]
        callback(event)
        return

    def run(self, fps = 70):
        delayMiliSeconds = int(1000 / fps)

        while not self.is_stop():
            pygame.display.update()
            pygame.time.delay(delayMiliSeconds)
            self.update()
            pass

    def close(self):
        pygame.quit()
        pass