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
        self.hit_platform = False

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

        if self.velocity > 9.5:
            self.velocity = 9.5

        # if self.rect.y >= 600 - self.frame.get_height():
        #     self.velocity = 0
        #     self.jumping = False


        self.hit_platform = False
        for i in platforms:
            if pygame.Rect.colliderect(self.rect, i.rect):
                self.velocity = 0
                self.hit_platform = True
                break
        if not self.hit_platform:
            if self.rect.y >= 600 - self.frame.get_height():
                self.velocity = 0
                self.jumping = False
            else:
                self.velocity += 0.5






            # elif self.rect.y >= 600 - self.frame.get_height():
            #     self.velocity = 0
            # else:
            #     self.velocity += 0.5

        # if self.rect.y >= 600 - self.frame.get_height():
        #     self.velocity = 0
        #
        #     for i in platforms:
        #         if pygame.Rect.colliderect(self.rect, i.rect):
        #             self.velocity = 0
        # else:
        #     self.velocity += 0.5

        # for i in platforms:
        # self.rect.y -= 84
        # if pygame.Rect.colliderect(self.rect, i.rect):
        # self.velocity = 0
        # self.jumping = False
        # self.rect.y += 84

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
        if self.hit_platform:
            self.rect.y += 75
            DISPLAY.blit(self.frame, self.rect)
            self.rect.y -= 75
        else:
            DISPLAY.blit(self.frame, self.rect)

        if self.gun_out:
            self.rect.x += 75
            DISPLAY.blit(self.gun, self.rect)
            self.rect.x -= 75


class PlayerBullets:
    def __init__(self):
        self.bullets = []
        img = pygame.image.load("tom.png")
        self.tom = pygame.transform.scale(img, (img.get_width() / 10, img.get_height() / 10))

    def fire(self):
        pygame.mixer.music.load('blast.mp3')
        pygame.mixer.music.play(1)
        self.bullets.append([character.rect.x + 75, character.rect.y])

    def update(self):
        for i in self.bullets:
            i[0] += 10

        for i in self.bullets:
            if i[0] > DISPLAY.get_width():
                self.bullets.remove(i)

        # collision with tomatoes
        for i in self.bullets:
            # make rectangle of a tomato
            tempTomRect = self.tom.get_rect()
            # set its coordinates to the x and y stored in the i list
            tempTomRect.x = i[0]
            tempTomRect.y = i[1]
            # check if that rectangle is colliding with the rectangle of pacman
            if pygame.Rect.colliderect(tempTomRect, pacman.pr):
                if pacman.mouth_open:
                    if pacman.image == pacman.pa_left[1]:
                        self.bullets.remove(i)
                        pygame.mixer.music.load('chomp.mp3')
                        pygame.mixer.music.play(1)
                # if pacman.mouth_open:

    def render(self):
        for i in self.bullets:
            DISPLAY.blit(self.tom, (i[0], i[1]))


class Pacman:
    def __init__(self):
        self.pa_right = [pygame.transform.scale(pygame.image.load("pacmanc.png"), (50, 50)),
                         pygame.transform.scale(pygame.image.load("pacmano.png"), (50, 50))]
        self.pa_left = [pygame.transform.flip(self.pa_right[0], True, False),
                        pygame.transform.flip(self.pa_right[1], True, False)]

        self.image = self.pa_right[0]
        self.mouth_open = False

        self.pr = self.pa_right[0].get_rect()

        self.pr.x = 375
        self.pr.y = 235

        self.velocity = 0

    def update(self):
        keypress = pygame.key.get_pressed()
        # if keypress[K_w]:
        #     if self.mouth_open:
        #         self.mouth_open = False
        #     elif not self.mouth_open:
        #         self.mouth_open = True

        if self.velocity > 9.5:
            self.velocity = 9.5

        self.pr.y += self.velocity

        # reset gravity if contact with ground

        # reset gravity if contact with platforms
        for i in platforms:
            if pygame.Rect.colliderect(self.pr, i.rect):
                self.velocity = 0
            elif self.pr.y >= 600 - self.image.get_height():
                self.velocity = 0
            else:
                self.velocity += 0.5

        self.pr.y += self.velocity

        if keypress[K_d]:
            self.pr.x += 5
            if self.mouth_open == True:
                self.image = self.pa_right[1]
            else:
                self.image = self.pa_right[0]

        if keypress[K_a]:
            self.pr.x -= 5
            if self.mouth_open == True:
                self.image = self.pa_left[1]
            else:
                self.image = self.pa_left[0]

        # if keypress[K_w]:
        #     self.pr.y -= 5
        # if keypress[K_s]:
        #     self.pr.y += 5





    def render(self):
        DISPLAY.blit(self.image, self.pr)


DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
character = Character()

playerBullets = PlayerBullets()

pacman = Pacman()

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
                    pygame.mixer.music.load('unholster.mp3')
                    pygame.mixer.music.play(1)
            if event.key == pygame.K_DOWN:
                if character.gun_out:
                    playerBullets.fire()
            if event.key == pygame.K_s:
                if pacman.mouth_open:
                    pacman.mouth_open = False

                elif not pacman.mouth_open:
                    pacman.mouth_open = True

            if event.key == pygame.K_w:
                pacman.velocity -= 50

    character.move()
    character.update()
    character.render()

    pacman.render()
    pacman.update()

    for i in platforms:
        i.render()

    platform_materializer()

    # print(character.walking_images[1].get_height())
    # print(character.walking_images[1].get_width())

    playerBullets.update()
    playerBullets.render()

    pygame.display.update()

print('game over')
