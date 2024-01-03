import pygame

pygame.init()
from pygame.locals import *
from time import sleep, time

CLOCK = pygame.time.Clock()
running = True
WIDTH = 1200
HEIGHT = 600

background = pygame.transform.scale(pygame.image.load("desert.jpg"), (WIDTH, HEIGHT))


class Platform:
    def __init__(self, x, y):
        self.platform = pygame.transform.scale(pygame.image.load("platform.png"), (200, 200))
        self.rect = self.platform.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

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

        self.gun_out = False

        self.gun = pygame.transform.scale(pygame.transform.flip(pygame.image.load("gun.png"), True, False), (50, 50))
        # add walking images to walking list
        for i in range(4):
            img = pygame.image.load("Penguin/Walk/walk{}.png".format(i))
            self.walking_images.append(pygame.transform.scale(img, (100, 50)))

        for i in range(3):
            img = pygame.image.load("Penguin/Jump/jump{}.png".format(i))
            self.jumping_images.append(pygame.transform.scale(img, (100, 50)))

        for i in range(4):
            img = pygame.image.load("Penguin/Die/die{}.png".format(i))
            self.dying_images.append(pygame.transform.scale(img, (100, 50)))

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

        for i in platforms:
            self.rect.y -= 84
            if pygame.Rect.colliderect(self.rect, i.rect):
                self.velocity = 0
                self.jumping = False
            self.rect.y += 84

        self.rect.y += self.velocity

    def move(self):
        # check for keyboard and move player
        keypress = pygame.key.get_pressed()
        # if keypress[K_SPACE]:
        #     self.gun_out = True
        if not self.gun_out:
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

    def jump(self):
        if not self.jumping:
            self.rect.y -= 350
            self.jumping = True

    def render(self):
        DISPLAY.blit(self.frame, self.rect)
        if self.gun_out:
            self.rect.x += 75
            DISPLAY.blit(self.gun, self.rect)
            self.rect.x -= 75


class PlayerBullets:
    def __init__(self):
        self.bullets = []
        keypress = pygame.key.get_pressed()

    def fire(self):
        self.bullets.append([character.rect.x + 75, character.rect.y])


DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
character = Character()

playerBullets = PlayerBullets()

platform = Platform(200, 400)
platform1 = Platform(400, 300)
platform2 = Platform(600, 500)
platform3 = Platform(800, 200)

platforms = []

platforms.append(platform)
platforms.append(platform1)
platforms.append(platform2)
platforms.append(platform3)


def platform_materializer():
    if character.rect.y >= 600 - character.frame.get_height():
        character.velocity = 0
        character.jumping = False

    for i in platforms:
        if pygame.Rect.colliderect(character.rect, i.rect):
            character.velocity = 0
            character.jumping = False
        # if not pygame.Rect.colliderect(character.rect, i.rect):
        # character.velocity


while running:
    CLOCK.tick(60)
    DISPLAY.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character.jump()
            if event.key == pygame.K_SPACE:
                if character.gun_out:
                    character.gun_out = False
                elif not character.gun_out:
                    character.gun_out = True
            if event.key == pygame.K_DOWN:
                playerBullets.fire()
    character.move()
    character.update()
    character.render()

    for i in platforms:
        i.render()

    platform_materializer()

    # print(character.walking_images[1].get_height())
    # print(character.walking_images[1].get_width())

    pygame.display.update()

print('game over')
