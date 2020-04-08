
#Tasks die von Lisa ausgeführt werden können definiert im dictTask
from datetime import datetime
import urllib
from konversation import Speak
import sys, os
import webbrowser
import json
import requests
import wikipedia
from openhab import OpenHAB
from bs4 import BeautifulSoup
import urllib3

#Uhrzeit
def spaet():
    zeit = datetime.now()
    strZeit = zeit.strftime('%H:%M')
    return("Die Uhrzeit ist " + strZeit)

#Openhab, SmartHome
def openhabHome(itemOpenhab, state):
    r = requests.get('https://openhab.z0euvq4xrgy91cvo.myfritz.net:8443/rest', verify=False)
    openhab = OpenHAB(r)

    item = openhab.get_item(itemOpenhab)
    #items = openhab.fetch_all_items()
    if itemOpenhab == "Lampe_Brightness": 
        if state == "ON":
            item.command(54)
            return ("Die Lampe wurde eingeschaltet")
        elif state == "OFF":
            item.command(0)
            return ("Die Lampe wurde ausgeschaltet")
    elif itemOpenhab == "Dose_Power":
        if state == "ON":
            item.command("ON")
            return ("Die Dose wurde eingeschaltet")
        elif state == "OFF":
            item.command("OFF")
            return ("Die Dose wurde ausgeschaltet")
    else:
        print("kein gültiges Item gefunden")
        return ("Das Kommando wurde nicht erkannt")

#Wann ist Hugo geboren
def birth():
    return ("Ich wurde erschaffen am dreizehnten Februar 20")

#Fahre den Rechner runter
def shutdown():
    os.system('shutdown -h 10')
    return ("Der Computer wird jetzt runtergefahren")

#öffne internet seite
def internet(seite):
    webbrowser.open(seite)
    return ("Browser wird geöffnet")

#sag ein Satz
def sprechen():
    return ("Ein intelligenter Mann ist manchmal dazu gezwungen betrunken zu sein, um Zeit mit Idioten zu verbringen.")

#Funktionen für den Wetterbericht
def getTemp(tempJson, wetterOrt):
    weather = tempJson.json()
    for item in weather:
        if "main" == item:
            temperatur = (weather[item]["temp"])
            befehl = "In {0} werden es heute {1} Grad Celsius"
            return (befehl.format(wetterOrt, round(temperatur)))
            break

def getTempFc(tempJson, wetterOrt, x):
    weather = tempJson.json()
    z = 0
    while x > 0:
        for item in weather:
            if "list" == item:
                y = "0" + str(z)
                temperatur = (weather[item][int(y)]["main"]["temp"])
                if x == 1:
                    befehl = "In {0} werden es morgen {1} Grad Celsius"
                else:
                    befehl = "In {0} werden es in den nächsten drei Tagen {1} Grad Celsius"
                    z = z + 1
                return (befehl.format(wetterOrt, round(temperatur)))
                break
        x = x - 1

def weather(ort):
    #ort holen
    apiKey = "5df18e2eb2595b515776f0c55f2b0986"
    lst = ort.split(" ")
    try:
        i = lst.index("in")
        wetterOrt = lst[i+1]
    except:
        pass
    if ("heute" in ort) or ("ist" in ort):
        print("in heute")
        tempJson = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + wetterOrt + "&appid=" + apiKey + "&units=metric")
        result = getTemp(tempJson, wetterOrt)
        print(result)
        return result
    elif("morgen" in ort):
        x = 1
        tempJsonFC = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=" + wetterOrt + "&appid=" + apiKey + "&units=metric")
        #tempJson = Daten von OpenWeatherMap, wetterOrt = Ort, befehl=Text aus Befehl, x = Anzahl wie oft die for Schleife später durchlaufen wird
        result = getTempFc(tempJsonFC, wetterOrt, x)
        return result
    elif ("wird" in ort):
        x = 3
        tempJsonFC = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=" + wetterOrt + "&appid=" + apiKey + "&units=metric")
        result = getTempFc(tempJsonFC, wetterOrt, x)
        return result
    else:
        return ("Ich konnte den Tag nicht finden")

#Mathe
def calculation(aufgabe):
    print("Rechnen")
    print(aufgabe)
    lst = aufgabe.split(" ")
    try:
        if(lst[4] == "x"):
            result = (int(lst[3])*int(lst[5]))
            return ('Das Ergebnis ist {0}'.format(result))
        elif(lst[4] == "+"):
            result = (int(lst[3])+int(lst[5]))
            return ('Das Ergebnis ist {0}'.format(result))
        elif(lst[4] == "-"):
            result = (int(lst[3])-int(lst[5]))
            return ('Das Ergebnis ist {0}'.format(result))
        elif(lst[4] == "/"):
            result = (int(lst[3])/int(lst[5]))
            return ('Das Ergebnis ist {0}'.format(result))
    except:
        pass

#Wikipedia
def wiki(aufgabe):
    name = ""
    #Löschen von eine, ein
    if ("eine" in aufgabe):
        aufgabe = aufgabe.replace("eine ", "")
    elif("ein" in aufgabe):
        aufgabe = aufgabe.replace("ein ", "")
        
    nameSplit = aufgabe.split(" ")
    #Index zum Starten der Suche auf den Namen für Wikipedia
    try:
        i = nameSplit.index("ist")
    except:
        i = nameSplit.index("sind")

    lengthNameSplit = len(nameSplit)
    while (i < (lengthNameSplit-1)):
        name = name + nameSplit[i+1]
        name = name + " "
        i = i + 1
    try:
        wikipedia.set_lang("de")
        print(wikipedia.summary(name,sentences=4))
        return (wikipedia.summary(name,sentences=4))
    except:
        print("name not found")

