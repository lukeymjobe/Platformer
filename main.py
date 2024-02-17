import pygame

pygame.init()
from pygame.locals import *
import random
from time import sleep, time

CLOCK = pygame.time.Clock()
running = True
WIDTH = 1600
HEIGHT = 900
vec = pygame.math.Vector2

background = pygame.transform.scale(pygame.image.load("desert.jpg"), (WIDTH, HEIGHT))


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pa_right = [pygame.transform.scale(pygame.image.load("pacmanc.png"), (50, 50)),
                         pygame.transform.scale(pygame.image.load("pacmano.png"), (50, 50))]
        self.pa_left = [pygame.transform.flip(self.pa_right[0], True, False),
                        pygame.transform.flip(self.pa_right[1], True, False)]

        self.image = self.pa_right[0]

        self.mouth_open = False
        self.direction = "LEFT"

        self.rect = self.pa_right[0].get_rect()

        self.rect.x = 400
        self.rect.y = 235

        self.ACC = 0.9
        self.FRIC = -0.12

        self.pos = vec((420, 235))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.double_jump = False
        self.triple_jump = False

    def update(self):
        self.acc = vec(0, 0.5)

        keypress = pygame.key.get_pressed()
        if keypress[K_d]:
            self.acc.x = self.ACC
            self.direction = "RIGHT"

        if keypress[K_a]:
            self.acc.x = -self.ACC
            self.direction = "LEFT"

        if self.mouth_open:
            if self.direction == "RIGHT":
                self.image = self.pa_right[1]
            if self.direction == "LEFT":
                self.image = self.pa_left[1]
        if not self.mouth_open:
            if self.direction == "RIGHT":
                self.image = self.pa_right[0]
            if self.direction == "LEFT":
                self.image = self.pa_left[0]

        # update position
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        # gravity
        hits = pygame.sprite.spritecollide(pacman, platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0

    def jump(self):
        hits = pygame.sprite.spritecollide(pacman, platforms, False)
        if hits:
            self.vel.y = -15
            self.double_jump = False
            self.triple_jump = False
        if not hits:
            if not self.double_jump:
                self.vel.y = -15
                self.double_jump = True
                self.triple_jump = False
            elif self.double_jump and not self.triple_jump:
                self.vel.y = -15
                self.triple_jump = True
                self.double_jump = True

    def render(self):
        DISPLAY.blit(self.image, self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
        self.rect.x, self.rect.y = x, y
        self.active = True

    def update(self):
        temp = pygame.sprite.Group()
        temp.add(self)

        if pygame.Rect.colliderect(pacman.rect, self.rect) and pygame.sprite.spritecollide(penguin, temp,
                                                                                           False) and len(
                platforms.sprites()) > 2:
            self.active = False
            platforms.remove(self)

            # randomly pick another platform to move penguin to
            index = random.randint(0, len(platforms.sprites()) - 2)
            newPlatform = platforms.sprites()[index]
            penguin.pos = vec((newPlatform.rect.x + (newPlatform.width / 2), newPlatform.rect.y - 30))

            penguin.left_boundary = newPlatform.rect.x
            penguin.right_boundary = (newPlatform.rect.x + newPlatform.width) - 100

        if pygame.Rect.colliderect(pacman.rect, self.rect):
            keypress = pygame.key.get_pressed()
            if keypress[K_s] and pacman.double_jump:
                platforms.remove(self)

    def render(self):
        DISPLAY.blit(self.surf, self.rect)


class Penguin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walking_images_r = []
        self.walking_images_l = []

        self.dying_images = []

        self.walking_index = 0
        self.dying_index = 0

        self.gun_out = False

        self.gun = pygame.transform.scale(pygame.transform.flip(pygame.image.load("gun.png"), True, False), (50, 50))
        # add walking images to walking list
        for i in range(4):
            img = pygame.image.load("Penguin/Walk/walk{}.png".format(i))
            self.walking_images_r.append(pygame.transform.scale(img, (100, 50)))

        for i in range(4):
            img = pygame.image.load("Penguin/Die/die{}.png".format(i))
            self.dying_images.append(pygame.transform.scale(img, (100, 50)))

        for image in self.walking_images_r:
            img_with_flip = pygame.transform.flip(image, True, False)
            self.walking_images_l.append(img_with_flip)

        self.ACC = 0.2
        self.FRIC = -0.12

        self.pos = vec((220, 235))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.direction = "RIGHT"

        self.image = self.walking_images_r[self.walking_index]
        self.rect = self.image.get_rect()

        self.left_boundary = 300
        self.right_boundary = 500

    def update(self):
        self.acc = vec(0, 0.5)

        if self.rect.x <= self.left_boundary:
            self.direction = "RIGHT"
        if self.rect.x >= self.right_boundary:
            self.direction = "LEFT"

        if self.direction == "RIGHT":
            self.acc.x = self.ACC
        else:
            self.acc.x = -self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        # update frames
        if self.direction == "RIGHT":
            self.image = self.walking_images_r[self.walking_index]
        else:
            self.image = self.walking_images_l[self.walking_index]

        # gravity
        hits = pygame.sprite.spritecollide(penguin, platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0

    def render(self):
        DISPLAY.blit(self.image, self.rect)


DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

pacman = Pacman()
penguin = Penguin()

platform = Platform(300, 400, 600, 20)
platform1 = Platform(400, 300, 870, 20)
platform2 = Platform(600, 500, 460, 20)
platform3 = Platform(800, 200, 740, 20)
platform4 = Platform(75, 200, 480, 20)
platform5 = Platform(900, 66, 740, 20)
platform6 = Platform(400, 500, 740, 20)

ground = Platform(0, HEIGHT, WIDTH, 20)

platforms = pygame.sprite.Group()

platforms.add(platform)
platforms.add(platform1)
platforms.add(platform2)
platforms.add(platform3)
platforms.add(platform4)
platforms.add(platform5)
platforms.add(platform6)
platforms.add(ground)

while running:
    CLOCK.tick(60)
    DISPLAY.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pacman.jump()
            if event.key == pygame.K_o:
                if pacman.mouth_open:
                    pacman.mouth_open = False
                else:
                    pacman.mouth_open = True

    pacman.update()
    pacman.render()

    penguin.update()
    penguin.render()

    for i in platforms:
        i.update()

    for i in platforms:
        i.render()

    pygame.display.update()

print('game over')
