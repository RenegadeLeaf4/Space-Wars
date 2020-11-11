import pygame 
import os
import random

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 580 
SCREEN_HEIGHT = 640
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space-Wars")

# Background
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

# Ship(PLayer)
GREEN_SHIP = pygame.image.load(os.path.join("assets", "player_green.png")).convert_alpha()
ORANGE_SHIP = pygame.image.load(os.path.join("assets", "player_orange.png")).convert_alpha()
RED_SHIP = pygame.image.load(os.path.join("assets", "player_red.png")).convert_alpha()
BLUE_SHIP = pygame.image.load(os.path.join("assets", "player_red.png")).convert_alpha()

# Ship(Enemy)
BLACK_MARK1 = pygame.image.load(os.path.join("assets/enemies", "enemyBlack1.png")).convert_alpha()
BLACK_MARK2 = pygame.image.load(os.path.join("assets/enemies", "enemyBLack2.png")).convert_alpha()
BLACK_MARK3 = pygame.image.load(os.path.join("assets/enemies", "enemyBlack3.png")).convert_alpha()

# UFO
BLUE_UFO = pygame.image.load(os.path.join("assets/enemies", "ufoBlue.png")).convert_alpha()
GREEN_UFO = pygame.image.load(os.path.join("assets/enemies", "ufoGreen.png")).convert_alpha()
RED_UFO = pygame.image.load(os.path.join("assets/enemies", "ufoRed.png")).convert_alpha()
YELLOW_UFO = pygame.image.load(os.path.join("assets/enemies", "ufoYellow.png")).convert_alpha()


# Laser 
BLUE_LASER = pygame.image.load(os.path.join("assets/lasers", "laserBlue1.png")).convert_alpha()
GREEN_LASER = pygame.image.load(os.path.join("assets/lasers", "laserGreen1.png")).convert_alpha()
RED_LASER = pygame.image.load(os.path.join("assets/lasers", "laserRed1.png")).convert_alpha()
ENEMY_LASER = pygame.image.load(os.path.join("assets/lasers", "laserRedEnemy.png")).convert_alpha()

# Meteor
METEOR_BROWN_LARGE1 = pygame.image.load(os.path.join("assets/meteors", "meteorBrown_big1.png")).convert_alpha()
METEOR_BROWN_LARGE2 = pygame.image.load(os.path.join("assets/meteors", "meteorBrown_big2.png")).convert_alpha()
METEOR_BROWM_MED = pygame.image.load(os.path.join("assets/meteors", "meteorBrown_med.png")).convert_alpha()
METEOR_BROWM_SMALL = pygame.image.load(os.path.join("assets/meteors", "meteorBrown_small.png")).convert_alpha()

# Effects
REGULAR_EXPLOSIONS = [pygame.image.load(os.path.join("assets/effects", "explosion" + str(x) + ".png")) for x in range(9)]
SONIC_EXPLOSIONS = [pygame.image.load(os.path.join("assets/effects", "sonic_explosion" + str(x) + ".png")) for x in range(9)]

# Sound
EXPLOSION_SND = pygame.mixer.Sound(os.path.join("assets/sound" , "sfx_explosion.ogg"))
LASER_SND = pygame.mixer.Sound(os.path.join("assets/sound", "sfx_laser.ogg"))
LOSE_SND = pygame.mixer.Sound(os.path.join("assets/sound" , "sfx_lose.ogg"))
SHIELD_SND = pygame.mixer.Sound(os.path.join("assets/sound" , "sfx_shieldUp.ogg"))
ZAP_SND = pygame.mixer.Sound(os.path.join("assets/sound", "sfx_zap.ogg"))

WHITE = (0, 0, 0)
BLACK = (255, 255, 255)
YELLOW = (0, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255, 0)

clock = pygame.time.Clock()

class Laser(): 
    VEL = 6

    def __init__(self, x, y, img): 
        self.x = x 
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen): 
        screen.blit(self.img, (self.x, self.y))

    def move(self): 
        self.y -= self.VEL

    def collision(self, obj): 
        if collision(self, obj): 
            return True

        return False 

