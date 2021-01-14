import datetime
import os
import shutil
import time

class BackupManager:
    backupDir = ""
    serverDir = ""
    folderNames = []
    fileNames = []

    def __init__(self, config):
        self.validateParams(config)

        self.backupDir = config["backupDir"]
        self.serverDir = config["serverDir"]
        self.folderNames = config["folderNames"]
        self.fileNames = config["fileNames"]

    def validateParams(self, config):
        if (config["backupDir"] is None) or not os.path.isdir(config["backupDir"]):
            raise Exception("config.backupDir is not set to a valid path.")

        if (config["serverDir"] is None) or not os.path.isdir(config["serverDir"]):
            raise Exception("config.serverDir is not set to a valid path.")

        if (config["folderNames"] is None) or not isinstance(config["folderNames"], list):
            raise Exception("config.folderNames is not an array.")

        for folderName in config["folderNames"]:
            folderPath = os.path.join(config["serverDir"], folderName)

            if not os.path.isdir(folderPath):
                raise Exception("folderName " + folderName + " is invalid.")

        if (config["fileNames"] is None) or not isinstance(config["fileNames"], list):
            raise Exception("config.fileNames is not an array.")

        for fileName in config["fileNames"]:
            filePath = os.path.join(config["serverDir"], fileName)

            if not os.path.isfile(filePath):
                raise Exception("fileName " + fileName + " is invalid.")

    def getDate(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%p"))

    def checkBackupExists(self, name):
        backupPath = os.path.join(self.backupDir, name)
        backupPathExists = os.path.isdir(backupPath)
        return backupPathExists

    def makeBackup(self, name):
        if (self.checkBackupExists(name)):
            raise Exception("makeBackup must be called with a backup name that doesn't exist!")

        backupPath = os.path.join(self.backupDir, name)
        os.mkdir(backupPath)

        for folderName in self.folderNames:
            folderPath = os.path.join(self.serverDir, folderName)
            folderBackupPath = os.path.join(backupPath, folderName)
            shutil.copytree(folderPath, folderBackupPath)

        for fileName in self.fileNames:
            filePath = os.path.join(self.serverDir, fileName)
            fileBackupPath = os.path.join(backupPath, fileName)
            shutil.copyfile(filePath, fileBackupPath)
