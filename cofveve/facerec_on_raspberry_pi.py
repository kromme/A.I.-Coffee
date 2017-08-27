# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
import glob
import cv2
import pandas
import serial
import time
from itertools import compress
import pickle
from play_sound_function import *
import speech_recognition as sr
from gtts import gTTS
from time import sleep
import os
from pygame import mixer

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

print ('Loading database')
df = pandas.read_csv('/home/pi/cofveve/db.csv', index_col=False, sep = ';')


print ("Initializing Coffee Machine..")
print ("")
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.timeout=3

# play intro sound

filename = '/home/pi/Sounds/koffietijd.mp3'
   
mixer.init()
mixer.music.load(filename)
mixer.music.play()





def brew(beverage, strong = 0):
    beverages = ['coffee', 'cafecreme', 'cafelait', 'cappu', 'espresso', 'doubleEspresso', 'hotchoc', 'hotwater']
    # check if beverage is known
    if beverage not in beverages:
            print ('choose one of the following: ', ', '.join(beverages))
            return False

    # check strongness
    if strong < -1 or strong > 1:
            print ('choose strong (1), weak (-1) or normal (0)')
            return False

    # set weaker beverage
    if strong == -1:
            ser.write('9'.encode())
            time.sleep(1.5)
            #print (ser.readline())

    if strong == 1:
            ser.write('0'.encode())
            time.sleep(1.5)
            #print (ser.readline())

    # brew beverage
    ser.write(str(beverages.index(beverage)+1).encode())
    time.sleep(1.5)

    return (ser.readline())

# Load faces we want to recognize
print("Loading known face image(s)")


with open('image_list_db.pickle' , 'rb' ) as f:
    image_list = pickle.load( f)

with open('image_names.pickle' , 'rb' ) as f:
    image_names = pickle.load( f)
    


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
# cascade file
cascPath = '/home/pi/cascades/haarcascade_frontalface_alt2.xml' 
faceCascade = cv2.CascadeClassifier(cascPath)

while True:

    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # detect faces
    faces = faceCascade.detectMultiScale(
                output,
                scaleFactor = 1.1,
                minNeighbors = 5,
                minSize = (30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
    )

    # print the current status of the program
    print ("Found " + str(len(faces)) + " faces at position(s): " + str(faces))

    if(len(faces) > 0):
       
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)
        face_names = []

        try:
            face_distances = face_recognition.face_distance(image_list, face_encodings[0])
        except:
            pass
        
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(image_list, face_encoding)

            if True not in match:
                print ("je bent lelijk van dichtbij. Neem jij maar rattengif")
                continue
            
            print(match)
            name = (list(compress(image_names,match))[0])
            print(name)

            #play sound
            play_sound(name)
            
            result = ''
            strong = 0
            who = name.lower()

            
            beverage = bytes(df[df.who == who].beverage.values[0],'UTF-8').decode('UTF-8')
            
            print(beverage)
            strong = int(df[df.who == who].strong)
            
            while len(result) == 0:

                    result = brew(beverage, strong)
                    print (result)
                    print ('')

            time.sleep(25)
