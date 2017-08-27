import speech_recognition as sr
from gtts import gTTS
from time import sleep
import os
from pygame import mixer
import pygame

def play_sound(name):

    # to lower
    name = name.lower()

    # database
    sounds_db = {'willem' : 'willem.mp3',
                 'joost':'joost.mp3',
                 'jeroen' : 'jeroen.mp3',
                 'klaas':'Zwakkeling.mp3' }

    # sound path
    sound_path = '/home/pi/Sounds/'

    # get sound
    if name in sounds_db.keys():

        sound = sounds_db[name]

    else:

        sound = 'koffietijd.mp3'

    # 
    
    filename = sound_path + sound
   
    mixer.init()
    mixer.music.load(filename)
    #mixer.Sound(filename)
    mixer.music.play()
    sleep(5)

    # stop playing
    #mixer.music.stop()
    mixer.quit()
