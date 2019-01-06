import pygame
import re

def load_image(filename, colorkey=None):
    """
    画像をロードする。

    @param filename ファイル名（ディレクトリ含む）
    @param colorkey 背景色 (デフォルト値 None)
    @return pygame.surface.Surface
    """
    # 画像ファイルがpngかgifか判定するための正規表現
    filecase = re.compile(r'[a-zA-Z0-9_/]+\.png|[a-zA-Z0-9_/]+\.gif')

    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image: " + filename)
        raise SystemExit(message)

    # 画像の拡張子によって処理を振り分け
    is_match = filecase.match(filename)
    if is_match:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image
