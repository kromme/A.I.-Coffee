
#### -------------------------------------------------------------------------------------------------------- ####
#### -------------------------------------------------------------------------------------------------------- ####
#### -----                  _____              _____ ____  ______ ______ ______ ______ 		    	----- ####
#### -----          /\     |_   _|      _     / ____/ __ \|  ____|  ____|  ____|  ____|			----- ####
#### -----         /  \      | |      _| |_  | |   | |  | | |__  | |__  | |__  | |__   			----- ####
#### -----        / /\ \     | |     |_   _| | |   | |  | |  __| |  __| |  __| |  __|  			----- ####
#### -----       / ____ \ _ _| |_ _    |_|   | |___| |__| | |    | |    | |____| |____ 			----- ####
#### -----      /_/    \_(_)_____(_)          \_____\____/|_|    |_|    |______|______|			----- ####
#### -------------------------------------------------------------------------------------------------------- ####
#### -------------------------------------------------------------------------------------------------------- ####
 

__author__ = ['j.schooneman', 't.stalman','k.tjepkema','j.v.d.leegte','w.v.d.geest','j.kromme']
__description__ = 'Script running on raspberry pi, which is connected to a coffee machine. It integrates face recognition for automatic coffee dispention'

# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

# ------ import packages
import face_recognition
import time, os, glob, pickle
import picamera
import numpy as np
import cv2
import pandas as pd
import serial
import speech_recognition as sr
from helper_functions import brew, play_sound
from itertools import compress
from gtts import gTTS
from time import sleep
from pygame import mixer


# ------ set parameters
working_directory = '/home/pi/A.I.-Coffee/'
database_path = working_directory + 'cofveve/db.csv'
serial_path = '/dev/ttyACM0'
image_list_path = working_directory + 'cofveve/image_list_db.pickle'
image_names_path = working_directory + 'cofveve/image_names.pickle' 
intro_sound_path = working_directory + 'Sounds/koffietijd.mp3'
face_cascade_path = working_directory + 'cascades/haarcascade_frontalface_alt2.xml' 
middle_finger_cascade_path =  working_directory + 'cascades/middlefinger_19.xml'




# ------ initialize camera
# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# ------ loading database with who wants which coffee
print ('Loading database')
df = pd.read_csv(database_path, index_col=False, sep = ';')

# ------ connect to the serial to the arduino.
print ("Initializing Coffee Machine..")
print ("")
ser = serial.Serial(serial_path, 9600)
ser.timeout=3

# ------ Load faces we want to recognize
print("Loading known face image(s)")

with open(image_list_path , 'rb' ) as f:
    image_list = pickle.load( f)

with open(image_names_path, 'rb' ) as f:
    image_names = pickle.load( f)
    

# ------ play intro sound
mixer.init()
mixer.music.load(intro_sound_path)
mixer.music.play()


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

# ------- load cascade file
faceCascade = cv2.CascadeClassifier(face_cascade_path)
middleFingerCascade = cv2.CascadeClassifier(middle_finger_cascade_path)


# ------ start the loop
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


    # detect middlefingers
    middleFingers = middleFingerCascade.detectMultiScale(
                output,
                scaleFactor = 1.1,
                minNeighbors = 5,
                minSize = (30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
    )



    # print the current status of the program
    print ("Found %d faces at position(s): %s & %d middel fingers at position(s): %s" %( len(faces), str(faces), len(middleFingers), str(middleFingers)))

    # if there are faces detected
    if(len(faces) > 0):
       
        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))

        # get encodings
        face_encodings = face_recognition.face_encodings(output, face_locations)
        face_names = []

        # NOT NECESSARY: try to create distances between found face and the earlier loaded faces.
        # face_distances = face_recognition.face_distance(image_list, face_encodings[0])
       
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(image_list, face_encoding)

            # if we don't have a match, end this iteration. Go in the new loop.
            if True not in match:
                print ("je bent lelijk van dichtbij. Neem jij maar rattengif")
                continue
            
            # get name of the match
            name = (list(compress(image_names,match))[0])
            print(name)

            # play sound that belongs with this name.
            play_sound(name)
            
            result = ''
            strong = 0
            
            # check the beverage
            beverage = bytes(df[df.who == name.lower()].beverage.values[0],'UTF-8').decode('UTF-8')
            strong = int(df[df.who == name.lower()].strong)
            
            print('Drinks %s, strongness: %s' %( str(beverage), str(strong)))
            
            # if we've got a drink, brew it
            while len(result) == 0:

                    result = brew(beverage, strong)
                    print (result)
                    print ('')

            # wait 25 seconds for the new loop.
            time.sleep(25)
    
    # if it can't find face, but it does find middle fingers
    elif (len(middleFingers) > 0):

    	result = ''
        strong = 0
        beverage = 'espresso'
        
        # play a sound
        # play_sound('middlefinger')
    	
    	# brew an espresso
    	while len(result) == 0:

            result = brew(beverage, strong)
            print (result)
            print ('first espresso')
        
        # wait till done
        time.sleep(15)

        # brew a second espresso to make it a double
        result = ''
        while len(result) == 0:
            result = brew(beverage, strong)
            print (result)
            print ('second espresso')

        time.sleep(25)