import os
from gtts import gTTS
import subprocess
import random
from datetime import datetime
import time
import sys
import speech_recognition as sr
import config
from fuzzywuzzy import fuzz as fuzz_ratio
from googlesearch import search
import webbrowser

def genrateDynemicSpeaker(text):
    tts = gTTS(text, lang='uk', slow = False)
    tts.save("audio/output.mp3")
    subprocess.call(['afplay', 'audio/output.mp3'])
    os.remove("audio/output.mp3")

def genrateSpeaker(text,namefile):
    tts = gTTS(text, lang='uk', slow = False)
    tts.save("audio/"+namefile+".mp3")

def rebootPc():
    subprocess.call(['afplay', 'audio/reboot.mp3'])
    time.sleep(30)
    subprocess.run(['sudo', 'reboot'])


def upVolume():
    current_volume = int(os.popen("osascript -e 'output volume of (get volume settings)'").read().strip())
    new_volume = min(current_volume + 10, 100)  
    applescript = f'set volume output volume {new_volume}'
    os.system(f"osascript -e '{applescript}'")
    os.system(f"osascript -e 'display notification \"Гучність: {new_volume}%\"'")
    subprocess.call(['afplay', 'audio/upvolume.mp3'])


def downVolume():
     current_volume = int(os.popen("osascript -e 'output volume of (get volume settings)'").read().strip())
     new_volume = max(current_volume - 10, 0) 
     applescript = f'set volume output volume {new_volume}'
     os.system(f"osascript -e '{applescript}'")
     os.system(f"osascript -e 'display notification \"Гучність: {new_volume}%\"'")
     subprocess.call(['afplay', 'audio/downvolume.mp3'])

def help():
    subprocess.call(['afplay', 'audio/help.mp3'])

def openBrowser():
    subprocess.run(["open", "-a", "Google Chrome", "https://www.google.com"])
    subprocess.call(['afplay', 'audio/openbrowser.mp3'])

def openYoutube():
    subprocess.run(["open", "-a", "Google Chrome", "https://www.youtube.com/"])
    subprocess.call(['afplay', 'audio/openyoutube.mp3'])

def shotDownPc():
    subprocess.call(['afplay', 'audio/shotdownpc.mp3'])
    time.sleep(30)
    os.system("sudo shutdown -h now")

def sleepPc():
    subprocess.call(['afplay', 'audio/sleeppc.mp3'])
    time.sleep(30)
    subprocess.call(["osascript", "-e", "tell application \"System Events\" to sleep"])
def joke():
    jokes = ['Как смеются программисты? ... ехе ехе ехе','ЭсКьюЭль запит заходить в бар, підходить до двох столів і запитує .. «м+ожно приєднатися?»','Программіст це машина для перетворення кофе в код']
    joke = random.choice(jokes)
    genrateDynemicSpeaker(joke)
def date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d день %m місяць %Y року")
    genrateDynemicSpeaker(formatted_date)

def time_():
     current_time = datetime.now()
     formatted_time = current_time.strftime("%H година %M хвилин %S секунд")
     genrateDynemicSpeaker(formatted_time)

def call():
        subprocess.call(['afplay', 'audio/call.mp3'])

def stop():
    subprocess.call(['afplay', 'audio/stop.mp3'])
    sys.exit()

def addNote(note_text):
    # Формуємо AppleScript для створення нотатки
    applescript = f'tell application "Notes"\n' \
                  f'    activate\n' \
                  f'    make new note at folder "Notes" with properties {{body:"{note_text}"}}\n' \
                  f'end tell\n'
    # Виконуємо AppleScript через osascript
    subprocess.run(['osascript', '-e', applescript])
    print('Нотатка створена.')

def googleSearch(query):
    query_search = "я загуглила " + query
    genrateDynemicSpeaker(query_search)
    search_results = search(query, num_results=2, lang='uk')
    first_result = next(search_results)
    webbrowser.open(first_result)

def mainSearcher(language): 
    subprocess.call(['afplay', 'audio/start.mp3'])
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Скажіть щось...")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language = language)
            print("Ви сказали:", text)
            if text.lower().startswith("додатай нотатку") :
                note_text = text.split("додатай нотатку",1)[1].strip()
                addNote(note_text)
            elif text.lower().startswith("загугли"):
                query = text.split("загугли", 1)[1].strip()
                googleSearch(query)
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_ALIAS_UKR):
                call()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_BROWSER):
                openBrowser()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_YOUTUBE):
                openYoutube()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 90 for alias in config.VA_CMD_VOLUME_UP):
                upVolume()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 90 for alias in config.VA_CMD_VOLUME_DOWN):
                downVolume()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_SHUTDOWN):
                shotDownPc()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_SLEEP):
                sleepPc()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_REBOOT):
                rebootPc()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_DATE):
                date()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_TIME):
                time_()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_HELP): 
                help()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_JOKE):
                joke()
            elif any(fuzz_ratio.ratio(text.lower(), alias.lower()) > 70 for alias in config.VA_CMD_STOP):
                stop()
        except sr.UnknownValueError:
            print("Не можу розпізнати голос")
        except sr.RequestError as e:
            print("Помилка сервісу Google Speech Recognition; {0}".format(e)) 

