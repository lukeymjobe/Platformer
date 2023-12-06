import pygame

pygame.init()
from pygame.locals import *
from time import sleep, time

CLOCK = pygame.time.Clock()
running = True
WIDTH = 1200
HEIGHT = 600

background = pygame.transform.scale(pygame.image.load("desert.jpg"), (WIDTH, HEIGHT))

class Platforms:
    def __init__(self):
        self.platform = pygame.transform.scale(pygame.image.load("platform.png"),(100,100))

        self.rect = self.platform.get_rect()
        #self.rect.y = HEIGHT-self.rect.get_height()
        self.rect.x = 100
    def render(self):
        DISPLAY.blit(self.platform, self.rect)
class Character:
    def __init__(self):
        self.walking_images = []
        self.jumping_images = []
        self.dying_images = []

        self.walking_index = 0
        self.jumping_index = 0
        self.dying_index = 0

        # add walking images to walking list
        for i in range(4):
            img = pygame.image.load("Penguin/Walk/walk{}.png".format(i))
            self.walking_images.append(pygame.transform.scale(img, (150, 150)))

        for i in range(3):
            img = pygame.image.load("Penguin/Jump/jump{}.png".format(i))
            self.jumping_images.append(pygame.transform.scale(img, (150, 150)))

        for i in range(4):
            img = pygame.image.load("Penguin/Die/die{}.png".format(i))
            self.dying_images.append(pygame.transform.scale(img, (150, 150)))

        # create rect and set frame
        self.rect = self.walking_images[0].get_rect()
        self.frame = self.walking_images[0]

        self.rect.x = 0
        self.rect.y = 0

        # motion variables
        self.velocity = 0
        self.jumping = False

        # animation delay
        self.last_time = pygame.time.get_ticks()
        self.delay = 100
        self.jump_time = pygame.time.get_ticks()
        self.die_time = pygame.time.get_ticks()

    def update(self):
        # update animation
        if self.walking_index > 3:
            self.walking_index = 0

        if self.jumping_index > 2:
            self.jumping_index = 0

        if self.jumping:
            self.frame = self.jumping_images[self.jumping_index]
            # self.jumping_index += 1
            if pygame.time.get_ticks() - self.jump_time > self.delay:
                self.jumping_index += 1
                self.jump_time = pygame.time.get_ticks()

        if not self.jumping:
            self.frame = self.walking_images[self.walking_index]

        # update gravity
        self.velocity += 0.5
        if self.velocity > 9.5:
            self.velocity = 9.5

        if self.rect.y >= 600 - self.frame.get_height():
            self.velocity = 0
            self.jumping = False

        self.rect.y += self.velocity

    def move(self):
        # check for keyboard and move player
        keypress = pygame.key.get_pressed()
        if keypress[K_RIGHT]:
            self.rect.x += 10
            # update animation
            if pygame.time.get_ticks() - self.last_time > self.delay:
                self.walking_index += 1
                self.last_time = pygame.time.get_ticks()
        keypress = pygame.key.get_pressed()
        if keypress[K_LEFT]:
            self.rect.x -= 10
            # Update Animation
            if pygame.time.get_ticks() - self.last_time > self.delay:
                self.walking_index += 1
                self.last_time = pygame.time.get_ticks()
        keypress = pygame.key.get_pressed()

    def jump(self):
        if not self.jumping:
            self.rect.y -= 200
            self.jumping = True

    def render(self):
        DISPLAY.blit(self.frame, self.rect)


DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
character = Character()
platforms = Platforms()

while running:
    CLOCK.tick(60)
    DISPLAY.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                character.jump()

    character.move()
    character.update()
    character.render()

    platforms.render()

    pygame.display.update()

print('game over')
