#!/bin/bash
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:50:19 2017

@author: w.v.d.geest
script om foto's in te scannen als tbv face recognition
"""

import os
import face_recognition
from scipy import misc
import pickle
import glob, os

#location_faces = "C:/Users/w.v.d.geest/Documents/Python/FaceRecognition/Faces/"
location_faces = "/home/pi/known_faces/"
location_pickles = "/home/pi/A.I.-Coffee/cofveve/"
face_encodings = []
face_names = []

pictures = os.listdir(location_faces)
print(pictures)
names_list_old = pickle.load( open(location_pickles+'image_names.pickle', "rb") )
pictures_without_jpg = []
print(names_list_old)
#remove .jpg from names_list_old > create names_list_old_without_jpg
for i in range(0, len(pictures)):
    picture_without_jpg = pictures[i].replace(".jpg", "")
    pictures_without_jpg.append(picture_without_jpg)

new_faces = set(pictures_without_jpg) - set(names_list_old)
new_faces = list(new_faces)
print(new_faces)
#i = 0

try:
    for i in range(0,len(new_faces)):
        picture = location_faces+new_faces[i]+'.jpg'
    #read picture
        arr = misc.imread(picture) 
    #find location of face
        face_locations = face_recognition.face_locations(arr)
    # get encodings, add to list
        face_encoding = face_recognition.face_encodings(arr, face_locations)
        face_encodings = face_encodings + face_encoding

        face_name = new_faces[i].split(".",1)[0]
        face_names.append(face_name)


    #toevoegen aan bestaande pickles
    names_list_old.extend(face_names)

    face_encodings_old = pickle.load( open(location_pickles+'image_list_db.pickle', "rb") )

    face_encodings_old.extend(face_encodings)

    #save as pickle files
    with open(location_pickles+'image_list_db.pickle', 'wb') as f:
        pickle.dump(face_encodings_old, f, protocol = 2)

    with open(location_pickles+'image_names.pickle', 'wb') as f:
        pickle.dump(names_list_old, f, protocol = 2)

except:
    print('oeps, er is iets mis gegaan met het verwerken van de nieuwe foto´s')
