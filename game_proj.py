import pygame
import os
import sys
import time

FPS = 60
pygame.init()
displayInfo = pygame.display.Info()
size = WIDTH, HEIGHT = displayInfo.current_w, displayInfo.current_h
MOVE_SPEED = 10
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
MISSON_ACTIVE = False
HP = 100
EXP = 0
SPEED_UP = 1
pygame.key.set_repeat(1, 50)
is_cancel = False
missions = 0
# def wait(secs):
#     while time.sleep(secs):
#         return False
#     return True

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
    saveGame()
    pygame.quit()
    sys.exit()

def saveGame():
    global EXP, SPEED_UP, MOVE_SPEED, HP
    save = open("data/save.txt", "w")
    save.write(str(int(EXP)) + "\n")
    save.write(str(int(SPEED_UP)) + "\n")
    save.write(str(int(MOVE_SPEED)) + "\n")
    save.write(str(int(HP)))
    save.close()

def loadGame():
    global EXP, SPEED_UP, MOVE_SPEED, HP
    save = open("data/save.txt", "r")
    read = str(save.read()).split('\n')
    EXP = int(read[0])
    SPEED_UP = int(read[1])
    MOVE_SPEED = int(read[2])
    HP = int(read[3])
    save.close()

def new_game():
    global EXP, SPEED_UP, MOVE_SPEED, HP
    EXP = 0
    SPEED_UP = 1
    MOVE_SPEED = 10
    HP = 100

def start_screen():
    screen.fill((255, 255, 255))
    bg = pygame.transform.scale(load_image('mainmenu.png'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))

    while True:
        mp = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (mp[0] >= 745 and mp[0] <= 1180) and (mp[1] >= 490 and mp[1] <= 540):
                new_game()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and (mp[0] >= 745 and mp[0] <= 1180) and (mp[1] >= 555 and mp[1] <= 600):
                loadGame()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and (mp[0] >= 870 and mp[0] <= 1050) and (mp[1] >= 675 and mp[1] <= 710):
                terminate()
        print(mp)
        pygame.display.flip()
        clock.tick(FPS)

def Mission():
    global is_cancel
    if is_cancel == False:
        global MISSON_ACTIVE
        if MISSON_ACTIVE:
            return
        else:
            screen.fill((255, 255, 255))
            bg = pygame.transform.scale(load_image('mission_start.png'), (WIDTH, HEIGHT))
            screen.blit(bg, (0, 0))
            while True:
                mp = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if (mp[0] >= 160 and mp[0] <= 640) and (mp[1] >= 960 and mp[1] <= 1030):
                            print('Mission active')
                            MISSON_ACTIVE = True
                            return
                        elif (mp[0] >= 1255 and mp[0] <= 1575) and (mp[1] >= 960 and mp[1] <= 1030):
                            is_cancel = True
                            return False
                print(mp)
                pygame.display.flip()
                clock.tick(FPS)

def endMission():
    global MISSON_ACTIVE
    global EXP
    global missions
    if not MISSON_ACTIVE:
        return
    else:
        screen.fill((255, 255, 255))
        bg = pygame.transform.scale(load_image('mission_end.png'), (WIDTH, HEIGHT))
        screen.blit(bg, (0, 0))
        while True:
            mp = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN and (mp[0] >= 720 and mp[0] <= 1200) and (mp[1] >= 810 and mp[1] <= 880):
                    print('Mission completed')
                    EXP += 100
                    MISSON_ACTIVE = False
                    return
                print(mp)
            missions += 1
            pygame.display.flip()
            clock.tick(FPS)


def Pause():
    screen.fill((255, 255, 255))
    bg = pygame.transform.scale(load_image('pause.png'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    while True:
        mp = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (mp[0] >= 870 and mp[0] <= 1050) and (mp[1] >= 675 and mp[1] <= 710):
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and (mp[0] >= 640 and mp[0] <= 1265) and (mp[1] >= 510 and mp[1] <= 575):
                return
        print(mp)
        pygame.display.flip()
        clock.tick(FPS)

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '#'), level_map))

def experience():
    global EXP
    font = pygame.font.Font(None, 40)
    exp_render = font.render('Exp: ' + str(EXP), 1, (100, 255, 0))
    screen.blit(exp_render, (20, 20))

def health():
    global HP
    font = pygame.font.Font(None, 40)
    hp_render = font.render('HP: ' + str(HP), 1, (100, 255, 0))
    screen.blit(hp_render, (20, 50))

def DeadScreen():
    font = pygame.font.Font(None, 40)
    text_render = font.render('YOU DIE', 1, (200, 0, 0))
    text_x = WIDTH // 2 - text_render.get_width() // 2
    text_y = HEIGHT // 2 - text_render.get_height() // 2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return True
        screen.blit(text_render, (text_x, text_y))
        pygame.display.flip()

