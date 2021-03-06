# Голосовой ассистент ГЕНА 1.0 BETA
import os 
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройка
opts = {
	"alias" : ('гена', 'генка', 'генчик', 'гендос', 'гиндос','геннадий', 'гина', 'генадий', 'гинадий',
		'гиннадий', 'кена', 'кенка', 'кенчик', 'кендос', 'киндос'),
	"tbr" : ('скажи', 'произнеси', 'озвучь', 'сколько', 'расскажи'),
	"cmds" : {
		"ctime" : ('текущее время', 'который час', 'сейчас времени', 'сейчас время'),
		"radio" : ('включи радио', 'запусти радио', 'включи музыку', 'воспроизведи радио'),
		"stupid1" : ('расскажи анекдот', 'ты знаешь анекдоты', 'анекдот', 'рассмежи меня')
	}
}

# функции
def speak(what):
	print( what )
	speak_engine.say( what )
	speak_engine.runAndWait()
	speak_engine.stop()

def callback(recognizer, audio):
	try:
		voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
		print("[log] Распознано: " + voice)

		if voice.startswith(opts["alias"]):
			# обращения к Гене
			cmd = voice

			for x in opts['alias']:
				cmd = cmd.replace(x, "").strip()

			for x in opts['tbr']:
				cmd = cmd.replace(x, "").strip()

			# распознаём и выполняем команду
			cmd = recognize_cmd(cmd)
			execute_cmd(cmd['cmd'])	

	except sr.UnknownValueError:
		print("[log] Голос не распознан!")
	except sr.RequestError as e:
		print("[log] Непонятно, кхм... Проверьте интернет!")

def recognize_cmd(cmd):
	RC = {'cmd': '', 'percent': 0}
	for c,v in opts['cmds'].items():

		for x in v:
			vrt = fuzz.ratio(cmd, x)
			if vrt > RC['percent']:
				RC['cmd'] = c
				RC['percent'] = vrt

	return RC

def execute_cmd(cmd):
	if cmd == 'ctime':
		# сказать текущее время
		now = datetime.datetime.now()
		speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

	elif cmd == 'radio':
		# воспроизвести радио
		os.system("D:\\Jarvis\\res\\radio_record.m3u")

	elif cmd == 'stupid1':
		# рассказать анекдот
		speak("Мой разработчик не научил меня анектодам... Ха-ха.")

	else:
		print('На эту тему я не хочу разговаривать, давай поговорим о другом')

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)

with m as source:
	r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если установлены другие голоса для синтеза речи
#voices = speak_engine.hetProperty('voices')
#speak_engine.setProperty('voice', voices[№].id)	

speak("Добрый день, мой дорогой программер, или кто ты там")
speak("Геннадий слушает")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)

#	while True:
#	    with m as source:
#	        audio = r.listen(source)
#	    callback(r, audio)
#	    time.sleep(0.1)