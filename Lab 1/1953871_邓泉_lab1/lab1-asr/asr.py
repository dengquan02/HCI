from PyQt5 import QtWidgets, QtGui, QtCore, uic
# from PySide2.QtCore import Signal, QObject
from asrInterface import Ui_MainWindow
import sys
import win32api
from guessTheWord import recognize_speech_from_mic
import speech_recognition as sr
from threading import Thread, Lock
from time import sleep
import operator

# 自定义信号源对象类型，继承自QObject
class MySignals(QtCore.QObject):
    text_print = QtCore.pyqtSignal(str, str, str)

class myWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 实例化
        self.ms = MySignals()
        # 自定义信号的处理函数
        self.ms.text_print.connect(self.updateGui)

        thread = Thread(target=self.monitor_execute)
        thread.setDaemon(True)  # 设置daemon参数值为True:Python程序中当所有的 `非daemon线程` 结束了，整个程序才会结束。
        thread.start()

    def updateGui(self, color, text, icon="icon/voice.gif"):
        # 锁定
        lock.acquire()
        try:
            # 修改提示字段
            self.ui.label_6.setStyleSheet(color)
            self.ui.label_6.setText(text)
            # 更换voiceFig
            self.ui.gif = QtGui.QMovie(icon)
            self.ui.voiceFig.setMovie(self.ui.gif)
            self.ui.gif.start()
        finally:
            # 释放
            lock.release()

    def monitor_execute(self):
        i = 1
        while True:
            # self.ms.text_print.emit("color: rgb(100, 177, 10);", "please speak...")
            print(f"开始识别，第{i}轮")

            # 一直等待指令，直到得到指令（API访问错误、其他错误）时退出该循环
            while True:
                self.ms.text_print.emit("color: rgb(100, 177, 10);", "Please speak...", "icon/voice.gif")
                # create recognizer and mic instances
                recognizer = sr.Recognizer()
                microphone = sr.Microphone()
                response = recognize_speech_from_mic(recognizer, microphone)
                # a transcription is returned
                if response["transcription"]:
                    break
                # API request failed
                if not response["success"]:
                    break
                # API request succeeded but no transcription was returned
                self.ms.text_print.emit("color: #FFE7BA;", "I didn't catch that. What did you say?", "icon/voice.gif")
                sleep(2)

            # if there was an error, stop the game
            if response["error"]:
                print("ERROR: {}".format(response["error"]))
                self.ms.text_print.emit("color: #FFE7BA;", "ERROR: {}".format(response["error"]), "icon/voice.gif")
                sleep(2)
                continue;

            result = response["transcription"]
            # show the user the transcription
            print("You said: {}".format(result))
            self.ms.text_print.emit("color: #FFD700;", "You said : {}".format(result), "icon/voice.gif")
            sleep(2)
            flag = 0 # 1-成功 0-失败
            target = None
            # operator模块是python中内置的操作符函数接口，它定义了一些算术和比较内置操作的函数。
            # operator.contains(seq, obj)：包含测试 -- obj in seq
            if result.lower() == "play music":
                win32api.ShellExecute(0, 'open', 'f1lcapae.wav', '', '', 1)
                flag = 1
                target = "music"
            elif result.lower() == "open notepad":
                win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)
                flag = 1
                target = "notepad"
            elif result.lower() == "open browser":
                win32api.ShellExecute(0, 'open', 'https://shenyingtongji.gitee.io/home/course/HCI2022Spring/index.html', '', '', 1)
                flag = 1
                target = "browser"
            #
            elif operator.contains(result.lower(), "m") and operator.contains(result.lower(), "u") and operator.contains(result.lower(), "s"):
                win32api.ShellExecute(0, 'open', 'f1lcapae.wav', '', '', 1)
                flag = 1
                target = "music"
            elif operator.contains(result.lower(), "no") and operator.contains(result.lower(), "a") and operator.contains(result.lower(), "d"):
                win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)
                flag = 1
                target = "notepad"
            elif operator.contains(result.lower(), "b") and operator.contains(result.lower(), "ow") and operator.contains(result.lower(), "ser"):
                win32api.ShellExecute(0, 'open', 'https://shenyingtongji.gitee.io/home/course/HCI2022Spring/index.html', '', '', 1)
                flag = 1
                target = "browser"
            if flag != 1:
                print("识别失败")
                self.ms.text_print.emit("color: #FF0000;", "There is no matching operation. Please try again...", "icon/voice.gif")
                sleep(3)
            else:
                print("识别成功")
                self.ms.text_print.emit("color: rgb(100, 200, 100);", f"{target}...", f"icon/{target}.gif")
                sleep(3)
            # 进入下一轮识别
            i += 1


if __name__ == "__main__":
    lock = Lock()
    app = QtWidgets.QApplication(sys.argv)
    application = myWindow()
    application.show()
    sys.exit(app.exec())