def upgrades():
    global EXP
    global SPEED_UP
    global MOVE_SPEED
    upgrades = ['1. SPEED UPGRADE - ' + str(int(100 * (SPEED_UP * 0.5))) + 'EXP', '2. HEALTH UPGRADE -']
    font = pygame.font.Font(None, 40)
    # pygame.draw.rect(screen, (50, 50, 75), (50, 241, 450, 68), 0)
    upgrades_render = font.render('1. SPEED UPGRADE - ' + str(int(100 * (SPEED_UP * 0.5))) + 'EXP', 1, (255, 255, 255))
    cost_render = font.render(str(100 * (SPEED_UP * 0.5)), 1, (255, 255, 255))
    text_x = WIDTH // 2 - upgrades_render.get_width() // 2
    text_y = HEIGHT // 2 - upgrades_render.get_height() // 2
    text_w = upgrades_render.get_width()
    text_h = upgrades_render.get_height()
    print(text_x, text_y, text_h, text_w)
    screen.blit(upgrades_render, (text_x, text_y))
    pygame.draw.rect(screen, (50, 50, 75), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 0)
    screen.blit(upgrades_render, (text_x, text_y))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and EXP >= 100 * (SPEED_UP * 0.5) and SPEED_UP <= 10:
                    print('Upgrade bought')
                    SPEED_UP += 1
                    MOVE_SPEED += 2
                    EXP -= 100 * (SPEED_UP * 0.5)
                    print(100 * (SPEED_UP * 0.5))
                    pygame.time.wait(500)
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return
        pygame.display.flip()
        clock.tick(FPS)

def cheat():
    global EXP, HP
    EXP += 500
    HP = 100
    font = pygame.font.Font(None, 40)
    cheat_render = font.render('cheat activated!', 1, (0, 255, 0))
    screen.blit(cheat_render, (10, 1050))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


player = None

all_sprites = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
floor_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
damage_group = pygame.sprite.Group()
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
            elif level[y][x] == 'x':
                Floor('lava', x, y)
            elif level[y][x] == 'd':
                Door('door', x, y)
    return new_player, x, y


floor_images = {'floor': load_image('floor.png'), 'lava' : load_image('lava.png')}
door_images = {'door': load_image('Door.png')}
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
        if tile_type == 'floor':
            super().__init__(floor_group, all_sprites)
            self.image = floor_images[tile_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        elif tile_type == 'lava':
            super().__init__(damage_group, all_sprites)
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


class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.image = door_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_forward
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, keys):
        global is_cancel
        # global MISSON_ACTIVE
        global HP
        if keys[pygame.K_LEFT] == 1:
            self.rect.x -= MOVE_SPEED
            self.image = player_left
            if pygame.sprite.spritecollideany(self, walls_group) or pygame.sprite.spritecollideany(self, door_group):
                self.rect.x += MOVE_SPEED
        if keys[pygame.K_RIGHT] == 1:
            self.rect.x += MOVE_SPEED
            self.image = player_right
            if pygame.sprite.spritecollideany(self, walls_group) or pygame.sprite.spritecollideany(self, door_group):
                self.rect.x -= MOVE_SPEED
        if keys[pygame.K_DOWN] == 1:
            self.rect.y += MOVE_SPEED
            self.image = player_forward
            if pygame.sprite.spritecollideany(self, walls_group) or pygame.sprite.spritecollideany(self, door_group):
                self.rect.y -= MOVE_SPEED
        if keys[pygame.K_UP] == 1:
            self.rect.y -= MOVE_SPEED
            self.image = player_backward
            if pygame.sprite.spritecollideany(self, walls_group) or pygame.sprite.spritecollideany(self, door_group):
                self.rect.y += MOVE_SPEED
        if pygame.sprite.spritecollideany(self, startMisTrig_group) and not MISSON_ACTIVE:
            if not Mission():
                pygame.time.set_timer(pygame.KEYDOWN, 1000)
            Mission()
        if pygame.sprite.spritecollideany(self, endMisTrig_group) and MISSON_ACTIVE:
            endMission()
        if keys[pygame.K_ESCAPE] == 1:
            Pause()
        if keys[pygame.K_e] == 1:
            while upgrades():
                upgrades()
        if pygame.sprite.spritecollideany(self, damage_group):
            HP -= 1
            # pygame.time.set_timer(pygame.sprite.spritecollideany(self, damage_group), 1000)
            if HP <= 0:
                if DeadScreen():
                    start_screen()
        if keys[pygame.K_b] == 1 and keys[pygame.K_a] == 1 and keys[pygame.K_d] == 1:
            print('activated!')
            cheat()
        if not pygame.sprite.spritecollideany(self, startMisTrig_group) and is_cancel and not MISSON_ACTIVE:
            is_cancel = False



class Menu:
    pass


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

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
            saveGame()
        if event.type == pygame.KEYDOWN:
            player_group.update(pygame.key.get_pressed())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b and event.key == pygame.K_a and event.key == pygame.K_d:
                print('nice')
                cheat()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((25, 25, 25))
    all_sprites.draw(screen)
    player_group.draw(screen)
    experience()
    health()
    pygame.display.flip()