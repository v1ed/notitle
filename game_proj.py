import pygame
import os
import sys


FPS = 60
pygame.init()
size = WIDTH, HEIGHT = 550, 550
MOVE_SPEED = 10
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
# filename = input()
MISSON_ACTIVE = False
pygame.key.set_repeat(1, 50)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    screen.fill((255, 255, 255))
    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def Mission():
    global MISSON_ACTIVE
    if MISSON_ACTIVE:
        return
    else:
        text = ['Здесь должен быть текст миссии',
                "И еще текст",
                "SPACE - принять миссию", "TAB - отклонить миссию"]
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('Mission active')
                        MISSON_ACTIVE = True
                        return False
                    elif event.key == pygame.K_TAB:
                        return True
            pygame.display.flip()
            clock.tick(FPS)

def endMission():
    global MISSON_ACTIVE
    if not MISSON_ACTIVE:
        return
    else:
        text = ['Здесь должен быть текст миссии',
                "Миссия завершена",
                "SPACE - закрыть экран завершения миссии"]
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('Mission completed')
                        MISSON_ACTIVE = False
                        return
            pygame.display.flip()
            clock.tick(FPS)
def Pause():
    text = ['Игра на паузе', 'Нажмите любую клавишу, чтобы убрать паузу']
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '#'), level_map))

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
startMisTrig_group = pygame.sprite.Group()
endMisTrig_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Floor('floor', x, y)
            elif level[y][x] == '#':
                Walls('wall', x, y)
            elif level[y][x] == '@':
                Floor('floor', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '/':
                StartMissionTrigger('start_mission_trigger', x, y)
            elif level[y][x] == '-':
                EndMissionTrigger('end_mission_trigger', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

floor_images = {'floor': load_image('floor.png')}
startMisTrig_images = {'start_mission_trigger': load_image('trigger.png')}
endMisTrig_images = {'end_mission_trigger': load_image('trigger2.png')}
walls_images = {'wall': load_image('box.png')}
player_forward = load_image('player_forward.png', -1)
player_backward = load_image('player_backward.png', -1)
player_left = load_image('player_left.png', -1)
player_right = load_image('player_right.png', -1)

tile_width = tile_height = 64

class Walls(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = walls_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

class Floor(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(floor_group, all_sprites)
        self.image = floor_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

class StartMissionTrigger(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(startMisTrig_group, all_sprites)
        self.image = startMisTrig_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

class EndMissionTrigger(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(endMisTrig_group, all_sprites)
        self.image = endMisTrig_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_forward
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, keys):
        global MISSON_ACTIVE
        if keys[pygame.K_LEFT] == 1:
            self.rect.x -= MOVE_SPEED
            self.image = player_left
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x += MOVE_SPEED
        if keys[pygame.K_RIGHT] == 1:
            self.rect.x += MOVE_SPEED
            self.image = player_right
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x -= MOVE_SPEED
        if keys[pygame.K_DOWN] == 1:
            self.rect.y += MOVE_SPEED
            self.image = player_forward
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y -= MOVE_SPEED
        if keys[pygame.K_UP] == 1:
            self.rect.y -= MOVE_SPEED
            self.image = player_backward
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y += MOVE_SPEED
        if pygame.sprite.spritecollideany(self, startMisTrig_group) and not MISSON_ACTIVE:
            Mission()
        if pygame.sprite.spritecollideany(self, endMisTrig_group) and MISSON_ACTIVE:
            endMission()
        if keys[pygame.K_ESCAPE] == 1:
            Pause()

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)

running = True
start_screen()
player, level_x, level_y = generate_level(load_level('testlevel.txt'))
camera = Camera()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player_group.update(pygame.key.get_pressed())
    # изменяем ракурс камеры
    camera.update(player);
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((25, 25, 25))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

