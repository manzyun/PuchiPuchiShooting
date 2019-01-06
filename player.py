import pygame
from pygame.locals import *

import game
import lazer

class Player(pygame.sprite.Sprite):
    """
    プレイヤークラス
    """
    speed = 3 # 移動速度
    charge = 15 # レーザーがチャージされるまでの時間

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = game.SCR_RECT.bottom #プレイヤーは画面の一番下からスタート
        self.rect.left = 400
        self.charge_timer = 0
    def update(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        # 画面からはみ出さないようにする
        self.rect = self.rect.clamp(game.SCR_RECT)

        if pressed_key[K_SPACE]:
            # リロード時間が0になるまで発射できない。
            if self.charge_timer > 0:
                # リロード中
                self.charge_timer -= 1
            else:
                # 発射！
                lazer.Lazer(self.rect.center)# 作成すると同時にall_spriteに追加される。
                self.charge_timer = self.charge
