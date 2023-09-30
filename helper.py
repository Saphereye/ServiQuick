import threading
import pyttsx3

API_KEY = 'iWrpAat8eDeNt2CqqWtw6bQPweqd2xqCNk7wh9gR_p8'
ORS_API_KEY = '5b3ce3597851110001cf6248056ade7a5d63493cb05b0d6692675228'

engine = pyttsx3.init()
engine.setProperty('voice', 'english+f3') 

def temp(text):
    engine.say(text)
    engine.runAndWait()

def speak(text: str):
    engine.say(text)
    engine.runAndWait()
    