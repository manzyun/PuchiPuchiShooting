import pygame
import random

import game

class Enemy(pygame.sprite.Sprite):
    """
    エネミークラス
    """
    speed = 3 # 移動速度

    def __init__(self):
        """
        初期化処理

        .. note::
          敵は上からランダムに出てきます。
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(game.SCR_RECT.width - self.rect.width)
        self.rect.bottom = game.SCR_RECT.top

    def update(self):
        """
        更新処理

        .. note::
          ランダムで動き回ります。
        """
        mov_vec = [(-self.speed, 0), (0, self.speed), (self.speed, 0), (0, -self.speed)] # 上, 右, 下, 左の順で指定。
        self.rect.move_ip(random.choice(mov_vec))
