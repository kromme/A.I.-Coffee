# Load packages
from gtts import gTTS
from time import sleep
import os
from pygame import mixer

# create mp3 files with different texts

# Biertje
tts = gTTS(text='Pak gewoon een biertje!', lang='nl')
tts.save("/home/pi/Sounds/Biertje.mp3")

# Nodig
tts = gTTS(text='Je kan wel zien dat je het nodig hebt, sterkte vandaag', lang='nl')
tts.save("/home/pi/Sounds/Nodig.mp3")

# Genieten
tts = gTTS(text='Geniet er lekker van', lang='nl')
tts.save("/home/pi/Sounds/Genieten.mp3")

# Niet overbodig
tts = gTTS(text='Koffie is voor jou niet overbodig vandaag', lang='nl')
tts.save("/home/pi/Sounds/NietOverbodig.mp3")

# Zwakkeling
tts = gTTS(text='Zwakkelling', lang='nl')
tts.save("/home/pi/Sounds/Zwakkeling.mp3")



### play the mp3 file
##mixer.init()
##mixer.music.load(filename)
##mixer.music.play()
##sleep(10)
##
### stop playing
##mixer.music.stop()
##mixer.quit()

