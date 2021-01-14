import os
import re
import time
import psutil
import subprocess
import sys
import threading
from subprocess import PIPE

import Countdown


class MCServer:
    process = None
    startFile = None
    isDone = False
    serverDoneText = "[Server thread/INFO]: Done"
    countdownManager = None

    stopCallback = None

    def __init__(self, startFile):
        self.validateParams(startFile)
        self.startFile = startFile

        countdownConfig = {
            "unit": Countdown.countdownMINUTE,
            "amount": 5,
            "countCallback": self.sendStopCountdownMessage,
            "finishCallback": self.stopServer
        }
        self.countdownManager = Countdown.Countdown(countdownConfig)

    def validateParams(self, startFile):
        if(os.path.isfile(startFile) == False):
            raise Exception("startFile is not set to a valid (extant) file!")

    def serverIsStopped(self):
        if (self.process == None):
            return True
        if (self.process.poll() != None):
            return True
        return False

    def stop(self, stopCallback):
        if self.serverIsStopped():
            return
        self.stopCallback = stopCallback

        self.countdownManager.startCountdown()

    def sendStopCountdownMessage(self, count):
        self.sendCommand("say Server is rebooting in " +
                         str(count) + " minutes!")

    def stopServer(self):
        self.sendCommand("say Server is rebooting in 10 seconds!")
        time.sleep(10)

        self.isDone = False

        self.sendCommand("stop")
        while(self.serverIsStopped() == False):
            time.sleep(0.5)

        self.stopCallback()
        self.stopCallback = False

    def start(self):
        self.process = subprocess.Popen(
            self.startFile, stdin=PIPE, stdout=PIPE)
        self.startOutputThread()
        while(self.isDone == False):
            time.sleep(0.1)

    def sendCommand(self, command):
        encodedCommand = bytes(command+"\n", sys.getdefaultencoding())

        self.process.stdin.write(encodedCommand)
        self.process.stdin.flush()

    def readLine(self):
        rawLine = str(self.process.stdout.readline())
        regexMatch = re.findall("(?!b\\').*(?='$)", rawLine)

        if(len(regexMatch) < 1):
            return ""

        contents = regexMatch[0][1:]
        parsedContents = contents.replace("\\r\\n", "").replace("\\\\", "\\")

        return parsedContents

    def startOutputThread(self):
        if self.serverIsStopped():
            return

        while True:
            nextLine = self.readLine()
            if(len(nextLine) < 5):
                break
            if(self.serverDoneText in nextLine):
                self.isDone = True
            print(nextLine)

        threading.Timer(0.1, self.startOutputThread).start()

    def startInputLoop(self):
        while True:
            inp = input()
            self.sendCommand(inp)
            time.sleep(0.5)
