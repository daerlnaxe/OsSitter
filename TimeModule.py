#import datetime
from datetime import datetime, timedelta

# Return horodating for the log entries
#    @property
def timeHoroDLog():
        return "%Y-%m-%d %H:%M:%S"

# Return horodating for the file log
    #@property
def timeHoroDFile():
        return "%Y%m%D_%H%M%S"


#def getNowHoroDLog(self):
def getNowHoroDLog():        
        return datetime.now().strftime(self.timeHoroDLog)