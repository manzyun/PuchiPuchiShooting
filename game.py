import toothpick, player, enemy, lazer
import pygame
from pygame.locals import *
import random
import sys

GAME_MODE = {'START': 0, 'PLAY': 1, 'GAMEOVER': 2}
SCR_RECT = Rect(0, 0, 800, 600) # スクリーンサイズ(px指定)

class Game:
    """
    ゲームの構成そのものをまとめたクラス

    .. tip::

      クラス化することで各メソッドで共通して使う変数にアクセスしやすくする。
    """
    enemy_prob = 12 #敵の出現率

    def __init__(self):
        """
        各種読み込み.
        """
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption('プチプチシューティング')
        # 素材のロード
        self.load_images()
        # ゲームオブジェクトを初期化
        self.init_game()
        # メインループ開始
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self):
        """
        ゲームオブジェクトを初期化
        """
        # ゲームの状態
        self.game_state = GAME_MODE['START']
        # スプライトグループを作成して登録
        self.all_sprite = pygame.sprite.RenderUpdates()
        self.pc = pygame.sprite.Group() # HACK: 違和感あるけど、プレイヤーキャラクターグループ
        self.enemies = pygame.sprite.Group() # エネミーグループ
        self.lazers = pygame.sprite.Group() # レーザーグループ
        # デフォルトスプライトグループを登録
        player.Player.containers = self.all_sprite, self.pc
        enemy.Enemy.containers = self.all_sprite, self.enemies
        lazer.Lazer.containers = self.all_sprite, self.lazers
        # プレイヤーを作成
        self.player = player.Player()
        # スコア初期化
        self.score = 0

    def update(self):
        """
        情報の更新と敵の出現管理
        """
        if self.game_state == GAME_MODE['PLAY']:
            # 0からenemy_probまでの乱数を出して、0が出たらエネミー出現
            # つまりこのクラスの変数enemy_probを大きくすると……
            if not random.randrange(self.enemy_prob):
                enemy.Enemy()
            self.all_sprite.update()
            self.collision_detection()

    def draw(self, screen):
        """
        描画
        """
        screen.fill((0, 0, 0))
        if self.game_state == GAME_MODE['START']:
            # タイトル画面描画
            title_font = pygame.font.SysFont(None, 80)
            title = title_font.render('Puchi Puchi Shooting', False, (255, 0, 128))
            screen.blit(title, ((SCR_RECT.width - title.get_width()) / 2, 200))
            # エネミーのみ描画
            enemy_image = enemy.Enemy.image
            screen.blit(enemy_image, ((SCR_RECT.width - enemy_image.get_width())/ 2, 300))
            # PUSH SPACE KEYを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255, 255, 255))
            screen.blit(push_space, ((SCR_RECT.width - push_space.get_width()) / 2, 400))
            # クレジット描画
            credit_font = pygame.font.SysFont(None, 20)
            credit = credit_font.render('2017 CoderDojo Sapporo', False, (255, 255, 255))
            screen.blit(credit, ((SCR_RECT.width - credit.get_width()) / 2, 600))

        if self.game_state == GAME_MODE['PLAY']:
            # ゲームプレイ
            self.all_sprite.draw(screen)
            # 得点表示
            score_font = pygame.font.SysFont(None, 80)
            score = score_font.render("{0:0>4d}".format(self.score), False, (255, 255, 255))
            screen.blit(score, (SCR_RECT.left, SCR_RECT.top))

        if self.game_state == GAME_MODE['GAMEOVER']:
            # GAME OVERを描画
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("GAME OVER", False, (255, 0, 0))
            screen.blit(gameover, ((SCR_RECT.width - gameover.get_width()) / 2, 200))
            # PUSH STARTを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255, 255, 255))
            screen.blit(push_space, ((SCR_RECT.width - push_space.get_width()) / 2, 400))
            # 得点表示
            score_font = pygame.font.SysFont(None, 80)
            score = score_font.render("You got {0:0>4d} points!".format(self.score), False, (255, 255, 255))
            screen.blit(score, ((SCR_RECT.width - score.get_width()) / 2, 300))

    def collision_detection(self):
        """
        衝突判定

        プレイヤーとエネミー、レーザーとエネミーの衝突判定を行う
        """
        player_collided = pygame.sprite.groupcollide(self.enemies, self.pc, True, True)
        for enemy in player_collided.keys():
            self.game_state = GAME_MODE["GAMEOVER"]

        lazer_collided = pygame.sprite.groupcollide(self.enemies, self.lazers, True, True)
        for lazer in lazer_collided.keys():
            self.score += 1


    def load_images(self):
        """
        各イメージの読み込み
        """
        # スプライトの画像を登録
        player.Player.image = toothpick.load_image("img/pc_img.png")
        enemy.Enemy.image = toothpick.load_image("img/enemy_img.png")
        lazer.Lazer.image = toothpick.load_image("img/lazer.png")

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.game_state == GAME_MODE['START']: # スタート画面でスペースキーを押したらスタート
                    self.game_state = GAME_MODE['PLAY']
                elif self.game_state == GAME_MODE['GAMEOVER']: # ゲームオーバー
                    self.init_game() #ゲームを初期化して再開
                    self.game_state = GAME_MODE['PLAY']
