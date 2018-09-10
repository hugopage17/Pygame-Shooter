import pygame
import random
from os import path
import random
import datetime

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 600
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,  255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mech Defence")
clock = pygame.time.Clock()
font_name = pygame.font.match_font("arial")

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (96, 96))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.top = 0
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -15
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 15
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def ShootRight(self):
        right_bullet = Bullet(self.rect.centerx + 40, self.rect.bottom - 60)
        all_sprites.add(right_bullet)
        bullets.add(right_bullet)

    def ShootLeft(self):
        left_bullet = Bullet(self.rect.centerx - 40, self.rect.bottom - 60)
        all_sprites.add(left_bullet)
        bullets.add(left_bullet)

    def FireRocket(self):
        rocket = Rocket(self.rect.centerx, self.rect.top + 55)
        all_sprites.add(rocket)
        rockets.add(rocket)

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(npc_img, (36, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = 350
        self.rect.top = 50
        self.speedx = 5

    def update(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        for m in mobs:
            if npc.rect.x != m.rect.x:
                if m.rect.x > npc.rect.x:
                    npc.speedx = 5
                    npc.rect.x += npc.speedx
                if m.rect.x < npc.rect.x:
                    npc.speedx = -5
                    npc.rect.x += npc.speedx
            else:
                npc.speedx = 0
            for m in mobs:
                shoot_range = npc.rect.x - m.rect.x
                if shoot_range <= 25 and shoot_range >= -25:
                    npc.FireRocket()

    def FireRocket(self):
        n_bull = NPC_Bullet(self.rect.centerx, self.rect.top + 55)
        all_sprites.add(n_bull)
        npc_bullet.add(n_bull)

class Mob(pygame.sprite.Sprite):
    health = float
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (36, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(500, 550)
        self.speedy = random.randrange(1, 4)

    def Shoot(self):
        ene_bullet = EnemyBullet(self.rect.centerx + 15, self.rect.top + 30)
        all_sprites.add(ene_bullet)
        enemy_bullets.add(ene_bullet)

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(500, 550)
            self.speedy = random.randrange(2, 8)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (3, 25))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(rocket_img, (10, 25))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class NPC_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(npc_bullet_img, (3, 15))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Barrier(pygame.sprite.Sprite):
    health = float
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(barrier_img, (600, 75))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.top = 100

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.top = 0

#Load all game graphics
background = pygame.image.load("ground_img.png").convert()
background_rect = background.get_rect()
player_img = pygame.image.load("player.png").convert()
npc_img = pygame.image.load("npc.png").convert()
enemy_img = pygame.image.load("enemy.png").convert()
bullet_img = pygame.image.load("Mech1Shot.png").convert()
npc_bullet_img = pygame.image.load("npc_bullet.png").convert()
barrier_img = pygame.image.load("barrier.png").convert()
platform_img = pygame.image.load("platform.png").convert()
rocket_img = pygame.image.load("rocket.png").convert()

#Initialize the sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
rockets = pygame.sprite.Group()
npc_bullet = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
platform = Platform()
player = Player()
barrier = Barrier()
barrier.health = 100
all_sprites.add(platform)
all_sprites.add(player)
all_sprites.add(barrier)

for i in range(4):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    m.health = 100

score = 0
rocket_ammo = 15
troop_count = 0

#Game Intro
intro = True
running = False
controls = False

while intro == True and running == False and controls == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.fill(BLACK)
    draw_text(screen, str("MECH DEFENCE"), 52, 300, 10)
    mouse = pygame.mouse.get_pos()

    if 250+100 > mouse[0] and 350+50 > mouse[1] > 350:
        pygame.draw.rect(screen, GREEN, (250, 350, 100, 50))
    else:
        pygame.draw.rect(screen, BLUE, (250, 350, 100, 50))

    draw_text(screen, str("Start"), 36, 300, 365)

    draw_text(screen, str("Move left: left arrow or a"), 30, 300, 100)
    draw_text(screen, str("Move right: right arrow or d"), 30, 300, 125)
    draw_text(screen, str("Shoot left: j"), 30, 300, 150)
    draw_text(screen, str("Shoot right: l"), 30, 300, 175)
    draw_text(screen, str("Fire Rockets: k"), 30, 300, 200)
    draw_text(screen, str("Reload Rocket: r (cost $15)"), 30, 300, 225)
    draw_text(screen, str("Repair Barrier: h (cost $1 for each unit)"), 30, 300, 250)
    draw_text(screen, str("Call in reinforcements: m (cost $50)"), 30, 300, 275)

    if event.type == pygame.MOUSEBUTTONDOWN and 250+100 > mouse[0] and 350+50 > mouse[1] > 350:
        intro = False
        running = True
        controls = False

    pygame.display.update()
    clock.tick(15)

# Game loop
while running == True and intro == False and controls == False:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                player.ShootRight()
            if event.key == pygame.K_j:
                player.ShootLeft()
            if event.key == pygame.K_k and rocket_ammo >= 1:
                player.FireRocket()
                rocket_ammo -= 1
            if event.key == pygame.K_h and barrier.health != 100 and score >= 0:
                barrier.health += 1
                score -= 1
            if event.key == pygame.K_r and rocket_ammo <= 0 and score >= 15:
                rocket_ammo += 15
                score -= 15
            if event.key == pygame.K_m and score >= 50 and troop_count <= 1:
                troop_count += 1
                npc = NPC()
                all_sprites.add(npc)
                score -= 50

        if barrier.health <= 0:
            running = False
            barrier.kill()

    for m in mobs:
        if m.rect.top <= 200:
            m.speedy = 0
            m.Shoot()

    # Update
    all_sprites.update()

    #Check if bullet hits mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    #Check if rocket hits mob
    hits = pygame.sprite.groupcollide(mobs, rockets, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    #Check if npc bullet hits mob
    hits = pygame.sprite.groupcollide(mobs, npc_bullet, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    #Check if bullet hits barrier
    hits = pygame.sprite.spritecollide(barrier, enemy_bullets, False)
    if hits:
        barrier.health -= 1
        for bullet in enemy_bullets:
            bullet.kill()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    #Score Text
    draw_text(screen, str("$:"), 28, 25, 425)
    draw_text(screen, str(score), 28, 50, 425)
    # Health Text
    draw_text(screen, str("Health: "), 28, 50, 450)
    draw_text(screen, str(barrier.health), 28, 100, 450)
    #Rocket Ammo
    draw_text(screen, str("Rocket Ammo: "), 28, 500, 450)
    draw_text(screen, str(rocket_ammo), 28, 580, 450)
    # *after* drawing everything, flip the display
    pygame.display.flip()

if barrier.health <= 0:
    intro = True

pygame.quit()