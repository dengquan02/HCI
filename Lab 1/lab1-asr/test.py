
import speech_recognition as sr
import win32api
from guessTheWord import recognize_speech_from_mic

# Working with audio files
r = sr.Recognizer()
# speech = sr.AudioFile('f1lcapae.wav')
# with speech as source:
#     audio = r.record(source)
# print(r.recognize_sphinx(audio))

# Working with Microphones
# mic = sr.Microphone()
# with mic as source:
#     r.adjust_for_ambient_noise(source)
#     audio = r.listen(source)
# # print(r.recognize_sphinx(audio))
# print(r.recognize_google(audio))

for i in range(10):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    response = recognize_speech_from_mic(recognizer, microphone)
    print(response)
# win32api.ShellExecute
# win32api.ShellExecute(0, 'open', 'notepad.exe', 'D:\\Desktop\\ToDo.txt','',1)
# win32api.ShellExecute(0, 'open', 'f1lcapae.wav', '','',1)
# win32api.ShellExecute(0, 'open', 'http://www.python.org', '', '', 1)
