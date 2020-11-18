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

MAIN_FONT = pygame.font.Font(os.path.join("assets", "kenvector_future_thin.ttf"), 30)
MAIN_FONT_BIGGER = pygame.font.Font(os.path.join("assets", "kenvector_future_thin.ttf"), 50)
MAIN_FONT_SMALLER = pygame.font.Font(os.path.join("assets", "kenvector_future_thin.ttf"), 20)

# Background
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

# Ship(PLayer)
GREEN_SHIPS = [pygame.image.load(os.path.join("assets", "player_green" + str(x) + ".png")).convert_alpha() for x in range(1, 4)]
ORANGE_SHIPS = [pygame.image.load(os.path.join("assets", "player_orange" + str(x) + ".png")).convert_alpha() for x in range(1, 4)]
RED_SHIPS = [pygame.image.load(os.path.join("assets", "player_red" + str(x) + ".png")).convert_alpha() for x in range(1, 4)]
BLUE_SHIPS = [pygame.image.load(os.path.join("assets", "player_blue" + str(x) + ".png")).convert_alpha() for x in range(1, 4)]

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
REGULAR_EXPLOSIONS = [pygame.transform.scale(pygame.image.load(os.path.join("assets/effects", "explosion" + str(x) + ".png")).convert_alpha(), (65, 65)) for x in range(9)]
SONIC_EXPLOSIONS = [pygame.transform.scale(pygame.image.load(os.path.join("assets/effects", "sonic_explosion" + str(x) + ".png")).convert_alpha(), (125, 125)) for x in range(9)]

# UI
LIVE_GREEN = pygame.image.load(os.path.join("assets/ui", "lifeGreen.png")).convert_alpha()
LIVE_ORANGE = pygame.image.load(os.path.join("assets/ui", "lifeOrange.png")).convert_alpha()
LIVE_RED= pygame.image.load(os.path.join("assets/ui", "lifeRed.png")).convert_alpha()
LIVE_BLUE = pygame.image.load(os.path.join("assets/ui", "lifeBlue.png")).convert_alpha()

# Sound
EXPLOSION_SND = pygame.mixer.Sound(os.path.join("assets/sound" , "sfx_explosion.ogg"))
LASER_SND = pygame.mixer.Sound(os.path.join("assets/sound", "sfx_laser.ogg"))
POWERUP_SND = pygame.mixer.Sound(os.path.join("assets/sound", "sfx_powerup.ogg"))
LOSE_SND = pygame.mixer.Sound(os.path.join("assets/sound" , "sfx_lose.ogg"))
ZAP_SND = pygame.mixer.Sound(os.path.join("assets/sound", "sfx_zap.ogg"))
GAME_MUSIC = pygame.mixer.music.load(os.path.join("assets/sound", "game_music.mp3"))

pygame.mixer.music.set_volume(0.4)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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
            LASER_SND.play()
            laser = Laser(self.x + self.img.get_width() / 2 - self.laser_img.get_width() + 4, self.y - self.laser_img.get_height(), self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter += 1
        
    def get_width(self): 
        return self.img.get_width()

    def get_height(self): 
        return self.img.get_height()

class Player(Ship): 
    COLOR_MAP = {
        "green": (random.choice(GREEN_SHIPS), GREEN_LASER, LIVE_GREEN),
        "orange": (random.choice(ORANGE_SHIPS), RED_LASER, LIVE_ORANGE),
        "red": (random.choice(RED_SHIPS), RED_LASER, LIVE_RED),
        "blue":(random.choice(BLUE_SHIPS), BLUE_LASER, LIVE_BLUE)
    }

    def __init__(self, x, y, color): 
        super().__init__(x, y)
        self.img, self.laser_img, self.lives_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.img)

        self.lives = 3
        self.is_dead = False 
        self.death_timer = 0

    def draw(self, window):
        super().draw(window)
        self.create_healthbar(window, self.health)
        self.create_lives(screen)

    def create_lives(self, screen): 
        for i in range(self.lives):
            self.lives_x = 432 + 45 * i
            self.lives_y = 50 - self.lives_img.get_height() / 2
            screen.blit(self.lives_img, (self.lives_x, self.lives_y))

    def create_healthbar(self, screen, pct): 
        BAR_LENGHT = 100
        BAR_HEIGHT = 15

        if pct <0: 
            pct = 0
        else: 
            pygame.draw.rect(screen, GREEN, (25, 50 - BAR_HEIGHT / 2, ((pct / 100) * BAR_LENGHT), BAR_HEIGHT))
        
        pygame.draw.rect(screen, WHITE, (25, 50 - BAR_HEIGHT / 2, BAR_LENGHT, BAR_HEIGHT), 2)

    def death(self, x, y): 
        self.x = x
        self.y = y 

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
        self.rot = 0 
        self.rot_vel = random.randrange(-6, 6) % 360

    def draw(self, screen): 
        self.rot += self.rot_vel
        blit_rotate_center(self.img, (self.x, self.y), self.rot)

    def move(self): 
        self.x += self.VEL_X
        self.y += self.VEL_Y
    
    def get_width(self): 
        return self.img.get_width()

    def create_new(self): 
        self.x = random.randrange(SCREEN_WIDTH - self.img.get_width())
        self.y = random.randrange(-240, -100)
        self.VEL_X = random.randrange(-5, 5)
        self.VEL_Y = random.randrange(5, 10)

