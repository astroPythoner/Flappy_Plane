import pygame
from constants import *
import random
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, color):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.color = color
        self.last_image_num = 0
        self.image = pygame.transform.scale(player_images["plane{}1.png".format(self.color)],(88,73))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 4, HEIGHT / 2)
        self.pos = vec(WIDTH / 4, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        if not self.game.in_end_expl and self.game.game_status == None:
            self.acc = vec(0, PLAYER_GRAV)

            # Jump
            if self.game.check_key_pressed(JUMP):
                self.vel.y = -10

            # equations of motion
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            self.rect.center = self.pos

            # new image
            this_turns_image_num = int(str(pygame.time.get_ticks())[:-1])%3
            if self.last_image_num != this_turns_image_num:
                self.image = pygame.transform.scale(player_images["plane{}{}.png".format(self.color,this_turns_image_num+1)], (88, 73))
                self.last_image_num = this_turns_image_num

class Rock(pygame.sprite.Sprite):
    def __init__(self, game, top_or_button = FROM_BUTTON, höhe = 0, type = GEGENUEBER, color = None, start_x = WIDTH):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.top_or_button = top_or_button
        if höhe == 0:
            self.height = int(random.randrange(int(60 + HEIGHT / 3), int(HEIGHT - 60 - HEIGHT / 3)))
        else:
            self.height = int(höhe)
        self.type = type
        self.color = color
        self.start_x = start_x
        self.reset_image_rect_pos()

    def update(self):
        if not self.game.in_end_expl and self.game.game_status == None:
            self.rect.x -= self.game.speed

            if self.type == FALLEND:
                if self.rect.x < WIDTH/2 + 50:
                    self.rect.y += 15

            if self.rect.right < 0:
                self.kill()

    def reset_image_rect_pos(self):
        if self.top_or_button == FROM_BUTTON:
            self.image = pygame.transform.scale(rock_images["rock{}.png".format(self.color)], (108, self.height))
            self.rect = self.image.get_rect()
            if self.type == ZENTRAL:
                self.rect.bottomleft = (self.start_x, HEIGHT/2)
            else:
                self.rect.bottomleft = (self.start_x, HEIGHT)
            new_rock = None
            if self.type == GEGENUEBER or self.type == KURVE:
                if int(HEIGHT - self.height - HEIGHT / 3) > 70:
                    new_rock = OppositeRock(self.game, FROM_TOP, int(HEIGHT - self.height - HEIGHT/3), self.type, self.color, self.start_x)
            if self.type == TUNNEL:
                new_rock = OppositeRock(self.game, FROM_TOP, self.height, self.type, self.color, self.start_x)
            if self.type == VERSETZT:
                new_rock = OppositeRock(self.game, FROM_TOP, self.height, self.type, self.color, self.start_x + random.randrange(300,400))
            if self.type == ZENTRAL:
                new_rock = OppositeRock(self.game, FROM_TOP, self.height, self.type, self.color, self.start_x)
            if new_rock != None:
                self.game.all_sprites.add(new_rock)
                self.game.rocks.add(new_rock)
        elif self.top_or_button == FROM_TOP:
            self.image = pygame.transform.scale(rock_images["rock{}Down.png".format(self.color)], (108, self.height))
            self.rect = self.image.get_rect()
            if self.type == ZENTRAL:
                self.rect.topleft = (self.start_x, HEIGHT/2)
            else:
                self.rect.topleft = (self.start_x, 0)
            new_rock = None
            if self.type == GEGENUEBER or self.type == KURVE:
                if int(HEIGHT - self.height - HEIGHT / 3) > 70:
                    new_rock = OppositeRock(self.game, FROM_BUTTON, int(HEIGHT - self.height - HEIGHT / 3), self.type, self.color, self.start_x)
            if self.type == TUNNEL:
                new_rock = OppositeRock(self.game, FROM_BUTTON, self.height, self.type, self.color, self.start_x)
            if self.type == VERSETZT:
                new_rock = OppositeRock(self.game, FROM_BUTTON, self.height, self.type, self.color, self.start_x + random.randrange(150, 400))
            if self.type == ZENTRAL:
                new_rock = OppositeRock(self.game, FROM_TOP, self.height, self.type, self.color, self.start_x)
            if new_rock != None:
                self.game.all_sprites.add(new_rock)
                self.game.rocks.add(new_rock)

class OppositeRock(pygame.sprite.Sprite):
    def __init__(self,game, top_or_button = FROM_BUTTON, höhe = 0, type = GEGENUEBER, color = None, start_x = WIDTH):
        self.game = game
        self.color = color
        pygame.sprite.Sprite.__init__(self)
        self.top_or_button = top_or_button
        if self.top_or_button == FROM_BUTTON:
            self.image = pygame.transform.scale(rock_images["rock{}.png".format(self.color)],(108,höhe))
            self.rect = self.image.get_rect()
            if type == ZENTRAL:
                self.rect.bottomleft = (start_x, HEIGHT/2)
            else:
                self.rect.bottomleft = (start_x, HEIGHT)
        elif self.top_or_button == FROM_TOP:
            self.image = pygame.transform.scale(rock_images["rock{}Down.png".format(self.color)],(108,höhe))
            self.rect = self.image.get_rect()
            if type == ZENTRAL:
                self.rect.topleft = (start_x, HEIGHT/2)
            else:
                self.rect.topleft = (start_x, 0)

    def update(self):
        if not self.game.in_end_expl and self.game.game_status == None:
            self.rect.x -= self.game.speed

            if self.rect.right < 0:
                self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, top_or_button, place_second = True, x_pos = 0, color = None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.color = color
        self.top_or_button = top_or_button
        if self.top_or_button == FROM_BUTTON:
            self.image = pygame.transform.scale(ground_images["ground{}.png".format(self.color)],(WIDTH,71))
            self.rect = self.image.get_rect()
            self.rect.midbottom = (x_pos, HEIGHT)

        elif self.top_or_button == FROM_TOP:
            self.image = pygame.transform.scale(ground_images["ground{}Down.png".format(self.color)],(WIDTH,71))
            self.rect = self.image.get_rect()
            self.rect.midtop = (x_pos, 0)
        if place_second:
            new_ground = Ground(self.game,self.top_or_button, False, WIDTH, self.color)
            self.game.all_sprites.add(new_ground)
            self.game.rocks.add(new_ground)

    def update(self):
        if not self.game.in_end_expl and self.game.game_status == None:
            self.rect.x -= self.game.speed

            if self.rect.right < 0:
                self.rect.left = WIDTH + self.rect.right

class Explosion(pygame.sprite.Sprite):
    # Explosionen in unterschiedlichen Größen
    def __init__(self, game, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # Größe der Explosion
        self.size = size
        # Bilder ja nach Größe holen
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        # In welchem BIld der Explosion bin ich
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        # Schnelligkeit der Explosion
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            # nächstes Bilde der Explosion anzeigen
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center