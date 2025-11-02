#import datetime
from datetime import datetime, timedelta

# Return horodating for the log entries
#    @property
timeHoroDLog = "%Y-%m-%d %H:%M:%S"

# Wrning %D => /
# Return horodating for the file log
    #@property
timeHoroDFile = "%Y%m%d_%H%M%S"


#def getNowHoroDLog(self):
def getNowHoroDLog():        
        return datetime.now().strftime(timeHoroDLog)


def getNowHoroDFile():
        return datetime.now().strftime(timeHoroDFile)