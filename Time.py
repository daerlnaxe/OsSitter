#import datetime
from datetime import datetime, timedelta

# Return horodating for the log entries
#    @property
def timeHoroDLog(self):
        return "%Y-%m-%d %H:%M:%S"

# Return horodating for the file log
    #@property
def timeHoroDFile(self):
        return "%Y%m%D_%H%M%S"