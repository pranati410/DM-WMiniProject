import datetime
import os
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia
from win32com.client import Dispatch
import cv2
import numpy as np
import time

try:
    engine = pyttsx3.init()
except ImportError:
    print('required driver is not found!....')
except RuntimeError:
    print('driver fails to initialize!...')
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)  # changes the voice

def speak(cmd):
    engine.say(cmd)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!Pranati")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! Ma'am")

    else:
        speak("Good Evening! Ma'am")

def read_voice_cmd():
    voice_text = ''
    speech = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening....')
        speech.pause_threshold = 1
        speech.adjust_for_ambient_noise(source, 1)
        audio = speech.listen(source)

    try:
        voice_text = speech.recognize_google(audio, language='en-in')
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print('Network error!...')
    return voice_text


if __name__ == '__main__':
    wishMe()
    while True:

        query = read_voice_cmd().lower()
        print('cmd : {}'.format(query))

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia"," ")
            results = wikipedia.summary(query, sentences=1)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'hello sara' in query:
            speak('Hello Mam . how can i help you?')
            continue
        elif 'open explorer' in query:
            speak('ok Mam')
            os.system('explorer C:\\"{}"'.format(query.replace('Open', '')))
            continue
        elif 'open youtube' in query:
            speak('ok Mam.')
            webbrowser.open('youtube.com')
        elif 'open google' in query:
            speak('ok Mam.')
            webbrowser.open('google.co.in')
        elif 'please play music' in query:
            speak('ok Mam.')
            music_dir = "D:\songs"
            speak('Mam there are many songs! which song you want to play?')
            query = read_voice_cmd().lower()
            speak('ok Mam.')
            os.startfile(os.path.join(music_dir, query + ".mp3"))
            mp = Dispatch("WMPlayer.OCX")
            tune = mp.newMedia(music_dir + query)
            mp.currentPlaylist.appendItem(tune)
            mp.controls.play()
        elif 'Can you tell me When is my Birthday' in query:
            speak('4th October 1998')

        elif 'is this' in query:
            # Load Yolo
            net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
            classes = []
            with open("coco.names", "r") as f:
                classes = [line.strip() for line in f.readlines()]
            layer_names = net.getLayerNames()
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
            colors = np.random.uniform(0, 255, size=(len(classes), 3))

            # Loading image
            cap = cv2.VideoCapture(0)

            font = cv2.FONT_HERSHEY_PLAIN
            starting_time = time.time()
            frame_id = 0

            while True:
                _, frame = cap.read()
                frame_id += 1
                height, width, channels = frame.shape

                # Detecting objects
                blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

                net.setInput(blob)
                outs = net.forward(output_layers)

                # Showing informations on the screen
                class_ids = []
                confidences = []
                boxes = []
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:
                            # Object detected
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)

                            # Rectangle coordinates
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)

                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                # print(indexes)

                for i in range(len(boxes)):
                    if i in indexes:
                        x, y, w, h = boxes[i]
                        label = str(classes[class_ids[i]])
                        color = colors[i]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)

                elapse_time = time.time() - starting_time
                fps = frame_id / elapse_time
                cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 100), font, 3, (0, 0, 0), 1)
                cv2.imshow("Image", frame)
                key = cv2.waitKey(1)
                speak(label)
                if key == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif 'Can you tell my address' in query:
            speak('Christian Colony, Baramati, Pune')
        elif 'my name' in query:
            speak('Mam your name is Pranati')
        elif 'your full name' in query:
            speak('My Name is Sara Version 2 point 0, i am your Python Personal Assistant Mam')
        elif 'are you single' in query:
            speak('Yes! Mam')
        elif 'will you marry me' in query:
            speak('No Mam, i am not a human, i am a machine , i cant marry you!...')
        elif 'bye' in query:
            speak('Bye Ms. Pranati Have a Great Day')
            exit()
