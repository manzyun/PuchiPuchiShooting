import pygame

class Lazer(pygame.sprite.Sprite):
    """
    レーザークラス

    エネミーへの唯一の武器
    """

    speed = 9 # レーザーの移動速度

    def __init__(self, pos):
        """
        初期化処理
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        self.rect.move_ip(0, -self.speed) # 上へ移動
        if self.rect.top < 0: # 上辺に達したら削除
            self.kill()
