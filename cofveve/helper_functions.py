

import pygame
import face_recognition
import time, os, glob, pickle
import picamera
import numpy as np
import cv2
import pandas as pd
import serial
import speech_recognition as sr
from itertools import compress
from gtts import gTTS
from time import sleep
from pygame import mixer



def play_sound(name):
    '''
    play sound that belongs to a person.
    '''

    # convert name to lowercase
    name = name.lower()

    # database
    sounds_db = {'willem' : 'willem.mp3',
                 'joost':'joost.mp3',
                 'jeroen' : 'jeroen.mp3',
                 'klaas':'Zwakkeling.mp3' }

    # sound path
    sound_path = '/home/pi/A.I.-Coffee/Sounds/'

    # get sound. if not in database, get default.
    if name in sounds_db.keys():

        sound = sounds_db[name]

    else:

        sound = 'koffietijd.mp3'

    # create path to sound 
    filename = sound_path + sound
   
    # play sound.
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    
    # wait till sound is played.
    sleep(5)

    # stop playing
    mixer.quit()



def brew(ser, beverage):
    '''
    Tell the coffee machine which beverage to brew
    '''

    # list of beverages. should be aligned with the values in the arduino
    beverages = ['coffee', 'cafecreme', 'cafelait', 'cappu', 'espresso', 'doubleEspresso', 'hotchoc', 'hotwater']
    
    # check if beverage is known
    if beverage not in beverages:
            print ('choose one of the following: ', ', '.join(beverages))
            return False

    # brew beverage
    ser.write(str(beverages.index(beverage)+1).encode())
    time.sleep(1.5)

    return (ser.readline())
