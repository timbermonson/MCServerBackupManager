import MCServer
import BackupManager
from logger import log

import os
import time
import threading

# Configuration variables ------------------------------
backupCheckDelayInSeconds = 1800

startFile = os.path.normpath("../start.bat")

backupDir = os.path.normpath("D:\\MCServer\\Backups")
serverDir = os.path.normpath("../")
folderNames = ["world", "world_nether", "world_the_end", "logs", "plugins"]
fileNames = ["banned-ips.json", "banned-players.json", "bukkit.yml", "ops.json",
             "permissions.yml", "server.properties", "spigot.yml", "whitelist.json"]

backupConfig = {"backupDir": backupDir, "serverDir": serverDir,
                "folderNames": folderNames, "fileNames": fileNames}
# ------------------------------------------------------

backupManager = BackupManager.BackupManager(backupConfig)
mcServer = MCServer.MCServer(startFile)


def startup():
    print("--------STARTUP----------")

    log("starting server...")
    mcServer.start()
    log("server started!")

    print("-------------------------")
    startBackupChecker()
    mcServer.startInputLoop()


def startBackupChecker():
    print("---------BACKUP----------")
    log("checking backup...")
    curDate = backupManager.getDate()

    if backupManager.checkBackupExists(curDate):
        log("today's backup found!")
    else:
        log("today's backup not found.")
        startBackup(curDate)

    print("-------------------------")
    threading.Timer(backupCheckDelayInSeconds, startBackupChecker).start()


def startBackup(name):
    log("stopping server...")
    mcServer.stop(lambda: finishBackup(name))


def finishBackup(name):
    log("server stopped!")

    log("making backup...")
    backupManager.makeBackup(name)
    print("done!")

    log("restarting server...")
    mcServer.start()
    log("server started!")


startup()
