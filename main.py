 # Created by Aldric Shi with the help of ChatGPT
# import necessary modules
# core game loop
# input
# update
# draw

# yay i can use github from VS CODE! :D

import math # imports everything we need to write the code
import random
import sys
import time
from random import randint
import pygame as pg
from pygame import mixer
# importing everything from other .py files
from settings import *
from sprites import *
from os import path
from Utils import *

class Game: # creates class named Game that includes the below indented lines
   def __init__(self):
      pg.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Project Funkin'")
      self.playing = True

   # sets up a game folder directory path using the current folder containing THIS file
   # loads data from level1.txt so the Game class has a map property that uses the map class to parse the level1.txt file
   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.map = Map(path.join(self.game_folder, LEVEL1))
      # takes level1.txt and puts it into a list that we can use later

   def new(self):
      self.load_data()
      self.all_sprites = pg.sprite.Group() # allows us to update and draw sprites in grouped batches
      # creates all sprite groups
      self.all_notes = pg.sprite.Group()
      self.all_players = pg.sprite.Group()
      self.all_perfects = pg.sprite.Group()
      self.all_misses = pg.sprite.Group()
      self.all_greats = pg.sprite.Group()
      self.all_restarts = pg.sprite.Group()
      self.all_mouses = pg.sprite.Group()

      for row, tiles, in enumerate(self.map.data):
         for col, tile, in enumerate(tiles): # from self.map checks if something meets the selected number/letter
            # if it meets the selected number/letter it will in that place put the selected sprite
            if tile == 'N':
               Note(self, col, row)
               self.player1.notes += 1
            elif tile == '1':
               self.player1 = Player1(self, col, row)
               global numbertypemiss
               numbertypemiss = "1"
               Miss(self, -999, -999, numbertypemiss)
            elif tile == '2':
               self.player2 = Player2(self, col, row)
               numbertypemiss = "2"
               Miss(self, -999, -999, numbertypemiss)
            elif tile == '3':
               self.player3 = Player3(self, col, row)
               numbertypemiss = "3"
               Miss(self, -999, -999, numbertypemiss)
            elif tile == '4':
               self.player4 = Player4(self, col, row)
               numbertypemiss = "4"
               Miss(self, -999, -999, numbertypemiss)
                   
      self.all_sprites.add(self.all_notes)
      self.all_sprites.add(self.player1)
      self.all_sprites.add(self.player2)
      self.all_sprites.add(self.player3)
      self.all_sprites.add(self.player4)
      self.all_sprites.add(self.all_perfects)
      self.all_sprites.add(self.all_misses)
      self.all_sprites.add(self.all_greats)
      self.all_sprites.add(self.all_restarts)
      self.all_sprites.add(self.all_mouses)

   def run(self):
      while self.playing == True:
         # self.dt used for time
         self.dt = self.clock.tick(FPS) / 1000
         # input
         self.events()
         # process
         self.update()
         # output
         self.draw()
      pg.quit()
        

   def update(self):
      # restarts the game when restart button gets clicked
      if self.player1.restart == True:
         self.player1.restart = False
         self.player1.restart_exists == False
         self.player1.music = True
         self.player1.music_loop_fix = True
         self.playing = False
         g = Game()
         g.new()
         g.run()
      if self.player1.notes == 0 and self.player1.mode == 1 or self.player1.health == 0 and self.player1.mode == 1:
         if self.player1.restart_exists == False:
            # when notes do not exists or when you die summons restart and stops music
            Restart(self, -999, -999)
            self.player1.music = False
            self.player1.restart_exists = True
            mixer.music.stop()
      #  starts a cooldown so music playing gets delayed
      if self.player1.music == True:
         self.player1.music_cd.start()
         self.player1.music = False
      
      if self.player1.music_cd.ready() and self.player1.music_loop_fix == True:
         # loads a mp3 and plays it
         mixer.init()

         mixer.music.load("sound/Music_1.mp3")

         mixer.music.set_volume(0.7)

         mixer.music.play()

         self.player1.music_loop_fix = False



      self.all_sprites.update()
   # makes a draw text function to be used later
   def draw_text(self, surface, text, size, color, x, y):
      font_name = pg.font.match_font('arial')
      font = pg.font.Font(font_name, size)
      text_surface = font.render(text, True, color)
      text_rect = text_surface.get_rect()
      text_rect.midtop = (x,y)
      surface.blit(text_surface, text_rect)
      
   def draw(self):
      self.screen.fill(BLACK)
      self.draw_text(self.screen, str(self.player1.score), 24, WHITE, 160, 40)
      self.draw_text(self.screen, str(self.player1.S), 24, WHITE, 100, 40)

      self.draw_text(self.screen, str(self.player1.perfects_hit), 24, WHITE, 1045, 300)
      self.draw_text(self.screen, str(self.player1.P), 24, WHITE, 1000, 300)

      self.draw_text(self.screen, str(self.player1.greats_hit), 24, WHITE, 1045, 340)
      self.draw_text(self.screen, str(self.player1.G), 24, WHITE, 1000, 340)

      self.draw_text(self.screen, str(self.player1.misses_hit), 24, WHITE, 1045, 380)
      self.draw_text(self.screen, str(self.player1.M), 24, WHITE, 1000, 380)

      self.draw_text(self.screen, str(self.player1.combo), 24, WHITE, 1045, 420)
      self.draw_text(self.screen, str(self.player1.C), 24, WHITE, 1000, 420)

      self.draw_text(self.screen, str(self.player1.health), 24, WHITE, 1345, 40)
      self.draw_text(self.screen, str(self.player1.H), 24, WHITE, 1280, 40)
      
      self.all_sprites.draw(self.screen)
      pg.display.flip()
   
   def events(self):
      keys = pg.key.get_pressed()
      for event in pg.event.get():
         if event.type == pg.QUIT: # checks if you try to quit the game
            print("this is happening")
            self.playing = False
         if event.type == pg.MOUSEBUTTONDOWN:
            Mouse(self, -999, -999)
         global numbertypeperfect
         global numbertypegreat
         if self.player1.health == 0 and self.player1.mode == 1 or self.player1.restart == True:
            pass
         else:
            #  when a key is clicked it will spawn a sprite
            if keys[pg.K_a]:
               numbertypeperfect = "1"
               PERFECT(self, -999, -999, numbertypeperfect)
               numbertypegreat = "1"
               GREAT(self, -999, -999, numbertypegreat)
               numbertypegreat = "11"
               GREAT(self, -999, -999, numbertypegreat)
               print("A")
            if keys[pg.K_s]:
               numbertypeperfect = "2"
               PERFECT(self, -999, -999, numbertypeperfect)
               numbertypegreat = "2"
               GREAT(self, -999, -999, numbertypegreat)
               numbertypegreat = "22"
               GREAT(self, -999, -999, numbertypegreat)
               print("S")
            if keys[pg.K_k]:
               numbertypeperfect = "3"
               PERFECT(self, -999, -999, numbertypeperfect)
               numbertypegreat = "3"
               GREAT(self, -999, -999, numbertypegreat)
               numbertypegreat = "33"
               GREAT(self, -999, -999, numbertypegreat)
               print("K")
            if keys[pg.K_l]:
               numbertypeperfect = "4"
               PERFECT(self, -999, -999, numbertypeperfect)
               numbertypegreat = "4"
               GREAT(self, -999, -999, numbertypegreat)
               numbertypegreat = "44"
               GREAT(self, -999, -999, numbertypegreat)
               print("L")
      


if __name__ == "__main__":
# creating an instance or instantiating the Game class
   g = Game()
   g.new()
   g.run()