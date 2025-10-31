import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from Utils import *
vec = pg.math.Vector2

# the sprite module contains every sprite and being able to test different modules
# includes: player, mob a moving object

# makes Player a sprite
class Player1(Sprite): # superclass
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(HITSIZE)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.music_cd = Cooldown(1250)
        self.music_loop_fix = True
        self.mode = GAMEMODE
        self.hit_note = False
        self.restart = False
        self.restart_exists = False
        self.music = True
        self.music_wait = True
        self.notes = 0
        self.score = 0
        self.health = 1000
        self.quit_wait = False
        self.perfects_hit = 0
        self.greats_hit = 0
        self.misses_hit = 0
        self.P = "Perfect:"
        self.G = "Great:"
        self.M = "Miss:"
        self.H = "Health:"
        self.S = "Score:"

    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()

    def update(self):

        self.get_keys()

        self.pos += self.vel
        # small positioning so it is centered
        self.rect.x = self.pos.x-5
        self.rect.y = self.pos.y-5

        if self.health > 1000:
            self.health = 1000
        if self.health < 0:
            self.health = 0

class Player2(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(HITSIZE)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]

    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()

    def update(self):

        self.get_keys()

        self.pos += self.vel

        self.rect.x = self.pos.x-5

        self.rect.y = self.pos.y-5

class Player3(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(HITSIZE)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]

    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()

    def update(self):

        self.get_keys()

        self.pos += self.vel

        self.rect.x = self.pos.x-5

        self.rect.y = self.pos.y-5

class Player4(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(HITSIZE)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]

    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()

    def update(self):

        self.get_keys()

        self.pos += self.vel

        self.rect.x = self.pos.x-5

        self.rect.y = self.pos.y-5

# makes Mob a sprite
class Note(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_notes
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(NOTESIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = NOTESPEED
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]

    def update(self):
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.game.player1.health == 0 and self.game.player1.mode == 1:
            self.vel.y = 0
        else:
            self.vel.y = -self.speed*self.game.dt

class Restart(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_restarts
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(RESTARTSIZE)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]

    def update(self):
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.pos.x = 1200
        self.pos.y = 200

class Mouse(Sprite): #  adds a mouse sprite used for clicking hitboxes
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mouses
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(MOUSESIZE)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.kill_cd = Cooldown(50)
        self.wait = False
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]

    def collide_with_stuff(self, group, kill): # checks for collisions with "Restart"
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Restart":
                # tells code in main.py in update to spawn the restart button
                self.game.player1.restart = True

    def update(self):
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        mouse_pos = pg.mouse.get_pos() # gets mouse position in a (x, y) way
        self.pos.x = mouse_pos[0] - MOUSESIZE[0] / 2
        self.pos.y = mouse_pos[1] - MOUSESIZE[1] / 2

        # kills sprite after a certain amount of time after it is called to spawn

        if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.kill_cd.ready():
            self.kill()
            self.wait = False

        self.collide_with_stuff(self.game.all_restarts, True)

class PERFECT(Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self.groups = game.all_sprites, game.all_perfects
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(PERFECTSIZE)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.type = type
        self.kill_cd = Cooldown(35)
        self.wait = False

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        # checks collisions with note sprite
        if hits:
            if str(hits[0].__class__.__name__) == "Note":
                print("Note hit PERFECT")
                self.game.player1.score += 1000
                self.game.player1.perfects_hit += 1
                self.game.player1.notes -= 1
                if self.game.player1.health < 1000:
                    self.game.player1.health += 20

    def update(self):
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # different types of notes so we can differentiate which player it should spawn on
        # also waits to kill after a certain amount of time

        if self.type == "1":
            self.pos.x = self.game.player1.pos.x-5
            self.pos.y = self.game.player1.pos.y
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()
        
        if self.type == "2":
            self.pos.x = self.game.player2.pos.x-5
            self.pos.y = self.game.player2.pos.y
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.type == "3":
            self.pos.x = self.game.player3.pos.x-5
            self.pos.y = self.game.player3.pos.y
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.type == "4":
            self.pos.x = self.game.player4.pos.x-5
            self.pos.y = self.game.player4.pos.y
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.kill_cd.ready():
            self.kill()
            self.wait = False

        self.collide_with_stuff(self.game.all_notes, True)

class GREAT(Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self.groups = game.all_sprites, game.all_greats
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(GREATSIZE)
        self.image.fill(DARK_GREY)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.type = type
        self.kill_cd = Cooldown(35)
        self.wait = False

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
                # checks collisions with note sprite
            if str(hits[0].__class__.__name__) == "Note":
                print("Note hit GREAT")
                self.game.player1.score += 500
                self.game.player1.greats_hit += 1
                self.game.player1.notes -= 1
                if self.game.player1.health < 1000:
                    self.game.player1.health += 10

    def update(self):
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # different types of notes so we can differentiate which player it should spawn on
        # also waits to kill after a certain amount of time

        if self.type == "1":
            self.pos.x = self.game.player1.pos.x-5
            self.pos.y = self.game.player1.pos.y-15
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()
        
        if self.type == "2":
            self.pos.x = self.game.player2.pos.x-5
            self.pos.y = self.game.player2.pos.y-15
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.type == "3":
            self.pos.x = self.game.player3.pos.x-5
            self.pos.y = self.game.player3.pos.y-15
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.type == "4":
            self.pos.x = self.game.player4.pos.x-5
            self.pos.y = self.game.player4.pos.y-15
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.type == "11":
            self.pos.x = self.game.player1.pos.x-5
            self.pos.y = self.game.player1.pos.y+30
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()
        
        if self.type == "22":
            self.pos.x = self.game.player2.pos.x-5
            self.pos.y = self.game.player2.pos.y+30
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.type == "33":
            self.pos.x = self.game.player3.pos.x-5
            self.pos.y = self.game.player3.pos.y+30
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.type == "44":
            self.pos.x = self.game.player4.pos.x-5
            self.pos.y = self.game.player4.pos.y+30
            if self.wait == False:
                self.wait = True
                self.kill_cd.start()

        if self.kill_cd.ready():
            self.kill()
            self.wait = False

        self.collide_with_stuff(self.game.all_notes, True)

class Miss(Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self.groups = game.all_sprites, game.all_misses
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(MISSSIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.type = type

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Note":
                print("Note hit Miss")
                self.game.player1.score -= 500
                self.game.player1.misses_hit += 1
                self.game.player1.notes -= 1
                if self.game.player1.health > 0:
                    self.game.player1.health -= 50

    def update(self):
        self.pos += self.vel

        if self.type == "1":
            self.rect.x = self.game.player1.pos.x-5
            self.rect.y = self.game.player1.pos.y-158

        if self.type == "2":
            self.rect.x = self.game.player2.pos.x-5
            self.rect.y = self.game.player2.pos.y-157

        if self.type == "3":
            self.rect.x = self.game.player3.pos.x-5
            self.rect.y = self.game.player3.pos.y-156

        if self.type == "4":
            self.rect.x = self.game.player4.pos.x-5
            self.rect.y = self.game.player4.pos.y-155
        
        self.collide_with_stuff(self.game.all_notes, True)




            

