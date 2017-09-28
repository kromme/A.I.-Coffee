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
    with sr.Microphone(device_index=2, sample_rate = 48000) as source:
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
