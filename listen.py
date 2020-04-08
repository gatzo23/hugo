import sys
import speech_recognition as sr
import os
from konversation import Speak
from tasks import *
from threading import *

dictTask={"amazon":"internet(https://www.amazon.de)",
            "dose an":"openhabHome('Dose_Power','ON')",
            "dose aus":"openhabHome('Dose_Power',''OFF')",
            "fahre den":"shutdown()",
            "geboren":"birth()",
            "internet":"internet(https://www.google.de)",
            "kaffee":"openhabHome('Dose_Power',ON",
            "kino":"internet(https://www.kinoz.to)",
            "lampe an":"openhabHome('Lampe_Brightness','ON')",
            "lampe aus":"openhabHome('Lampe_Brightness','OFF')",
            "lampe ein":"openhabHome('Lampe_Brightness','ON')",
            "nextcloud":"internet(https://kaiserver2.z0euvq4xrgy91cvo.myfritz.net/index.php/login)",
            "sag":"sprechen()",
            "spät":"spaet()",
            "spiegel":"internet(https://www.spiegel.de)",
            "wetter":"weather('*')",
            "wie viel":"calculation('*')",
            "wer ist":"wiki('*')",
            "was ist":"wiki('*')",
            "wer sind":"wiki('*')",
            "was sind":"wiki('*')"
            }

def listen():
    print(current_thread().getName())
    r = sr.Recognizer()
    text = ""
    print("Hören...")
    while (text != "stop"):
        with sr.Microphone() as source:
            audio_data = r.record(source, duration=2)
            #Falls im Zug, Zuhören überschreiben
            #text=input("Enter some text: ").lower()
            try:
                text = r.recognize_google(audio_data, language="de-DE").lower()
                print(text)
            except:
                pass
        if "hugo" in text:
            print("Hallo Kai")
            os.system('afplay /System/Library/Sounds/Sosumi.aiff') #kurzer beep zum sprechen
            with sr.Microphone() as source:
                audio_data = r.record(source, duration=4)
                #Falls im Zug, Zuhören überschreiben
                #text = input("Enter some more text: ").lower()
                try:
                    befehl = ""
                    #hier ausschalten wenn im zug
                    text = r.recognize_google(audio_data, language="de-DE").lower()  
                    for i in dictTask:
                        if i in text:
                            befehl = dictTask.get(i)
                    #prüfung ob platzhalter im Befehl und dann mit StringBefehl austauschen
                    if ('*' in befehl):
                        befehl = befehl.replace("*", text)
                    print(befehl + ' -- Text falls der Befehl leer ist')

                    if befehl != "":
                        result = eval(befehl)
                        print(result)
                        Speak(result)
                except:
                    print("except aufgabe")
                    text = ""
                    pass
        elif "stop" in text:
            text = "Stop"
        
