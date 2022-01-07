import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

opts = {
    'alias': ('зиро', 'зайро', 'зеро', 'ира', 'зира', 'иро' ),
    'tbr': ('скажи', 'расскажи', 'покажи', 'сколько', 'произнести',),
    'cmds': {
        "ctime": ('текущее время', 'сейчас времени', 'который час',),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио',),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анектоды',)
    }
}
# Функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, Language='ru-Ru').lower()
        print('[log] Распознано: ' + voice)

        if voice.startswith(opts['alias']):

            cmd = voice

        for x in opts['alias']:
            cmd = cmd.replace(x, "").strip()

        for x in opts['tbr']:
            cmd = cmd.replace(x, "").strip()

        #распазнаем и выполняем команду

        cmd = recognizer_cmd(cmd)
        execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print('[logo] Голос не распознано!')
    except sr.RequestError as e:
        print('[logo] Неизвестная ошибка, проверьте интернет!')


def recognizer_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd,x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak('Сейчас' + str(now.hour) + ':' + str(now,min))

    elif cmd == 'radio':
        os.system("D:\\Python\\res\\radio_record.m3u")
    elif cmd == 'stupid1':
        speak("Мой создатель не научил меня аниктодам ... Ха ха")

    else:
        print('Команда не распознано, повторите!')
# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)

with m as  source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[4].id)

speak('Добрый день, создатель')
speak('Зиро слушает')

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)