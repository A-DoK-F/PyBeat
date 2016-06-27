 #!/usr/bin/env python3
# coding: utf-8

from moviepy.editor import AudioFileClip

import threading
import vlc
import random
#import numpy as np
import sys
import pygame
import time
from pygame.locals import *


global sound_array
global song
global score

class Square(pygame.sprite.Sprite):
    def __init__(self,all_sprites,width, height, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self, all_sprites)

        self.image_empty = pygame.image.load('img/empty_square.png').convert_alpha()
        self.image_red = pygame.image.load('img/red_square.png')
        self.image_orange = pygame.image.load('img/orange_square.png')
        self.image_green = pygame.image.load('img/green_square.png')
        self.image = self.image_empty

        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = None

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.is_triggered = False

        self.frame_tick = 0
        self.tick_per_frame = 1

    def update(self):
        for i in range(len(all_square)):
            if all_square[i].is_triggered == True:
                if all_square[i].frame_tick >= 0 and all_square[i].frame_tick < 60:
                    all_square[i].image = all_square[i].image_red
                    all_square[i].frame_tick +=1
                elif all_square[i].frame_tick >= 60 and all_square[i].frame_tick < 120:
                    all_square[i].image = all_square[i].image_orange
                    all_square[i].frame_tick +=1
                elif all_square[i].frame_tick <= 180:
                    all_square[i].image = all_square[i].image_green
                    all_square[i].frame_tick +=1
                elif all_square[i].frame_tick >= 180:
                    all_square[i].image = all_square[i].image_empty
                    all_square[i].is_triggered = False
                    all_square[i].frame_tick = 0
            else:
                all_square[i].image = all_square[i].image_empty
                all_square[i].is_triggered = False
                all_square[i].frame_tick = 0


        #print(all_square[0].frame_tick)


#initialisation
score = 0
song = "myaudio.mp3"
# Get the sound (we be an array with values between 0 and 1)
audio = AudioFileClip(song) # could be a wav, ogg... 13553253
vlcplayer = vlc.MediaPlayer(song)
sound_array = audio.to_soundarray()

PlaybackThread = threading.Thread(target=vlcplayer.play)
PlaybackThread.daemon = True

GAME_WIDTH = 720
GAME_HEIGHT = 720

all_square = []
game_map = []

#initialisation de la sequence de pop à partir du son charger
#sound_array a pour valeur -1 à +1 donc on on décale vers 0 à 2
for i in range (0,len(sound_array)):
    sound_array[i] += 1
    #print(sound_array[i])



for j in range(0,int(len(sound_array)/706)):
    somme = 0
    for i in range(0, 706):
        somme += sound_array[((j*706)+i),0]
    game_map.append(somme/420)
    #print(game_map)



pygame.init()  # Initialisation de pygame

clock = pygame.time.Clock()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))  # Création de la fenêtre
pygame.display.set_caption("PyBeat")  # Définition du nom de la fenêtre
background = pygame.image.load("img/background.png")  # Création de la "surface" de fond

all_sprites = pygame.sprite.LayeredUpdates()

for i in range(0,4):
    for j in range(0,4):
        all_square.append(Square(all_sprites,180, 180, j*180, i*180))

#Variable qui continue la boucle si = 1, stoppe si = 0
continuer = True

#Début du thread de lecture de la musique
PlaybackThread.start()
#Boucle infinie
while continuer:

    clock.tick(4)

    #(pressed1,pressed2,pressed3) = pygame.mouse.get_pressed()
    all_sprites.update()
    window.blit(background, (0, 0))  # "Colle" le fond sur la fenêtre
    all_sprites.draw(window)

    if game_map[int(vlcplayer.get_time()/16)] > 1:
        carre_displayed = False
        #while carre_displayed == False:
        genere = random.randint(0, 15)

        if all_square[genere].is_triggered == False:
            all_square[genere].is_triggered = True
            carre_displayed = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Votre Score : " + str(score) + " Merci d'avoir joué!")
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Votre Score : " + str(score) + " Merci d'avoir joué!")
                sys.exit(0)
            if event.key == pygame.K_SPACE:
                pos = pygame.mouse.get_pos()

                for i in range(0, 16):
                    if all_square[i].rect.collidepoint(pos):
                        if all_square[i].is_triggered:
                            if all_square[i].frame_tick >= 0 and all_square[i].frame_tick < 60:
                                score -= 100
                                all_square[i].is_triggered = False
                                all_square[i].frame_tick = 0
                            elif all_square[i].frame_tick >= 60 and all_square[i].frame_tick < 120:
                                score += 50
                                all_square[i].is_triggered = False
                                all_square[i].frame_tick = 0
                            elif all_square[i].frame_tick <= 180:
                                score += 200
                                all_square[i].is_triggered = False
                                all_square[i].frame_tick = 0


    if vlcplayer.is_playing() == 0:
        print("Votre Score : " + str(score) + " Merci d'avoir joué!")
        sys.exit(0)

    pygame.display.flip()
