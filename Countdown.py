import threading

countdownHOUR = 2
countdownMINUTE = 1
countdownSECOND = 0


class Countdown:
    amount = None
    unit = None
    countCallback = None
    finishCallback = None
    delayInSeconds = None

    currentCount = 0
    isFinished = True

    def __init__(self, config):
        self.validateParams(config)

        self.amount = config["amount"]
        self.unit = config["unit"]
        self.countCallback = config["countCallback"]
        self.finishCallback = config["finishCallback"]

        if(self.unit == countdownHOUR):
            self.delayInSeconds = 3600
        elif(self.unit == countdownMINUTE):
            self.delayInSeconds = 60
        elif(self.unit == countdownSECOND):
            self.delayInSeconds = 1
        else:
            raise Exception(
                "I dunno how this branch could be reached, but ya messed up")

    def validateParams(self, config):
        if(config["amount"] is None or not isinstance(config["amount"], int)):
            raise Exception("config.amount is not a valid int.")

        if((config["unit"] is None) or (not isinstance(config["unit"], int)) or config["unit"] < countdownSECOND or config["unit"] > countdownHOUR):
            raise Exception("config.unit is not a valid unit.")

        if(config["countCallback"] is None or not hasattr(config["countCallback"], '__call__')):
            raise Exception("config.countCallback is not a valid function.")

        if(config["finishCallback"] is None or not hasattr(config["finishCallback"], '__call__')):
            raise Exception("config.finishCallback is not a valid function.")

    def startCountdown(self):
        self.isFinished = False
        self.currentCount = self.amount
        self.doCountdown()

    def doCountdown(self):
        if(self.isFinished == True):
            return
        if(self.currentCount <= 0):
            self.isFinished = True
            self.finishCallback()
            return

        self.countCallback(self.currentCount)
        self.currentCount = self.currentCount - 1

        threading.Timer(self.delayInSeconds, self.doCountdown).start()
