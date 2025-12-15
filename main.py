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
import shelve
from random import randint
import pygame as pg
from pygame import mixer
from os import path
# importing everything from other .py files
from settings import *
from sprites import *
from Utils import *

class Game: # creates class named Game that includes the below indented lines
   def __init__(self):
      pg.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Project Funkin'")
      self.playing = True
      pg.mixer.init()
      pg.display.init()

   # sets up a game folder directory path using the current folder containing THIS file
   # loads data from level1.txt so the Game class has a map property that uses the map class to parse the level1.txt file
   def load_data(self):
      self.game_folder = path.dirname(__file__)
      self.img_folder = path.join(self.game_folder, 'images')
      self.snd_folder = path.join(self.game_folder, 'sound effects')
      #  Takes Level types and puts them into a list to be used later
      if LEVEL == LEVEL1:
         self.map = Map(path.join(self.game_folder, LEVEL1))
      elif LEVEL == LEVEL2:
         self.map = Map(path.join(self.game_folder, LEVEL2))
      elif LEVEL == LEVEL3:
         self.map = Map(path.join(self.game_folder, LEVEL3))
      elif LEVEL == LEVEL4:
         self.map = Map(path.join(self.game_folder, LEVEL4))
      elif LEVEL == LEVEL5:
         self.map = Map(path.join(self.game_folder, LEVEL5))
      elif LEVEL == None:
         self.map = Map(path.join(self.game_folder, LEVEL_SELECTOR))

      #  Loads saved highscores
      hs_path = path.join(self.game_folder, 'level1 highscore')
      d = shelve.open(hs_path)
      if 'level1 highscore' not in d:
         d['level1 highscore'] = 0
      self.level1_highscore = d['level1 highscore']
      d.close()

      hs_path = path.join(self.game_folder, 'level2 highscore')
      d = shelve.open(hs_path)
      if 'level2 highscore' not in d:
         d['level2 highscore'] = 0
      self.level2_highscore = d['level2 highscore']
      d.close()

      hs_path = path.join(self.game_folder, 'level3 highscore')
      d = shelve.open(hs_path)
      if 'level3 highscore' not in d:
         d['level3 highscore'] = 0
      self.level3_highscore = d['level3 highscore']
      d.close()

      hs_path = path.join(self.game_folder, 'level4 highscore')
      d = shelve.open(hs_path)
      if 'level4 highscore' not in d:
         d['level4 highscore'] = 0
      self.level4_highscore = d['level4 highscore']
      d.close()
      
      hs_path = path.join(self.game_folder, 'level5 highscore')
      d = shelve.open(hs_path)
      if 'level5 highscore' not in d:
         d['level5 highscore'] = 0
      self.level5_highscore = d['level5 highscore']
      d.close()

      #  Loads images for ingame sprites
      self.player1_img = pg.image.load(path.join(self.img_folder, 'Player.png')).convert_alpha()
      self.player1_key_img = pg.image.load(path.join(self.img_folder, 'Player Key.png')).convert_alpha()
      self.all_restarts_img = pg.image.load(path.join(self.img_folder, 'Restart Button.png')).convert_alpha()
      self.all_levels_img = pg.image.load(path.join(self.img_folder, 'Level Start.png')).convert_alpha()
      self.all_quit_buttons_img = pg.image.load(path.join(self.img_folder, 'Quit Button.png')).convert_alpha()
      self.all_notes_img = pg.image.load(path.join(self.img_folder, 'Note.png')).convert_alpha()
      self.all_invisibles1_img = pg.image.load(path.join(self.img_folder, 'Invisible1.png')).convert_alpha()
      self.all_invisibles2_img = pg.image.load(path.join(self.img_folder, 'Invisible2.png')).convert_alpha()
      self.all_right_arrows_img = pg.image.load(path.join(self.img_folder, 'Right Arrow.png')).convert_alpha()
      self.all_left_arrows_img = pg.image.load(path.join(self.img_folder, 'Left Arrow.png')).convert_alpha()
      self.all_back_arrows_img = pg.image.load(path.join(self.img_folder, 'Back Arrow.png')).convert_alpha()

      self.gamestart_sound = pg.mixer.Sound(path.join(self.snd_folder, 'Game Start.mp3'))
      self.victory_sound = pg.mixer.Sound(path.join(self.snd_folder, 'Victory.mp3'))
      self.lose_sound = pg.mixer.Sound(path.join(self.snd_folder, 'Lost.mp3'))
      self.change_level_sound = pg.mixer.Sound(path.join(self.snd_folder, 'Level Change.mp3'))

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
      self.all_levels = pg.sprite.Group()
      self.all_quit_buttons = pg.sprite.Group()
      self.all_right_arrows = pg.sprite.Group()
      self.all_left_arrows = pg.sprite.Group()
      self.all_back_arrows = pg.sprite.Group()

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
            elif tile == 'S':
               Level(self, col, row, '1')
            elif tile == 'X':
               Quit_Button(self, col, row)
            elif tile == 'R':
               Right_Arrow(self, col, row)
            elif tile == 'L':
               Left_Arrow(self, col, row)
            elif tile == '<':
               Back_Arrow(self, col, row)
                  
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
      self.all_sprites.update()
      global LEVEL
      global VICTORYSOUNDFIX
      global LOSTSOUNDFIX
      global LOOPFIX1
      global LOOPFIX2
      global LOOPFIX3
      global LOOPFIX4
      global LOOPFIX5
      self.keyfix_cd1 = Cooldown(500)
      self.keyfix_cd2 = Cooldown(500)
      self.keyfix_cd3 = Cooldown(500)
      self.keyfix_cd4 = Cooldown(500)

      if self.player1.keyfix == True:
         self.keyfix_cd1.start()
         self.player1.keyfix = False
      if self.keyfix_cd1.ready():
         self.player1.image = self.player1_img

      if self.player2.keyfix == True:
         self.keyfix_cd2.start()
         self.player2.keyfix = False
      if self.keyfix_cd2.ready():
         self.player2.image = self.player1_img

      if self.player3.keyfix == True:
         self.keyfix_cd3.start()
         self.player3.keyfix = False
      if self.keyfix_cd3.ready():
         self.player3.image = self.player1_img

      if self.player4.keyfix == True:
         self.keyfix_cd4.start()
         self.player4.keyfix = False
      if self.keyfix_cd4.ready():
         self.player4.image = self.player1_img

      #  Restarts game instead with a different level so it will load a different map
      if self.player1.level == LEVEL1:
         self.player1.level = True
         LOOPFIX1 = False
         mixer.music.stop()
         self.playing = False
         LEVEL = LEVEL1
         g = Game()
         g.new()
         g.run()
      elif self.player1.level == LEVEL2:
         self.player1.level = True
         mixer.music.stop()
         self.playing = False
         LEVEL = LEVEL2
         g = Game()
         g.new()
         g.run()
      elif self.player1.level == LEVEL3:
         self.player1.level = True
         mixer.music.stop()
         self.playing = False
         LEVEL = LEVEL3
         g = Game()
         g.new()
         g.run()
      elif self.player1.level == LEVEL4:
         self.player1.level = True
         mixer.music.stop()
         self.playing = False
         LEVEL = LEVEL4
         g = Game()
         g.new()
         g.run()
      elif self.player1.level == LEVEL5:
         self.player1.level = True
         mixer.music.stop()
         self.playing = False
         LEVEL = LEVEL5
         g = Game()
         g.new()
         g.run()
      elif self.player1.level == 'Back':
         self.player1.level = None
         mixer.music.stop()
         self.playing = False
         LEVEL = None
         g = Game()
         g.new()
         g.run()
      if self.player1.level_selected > 5:
         self.player1.level_selected = 1
      if self.player1.level_selected < 1:
         self.player1.level_selected = 5

      # restarts the game when restart button gets clicked
      if LEVEL != None:
         if self.player1.restart == True:
            self.player1.restart = False
            self.player1.restart_exists == False
            self.player1.music = True
            self.player1.music_loop_fix = True
            VICTORYSOUNDFIX = False
            LOSTSOUNDFIX = False
            self.playing = False
            g = Game()
            g.new()
            g.run()

         if self.player1.notes == 0 and self.player1.mode == 1 and VICTORYSOUNDFIX == False:
            VICTORYSOUNDFIX = True
            self.victory_sound.play()

         if self.player1.health == 0 and self.player1.mode == 1 and LOSTSOUNDFIX == False:
            LOSTSOUNDFIX = True
            self.lose_sound.play()
         
         if self.player1.notes == 0 and self.player1.mode == 1 or self.player1.health == 0 and self.player1.mode == 1:
            #  Saves score only based off which level
            if LEVEL == LEVEL1:
               if self.player1.score > self.level1_highscore:
                  self.level1_highscore = self.player1.score

                  d = shelve.open(path.join(self.game_folder, 'level1 highscore'))
                  d['level1 highscore'] = self.level1_highscore
                  d.close()

            elif LEVEL == LEVEL2:
               if self.player1.score > self.level2_highscore:
                  self.level2_highscore = self.player1.score

                  d = shelve.open(path.join(self.game_folder, 'level2 highscore'))
                  d['level2 highscore'] = self.level2_highscore
                  d.close()

            elif LEVEL == LEVEL3:
               if self.player1.score > self.level3_highscore:
                  self.level3_highscore = self.player1.score

                  d = shelve.open(path.join(self.game_folder, 'level3 highscore'))
                  d['level3 highscore'] = self.level3_highscore
                  d.close()

            elif LEVEL == LEVEL4:
               if self.player1.score > self.level4_highscore:
                  self.level4_highscore = self.player1.score

                  d = shelve.open(path.join(self.game_folder, 'level4 highscore'))
                  d['level4 highscore'] = self.level4_highscore
                  d.close()

            elif LEVEL == LEVEL5:
               if self.player1.score > self.level5_highscore:
                  self.level5_highscore = self.player1.score

                  d = shelve.open(path.join(self.game_folder, 'level5 highscore'))
                  d['level5 highscore'] = self.level5_highscore
                  d.close()

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
            # loads a mp3 and plays it based on level
            # thank you for providing me with how to play music using pygame: https://www.geeksforgeeks.org/python/python-playing-audio-file-in-pygame/
            if LEVEL == LEVEL1:
               mixer.music.load("sound/Music_1.mp3")

               mixer.music.set_volume(0.7)

               mixer.music.play()

               self.player1.music_loop_fix = False

            elif LEVEL == LEVEL2:
               mixer.music.load("sound/Music_2.mp3")

               mixer.music.set_volume(1)

               mixer.music.play()

               self.player1.music_loop_fix = False

            elif LEVEL == LEVEL3:
               mixer.music.load("sound/Music_3.mp3")

               mixer.music.set_volume(1)

               mixer.music.play()

               self.player1.music_loop_fix = False

            elif LEVEL == LEVEL4:
               mixer.music.load("sound/Music_4.mp3")

               mixer.music.set_volume(1)

               mixer.music.play()

               self.player1.music_loop_fix = False

            elif LEVEL == LEVEL5:
               mixer.music.load("sound/Music_5.mp3")

               mixer.music.set_volume(1)

               mixer.music.play()

               self.player1.music_loop_fix = False

      if self.player1.stop_music == True:
         self.player1.stop_music = False
         mixer.music.stop()

      if LEVEL == None:
         VICTORYSOUNDFIX = False
         LOSTSOUNDFIX = False
         if self.player1.level_selected == 1 and LOOPFIX1 == False:
            LOOPFIX1 = True
            
            mixer.music.load("sound/Music_1.mp3")

            mixer.music.set_volume(0.7)

            mixer.music.play(loops= -1)
         elif self.player1.level_selected != 1:
            LOOPFIX1 = False

         if self.player1.level_selected == 2 and LOOPFIX2 == False:
            LOOPFIX2 = True
            
            mixer.music.load("sound/Music_2.mp3")

            mixer.music.set_volume(0.8)

            mixer.music.play(loops= -1)
         elif self.player1.level_selected != 2:
            LOOPFIX2 = False

         if self.player1.level_selected == 3 and LOOPFIX3 == False:
            LOOPFIX3 = True
            
            mixer.music.load("sound/Music_3.mp3")

            mixer.music.set_volume(0.5)

            mixer.music.play(loops= -1)
         elif self.player1.level_selected != 3:
            LOOPFIX3 = False

         if self.player1.level_selected == 4 and LOOPFIX4 == False:
            LOOPFIX4 = True
            
            mixer.music.load("sound/Music_4.mp3")

            mixer.music.set_volume(0.9)

            mixer.music.play(loops= -1)
         elif self.player1.level_selected != 4:
            LOOPFIX4 = False

         if self.player1.level_selected == 5 and LOOPFIX5 == False:
            LOOPFIX5 = True
            
            mixer.music.load("sound/Music_5.mp3")

            mixer.music.set_volume(0.9)

            mixer.music.play(loops= -1)
         elif self.player1.level_selected != 5:
            LOOPFIX5 = False

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
      if LEVEL != None:
         #  In game text
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

      if LEVEL == None:
         #  text shown for Level Selector
         self.draw_text(self.screen, str(self.player1.level_selected), 100, WHITE, 810, 150)
         self.draw_text(self.screen, str("Level"), 100, WHITE, 660, 150)
         self.draw_text(self.screen, str("Highscore:"), 50, WHITE, 690, 425)
         self.draw_text(self.screen, str("Song Length:"), 40, WHITE, 690, 5)

         #  Shows text based on what level is selected
         if self.player1.level_selected == 1:
            self.draw_text(self.screen, str(self.level1_highscore), 50, WHITE, 690, 500)
            self.draw_text(self.screen, str("1:25"), 40, WHITE, 690, 50)
         if self.player1.level_selected == 2:
            self.draw_text(self.screen, str(self.level2_highscore), 50, WHITE, 690, 500)
            self.draw_text(self.screen, str("4:00"), 40, WHITE, 690, 50)
         if self.player1.level_selected == 3:
            self.draw_text(self.screen, str(self.level3_highscore), 50, WHITE, 690, 500)
            self.draw_text(self.screen, str("1:18"), 40, WHITE, 690, 50)
         if self.player1.level_selected == 4:
            self.draw_text(self.screen, str(self.level4_highscore), 50, WHITE, 690, 500)
            self.draw_text(self.screen, str("2:22"), 40, WHITE, 690, 50)
         if self.player1.level_selected == 5:
            self.draw_text(self.screen, str(self.level5_highscore), 50, WHITE, 690, 500)
            self.draw_text(self.screen, str("1:46"), 40, WHITE, 690, 50)
      
      self.all_sprites.draw(self.screen)
      pg.display.flip()
   
   def events(self):
      keys = pg.key.get_pressed()
      for event in pg.event.get():
         if event.type == pg.QUIT or self.player1.playing == False: # checks if you try to quit the game
            print("this is happening")
            self.playing = False
         if event.type == pg.MOUSEBUTTONDOWN:
            # spawns mouse when mousebutton is down
            Mouse(self, -999, -999)
         global numbertypeperfect
         global numbertypegreat
         if LEVEL != None:
            if self.player1.health == 0 and self.player1.mode == 1 or self.player1.restart_exists == True:
               pass
            else:
               #  when a key is clicked it will spawn a sprite
               if keys[pg.K_a]:
                  self.player1.image = self.player1_key_img
                  numbertypeperfect = "1"
                  PERFECT(self, -999, -999, numbertypeperfect)
                  numbertypegreat = "1"
                  GREAT(self, -999, -999, numbertypegreat)
                  numbertypegreat = "11"
                  GREAT(self, -999, -999, numbertypegreat)
                  self.player1.keyfix = True
                  print("Left")
               if keys[pg.K_s]:
                  self.player2.image = self.player1_key_img
                  numbertypeperfect = "2"
                  PERFECT(self, -999, -999, numbertypeperfect)
                  numbertypegreat = "2"
                  GREAT(self, -999, -999, numbertypegreat)
                  numbertypegreat = "22"
                  GREAT(self, -999, -999, numbertypegreat)
                  self.player2.keyfix = True
                  print("Down")
               if keys[pg.K_k]:
                  self.player3.image = self.player1_key_img
                  numbertypeperfect = "3"
                  PERFECT(self, -999, -999, numbertypeperfect)
                  numbertypegreat = "3"
                  GREAT(self, -999, -999, numbertypegreat)
                  numbertypegreat = "33"
                  GREAT(self, -999, -999, numbertypegreat)
                  self.player3.keyfix = True
                  print("Up")
               if keys[pg.K_l]:
                  self.player4.image = self.player1_key_img
                  numbertypeperfect = "4"
                  PERFECT(self, -999, -999, numbertypeperfect)
                  numbertypegreat = "4"
                  GREAT(self, -999, -999, numbertypegreat)
                  numbertypegreat = "44"
                  GREAT(self, -999, -999, numbertypegreat)
                  self.player4.keyfix = True
                  print("Right")
      


if __name__ == "__main__":
# creating an instance or instantiating the Game class
   g = Game()
   g.new()
   g.run()