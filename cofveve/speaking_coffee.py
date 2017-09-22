# Load packages
# pip install SpeechRecognition gTTS time pygame pyaudio
import speech_recognition as sr
from gtts import gTTS
from time import sleep
import os
from pygame import mixer

while True:
    
    # Record audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
     
    # Speech recognition using Google Speech Recognition
    try:
        tekst = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # print the recognized text
    if 'tekst' in locals():
        print(tekst)
    
    # write the text that has to be spoken to an mp3 file
    tts = gTTS(text='Do you feel like cappuccino? Computer says no! Take a double shot espresso', lang='en')
    filename = "D:/Documents/Python/test.mp3"
    tts.save(filename)

    # play the mp3 file
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    sleep(10)

    # stop playing
    mixer.music.stop()
    mixer.quit()
    
    # delete the mp3 file
    os.remove(filename)
