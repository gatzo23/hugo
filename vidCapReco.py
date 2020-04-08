import sys
import cv2
from pathlib import Path
from threading import *
from konversation import Speak
import speech_recognition as sr
import datetime
from tasks import *
from listen import *
from bot import bot1


def read_csv(filename):
    import csv
    import numpy as np

    images = []
    labels = []

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            assert len(row) == 2
            images.append(cv2.imread(row[0], 0))
            labels.append(int(row[1]))

    images = np.asarray(images)
    labels = np.asarray(labels)
    return images, labels
#LBPH Model
def create_and_train_model(images, labels):
    model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=80.00)
    #model = cv2.face.createLBPHFaceRecognizer(radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=80.00)
    model.train(images, labels)
    return model


def detect_faces(image, cascade_file):
    face_cascade = cv2.CascadeClassifier(cascade_file)
    return face_cascade.detectMultiScale(image)

def mark_faces(image, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) #Farbe grün

def get_user(prediction):
    #users = {0: 'person_0', 1: 'person_1', 2: 'person_2'}
    users = {0: 'kai', 1: 'anna'}
    return users[prediction]

def main():
    #Thread ausgeben
    print(current_thread().getName())
    home = str(Path.home()) #Holen des Homepfads wird nicht gebraucht da der vollständige Pfad in xml gespeichert wird
    xml = 'python/Lisa/Lisa/opencv/data/haarcascades/haarcascade_frontalface_default.xml' #Linux Pfad
    #xml = 'c:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml' #Windows Pfad
    cascade_file = '%s/%s' % (home, xml) #Linux Schreibweise
    #cascade_file = '%s' % (xml) #Windows Schreibweise

    #images, labels = read_csv('c:\\users\\asus\\source\\repos\\lisa\\lisa\\faces.csv') #Windows Schreibweise
    images, labels = read_csv('/Users/kaigatzlaff/python/Lisa/Hugo/faces.csv') #Linux Schreibweise
    model = create_and_train_model(images, labels)

    try:
        cap = cv2.VideoCapture(0)
        ret, img1 = cap.read()
        cv2.imshow("bild",img1)
    except:
        print("cap nicht bekommen")

    users = ["heinz"]
    user = ''
    userTimeStamp = {}
    #Sprachsteuerung aktivieren
    t1 = Thread(target = listen)
    t1.start()

    while True:
        ret, img = cap.read()
        assert ret

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(img, cascade_file)
        mark_faces(img, faces)
        
        for (x, y, w, h) in faces:
            face_img = gray[y:y + h, x:x + w]
            img_h, img_w = images[0].shape[:2]
            face_res = cv2.resize(face_img, (img_w, img_h))

            pred, conf = model.predict(face_res)
            if pred == -1:
                #Einschalten wenn über der Person ein Unknown stehen soll, dies steht aber immer da wenn das Bild nicht erkannt wird
                #cv2.putText(img, "unknown",(x,y), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0))
                continue

            user = get_user(pred)
            cv2.putText(img, '%s' % user, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0))
            #Zeit jetzt holen

            if (user in userTimeStamp):
                timeNow = datetime.now().timestamp()
                timeDiff = timeNow - userTimeStamp.get(user)
                #Check ob ich weg war
                if (timeDiff > 30):
                    Speak("Schön dass du wieder da bist {}".format(user))
                userTimeStamp[user] = timeNow
            else:
                userTimeStamp[user] = datetime.now().timestamp()
                Speak("Hallo {0}".format(user))
                result = spaet()
                Speak(result)
                result = weather("heute in Gifhorn")
                Speak(result)
        
        cv2.imshow('Kamera0', img)

        if (cv2.waitKey(30) & 0xff) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