class Ship():
    VEL = 8
    COOLDOWN = 15

    def __init__(self, x, y): 
        self.x = x 
        self.y = y

        self.img = None
        self.laser_img = None
        self.lasers = []
        self.health = 100 
        self.cooldown_counter = 0

    def draw(self, screen): 
        screen.blit(self.img, (self.x, self.y))
        for laser in self.lasers: 
            laser.draw(screen)

    def cooldown(self): 
        if self.cooldown_counter > 0:
            self.cooldown_counter += 1
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0

    def move_lasers(self, obj, objs, temp): 
        self.cooldown()
        for laser in self.lasers[:]: 
            laser.move()
            if laser.y <= 0: 
                self.lasers.remove(laser)

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x + self.img.get_width() / 2 - self.laser_img.get_width() + 4, self.y - self.laser_img.get_height(), self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter += 1

    def get_width(self): 
        return self.img.get_width()

    def get_height(self): 
        return self.img.get_height()

class Player(Ship): 
    def __init__(self, x, y): 
        super().__init__(x, y)
        self.img = RED_SHIP
        self.mask = pygame.mask.from_surface(self.img)

        self.laser_img = RED_LASER

class Enenmy(Ship):
    def __init__(self): 
        # super().__init__()
        pass

class Meteor(): 
    SIZE_MAP = {
        "large1": METEOR_BROWN_LARGE1,
        "large2": METEOR_BROWN_LARGE2,
        "med": METEOR_BROWM_MED,
        "small": METEOR_BROWM_SMALL
    }

    VEL_X = random.randrange(-4, 4)
    VEL_Y = random.randrange(3, 10)

    def __init__(self, size):
        self.img = self.SIZE_MAP[size]
        self.mask = pygame.mask.from_surface(self.img) 

        self.x = random.randrange(SCREEN_WIDTH - self.img.get_width())
        self.y = random.randrange(-240, -100)

    def draw(self, screen): 
        screen.blit(self.img, (self.x, self.y))

    def move(self): 
        self.x += self.VEL_X
        self.y += self.VEL_Y

    def create_new(self): 
        self.x = random.randrange(SCREEN_WIDTH - self.img.get_width())
        self.y = random.randrange(-240, -100)
        self.VEL_X = random.randrange(-5, 5)
        self.VEL_Y = random.randrange(5, 10)

def collision(obj1, obj2): 
    offset_x = round(obj2.x - obj1.x)
    offset_y = round(obj2.y - obj1.y)

    collide_mask = obj1.mask.overlap(obj2.mask, (offset_x, offset_y))

    if collide_mask:
        return True
    
    return False

def blit_rotate_center(img, position, angle): 
    pass

def menu_screen(screen): 
    pass

def game_over_screen(screen): 
    pass

def main(screen): 
    run = True
    game = True 
    lost = False

    wave_lenght = 8

    meteors = []

    player = Player(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT - 80)

    def redraw_game_window(screen): 
        screen.blit(BG_IMG, (0, 0)) 

        player.draw(screen)
        for meteor in meteors:
            meteor.draw(screen) 
        pygame.display.update()

    while run: 
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.K_UP: 
                if event.type == pygame.K_SPACE: 
                    game = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player.VEL
        if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.get_width(): 
            player.x += player.VEL
        if keys[pygame.K_SPACE]: 
            player.shoot()

        if game:
            temp = []
            if len(meteors) == 0:
                for i in range(wave_lenght):
                    meteor = Meteor(random.choice(["large1", "large2", "med", "small"]))
                    meteors.append(meteor)
            
            for laser in player.lasers[:]: 
                for meteor in  meteors[:]: 
                    if laser.collision(meteor): 
                        meteors.remove(meteor)
                        temp.append(meteor)
                        if laser in player.lasers: 
                            player.lasers.remove(laser)

            for meteor in meteors[:]: 
                meteor.move()
                if meteor.y > SCREEN_HEIGHT or meteor.x <= (0 - meteor.img.get_width()) or meteor.x >= SCREEN_WIDTH: 
                    meteors.remove(meteor)
                    temp.append(meteor)

                if collision(meteor, player): 
                    meteors.remove(meteor)
                    temp.append(meteor)

            if len(meteors) < wave_lenght:
                for i in range(len(temp)):
                    meteor = Meteor(random.choice(["large1", "large2", "med", "small"]))
                    meteor.create_new()
                    meteors.append(meteor)
                    lost = True
                    print(meteor.VEL_X, meteor.VEL_Y)

            player.move_lasers(meteor, meteors, temp)        

        redraw_game_window(screen)

    game_over_screen(screen)

main(screen) 