class Explosion(): 
    DELAY = 10

    def __init__(self, x, y, imgs): 
        self.x = x 
        self.y = y 
        
        self.imgs = imgs
        self.img = imgs[0]

        self.img_count = 0 
        self.animation_finished = False 
    
    def draw(self, screen):
        self.img_count += 1

        if self.img_count <= self.DELAY: 
            self.img = self.imgs[0] 
        elif self.img_count <= self.DELAY * 2: 
            self.img = self.imgs[1]
        elif self.img_count <= self.DELAY * 3: 
            self.img = self.imgs[2]
        elif self.img_count <= self.DELAY * 4: 
            self.img = self.imgs[3]
        elif self.img_count <= self.DELAY * 5: 
            self.img = self.imgs[4]
        elif self.img_count <= self.DELAY * 6: 
            self.img = self.imgs[5]
        elif self.img_count <= self.DELAY * 7: 
            self.img = self.imgs[6]
        elif self.img_count <= self.DELAY * 8: 
            self.img = self.imgs[7]
        elif self.img_count < self.DELAY * 9: 
            self.img = self.imgs[8]
        else:
            self.animation_finished = True

        screen.blit(self.img, (self.x, self.y))

def collision(obj1, obj2): 
    offset_x = round(obj2.x - obj1.x)
    offset_y = round(obj2.y - obj1.y)

    collide_mask = obj1.mask.overlap(obj2.mask, (offset_x, offset_y))

    if collide_mask:
        return True
    
    return False

def blit_rotate_center(img, position, angle): 
    rot_image = pygame.transform.rotate(img, angle)
    rot_rect = rot_image.get_rect(center = img.get_rect(topleft = position).center)

    screen.blit(rot_image, rot_rect.topleft)

def menu_screen(screen): 
    menu_text = MAIN_FONT.render("Press mouse to start", 1, WHITE)
    menu_text_rect = menu_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - menu_text.get_height() / 2))

    screen.blit(BG_IMG, (0, 0))
    screen.blit(menu_text, menu_text_rect)
    
    pygame.display.flip()
    pygame.mixer.music.play(loops=-1)
    run = True 
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN: 
                main(screen)
                run = False

def game_over_screen(screen): 
    go_text = MAIN_FONT_BIGGER.render("You lost!", 1, WHITE)
    go_text_rect = go_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - go_text.get_height() / 2))

    restart_text = MAIN_FONT.render("Press mouse to restart", 1, WHITE)
    restart_text_rect = restart_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))

    screen.blit(BG_IMG, (0, 0))
    screen.blit(go_text, go_text_rect)
    screen.blit(restart_text, restart_text_rect)
    
    pygame.display.flip()
    run = True 
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN: 
                main(screen)
                run = False


