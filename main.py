import pygame

pygame.init()
from pygame.locals import *
from time import sleep, time

CLOCK = pygame.time.Clock()
running = True
WIDTH = 1200
HEIGHT = 600
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

        self.rect = self.pa_right[0].get_rect()

        self.rect.x = 400
        self.rect.y = 235

        self.ACC = 0.5
        self.FRIC = -0.12

        self.pos = vec((420, 235))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0.5)

        keypress = pygame.key.get_pressed()
        if keypress[K_d]:
            self.acc.x = self.ACC
            if self.mouth_open:
                self.image = self.pa_right[1]
            else:
                self.image = self.pa_right[0]

        if keypress[K_a]:
            self.acc.x = -self.ACC
            if self.mouth_open:
                self.image = self.pa_left[1]
            else:
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

    def render(self):
        DISPLAY.blit(self.image, self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
        self.rect.x, self.rect.y = x, y

    def render(self):
        DISPLAY.blit(self.surf, self.rect)


DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

pacman = Pacman()

platform = Platform(200, 400, 100, 20)
platform1 = Platform(400, 300, 100, 20)
platform2 = Platform(600, 500, 100, 20)
platform3 = Platform(800, 200, 100, 20)
ground = Platform(0, 580, 1200, 20)

platforms = pygame.sprite.Group()

platforms.add(platform)
platforms.add(platform1)
platforms.add(platform2)
platforms.add(platform3)
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

    pacman.render()
    pacman.update()

    for i in platforms:
        i.render()

    pygame.display.update()

print('game over')
