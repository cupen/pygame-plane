# coding:utf-8
__author__ = 'cupen'
import random
from pygame.constants import USEREVENT
import pygame
import resource
from sprites import Background, Bullet, Enemy

ENEMY_REFRESH = USEREVENT + 1

class GameEngine:
    STATUS_RUNNING = 0
    STATUS_STOP    = 1
    STATUS_PAUSE   = 2

    def __init__(self):
        pygame.init()
        self.__listener = {}
        self.__status = GameEngine.STATUS_RUNNING
        self.planeGroup = pygame.sprite.Group()
        self.bulletGroup = pygame.sprite.Group()
        self.background = None
        self.screen = None
        self.srcLoader = resource
        self.__spriteGroups = (self.planeGroup, self.bulletGroup)
        self.player = None
        pass

    def set_enemy_count_per_seconds(self, count):
        pygame.time.set_timer(ENEMY_REFRESH, int(1000 / count))
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
            bullet = self.player.create_bullet(self.srcLoader.getSurface("bullet_0"), self.screen.get_rect())
            self.bulletGroup.add(bullet)
        pass

    def set_background(self, imageNameList, width, height):
        self.screen = pygame.display.set_mode((width, height))
        resource.load()
        pygame.display.set_icon(resource.getSurface("icon48x48.png"))
        _list = []
        for tmp in imageNameList:
            image = resource.getSurface(tmp)
            _list.append(image)
        self.background = Background(_list, width=width, height=height)
        self.screen.blit(self.background.image, (self.background.rect.x, self.background.rect.y) )
        pass

    def create_sprite(self, imageName, spriteClass = pygame.sprite.Sprite):
        surface = self.srcLoader.getSurface(imageName)
        return spriteClass(surface)

    def add_plane(self, sprite):
        self.planeGroup.add(sprite)
        pass

    def add_bullet(self, bullet):
        pass

    def play_music(self, musicFile):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play()

        # TODO: holy shit! 播完不知道怎么重放，endevent看起来木起作用
        for i in range(30):
            pygame.mixer.music.queue(musicFile)

        pygame.mixer.music.set_endevent(pygame.USEREVENT + 2)
        pass

    def is_stop(self):
        return self.__status == GameEngine.STATUS_STOP

    def is_pause(self):
        return self.__status == GameEngine.STATUS_PAUSE

    def refresh_enemy(self):
        enemyList = (
            self.srcLoader.getSurface("enemy_b"),
            self.srcLoader.getSurface("enemy_m"),
            self.srcLoader.getSurface("enemy_s"),
        )
        enemyImage = enemyList[ random.randint(0, len(enemyList) -1) ]
        x = random.randint(0, self.screen.get_width() + enemyImage.get_width() - 1)
        y = -(enemyImage.get_height())
        enemy = Enemy(enemyImage, position = (x, y), speed = random.randint(2, 8))
        self.add_enemy(enemy)
        pass

    def listen_keyboard(self, keyCode, callback):
        if keyCode in self.__listener:
            print("Dumplicate key:", keyCode)
            return
        self.__listener[keyCode] = callback
        pass

    def update(self):
        for e in pygame.event.get():
            # print(e)
            if e.type == pygame.QUIT:
                self.__status = GameEngine.STATUS_STOP
            if e.type == ENEMY_REFRESH:
                self.refresh_enemy()
            if e.type == pygame.USEREVENT + 2:
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

                if not bullet.rect.colliderect(enemy.rect):
                    continue

                bullet.kill()
                enemy.kill()
        pass

    def call_listener(self, event):
        # print(event)
        if event.key not in self.__listener:
            return

        callback = self.__listener[event.key]
        callback(event)
        return

    def run(self, fps = 70):
        fps = 70
        delayMiliSeconds = int(1000 / fps)

        while not self.is_stop():
            pygame.display.update()
            pygame.time.delay(delayMiliSeconds)
            self.update()
            pass

    def close(self):
        pygame.quit()
        pass