def main(screen): 
    run = True
    game = True 

    score = 0

    wave_lenght = 8
    meteors = []

    player = Player(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT - 80, random.choice(["green", "orange", "red", "blue"]))

    explosions = []

    def redraw_game_window(screen): 
        screen.blit(BG_IMG, (0, 0)) 

        for meteor in meteors:
            meteor.draw(screen) 
        
        player.draw(screen)

        score_text = MAIN_FONT.render(str(score), 1, WHITE)
        score_text_rect = score_text.get_rect(center = (SCREEN_WIDTH / 2, 50))
        screen.blit(score_text, score_text_rect)

        death_text = MAIN_FONT_SMALLER.render("Press arrow key up to get back to the position", 1, WHITE)
        death_text_rect = death_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        if player.y > SCREEN_HEIGHT - 80: 
            screen.blit(death_text, death_text_rect)

        for meteor_explosion in explosions: 
            meteor_explosion.draw(screen)

        for player_explosion in explosions: 
            player_explosion.draw(screen)

        for death_explosion in explosions: 
            death_explosion.draw(screen)

        pygame.display.update()

    while run: 
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.K_UP: 
                if event.type == pygame.K_SPACE: 
                    game = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0 and player.y == SCREEN_HEIGHT - 80:
            player.x -= player.VEL
        if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.get_width() and player.y == SCREEN_HEIGHT - 80: 
            player.x += player.VEL
        if keys[pygame.K_UP] and player.y > SCREEN_HEIGHT - 80: 
            player.y -= player.VEL
        if keys[pygame.K_SPACE] and player.y == SCREEN_HEIGHT - 80: 
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
                        EXPLOSION_SND.play()
                        meteor_explosion = Explosion(meteor.x + meteor.img.get_width() / 2, meteor.y - meteor.img.get_height() / 2, REGULAR_EXPLOSIONS)
                        explosions.append(meteor_explosion)
                        for meteor_explosion in explosions:
                            if meteor_explosion.animation_finished: 
                                explosions.remove(meteor_explosion)

                        if meteor.get_width() >= 89: 
                            score += 25
                        elif meteor.get_width() == 43: 
                            score += 18 
                        elif meteor.get_width() == 29: 
                            score += 12 

                        meteors.remove(meteor)
                        temp.append(meteor)
                        if laser in player.lasers: 
                            player.lasers.remove(laser) 

            for meteor in meteors[:]: 
                meteor.move()
                if meteor.y > SCREEN_HEIGHT or meteor.x <= (0 - meteor.img.get_width()) or meteor.x >= SCREEN_WIDTH: 
                    meteors.remove(meteor)
                    temp.append(meteor)

                if collision(meteor, player) and player.y == SCREEN_HEIGHT - 80: 
                    EXPLOSION_SND.play()
                    if meteor in meteors: 
                        meteors.remove(meteor)
                    temp.append(meteor)
                    player_explosion = Explosion(meteor.x + meteor.img.get_width() / 2, meteor.y - meteor.img.get_height() / 2, REGULAR_EXPLOSIONS)
                    if player.health > 12: 
                        explosions.append(player_explosion)
                    for player_explosion in explosions: 
                        if player_explosion.animation_finished: 
                            explosions.remove(player_explosion)

                    if meteor.get_width() >= 89: 
                        player.health -= 25
                    elif meteor.get_width() == 43: 
                        player.health -= 18
                    elif meteor.get_width() == 29: 
                        player.health -= 12

                    if player.health <= 0: 
                        LOSE_SND.play()
                        death_explosion = Explosion(player.x + player.img.get_width() / 2, player.y - player.img.get_height() / 2, SONIC_EXPLOSIONS)
                        explosions.append(death_explosion)
                        for death_explosion in explosions: 
                            if death_explosion.animation_finished: 
                                explosions.remove(death_explosion)
                        player.death(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT + 200)
                        player.lives -= 1   

                        if player.lives >= 1: 
                            player.health = 100
                        elif player.lives <= 0: 
                            LOSE_SND.play()
                            run =  False 

            if len(meteors) < wave_lenght:
                for i in range(len(temp)):
                    meteor = Meteor(random.choice(["large1", "large2", "med", "small"]))
                    meteor.create_new()
                    meteors.append(meteor)

            player.move_lasers(meteor, meteors, temp)        

        redraw_game_window(screen)

    game_over_screen(screen)

menu_screen(screen) 