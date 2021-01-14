from datetime import datetime

def log(message):
    timeString = datetime.now().strftime("%H:%M:%S")
    prefix = "[" + timeString + "] [Manager]: "
    
    print(prefix + str(message))
