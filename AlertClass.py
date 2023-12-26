class Alert:
    # Alert Name
    @property
    def nom(self):
        return self.__nom

    # Alert Type
    @property
    def typeA(self):
        return self.__typeA
    
    # Alert Timer
    @property
    def timer(self):
        return self.__timer
       
    @property
    def delay_alarm(self):
        return self.__delay_alarm
    
    # Cycle Alert, timer before send alert
    cycle_alert=0
        
    # Mark you must alert
    state=None

    
    
    #Next Execution
    next_execution=None
    
    #Next alarm
    next_alarm=None
    
    def __init__(self,nom: str,typeA: str, timer: int, delay_alarm: int):
        print("meee")
        print(delay_alarm)
        self.__nom = nom
        self.__typeA=typeA
        self.__timer=timer
        self.__delay_alarm=delay_alarm

    @classmethod
    def dict_toAlert(self, adict:dict):
        return Alert(adict["nom"], adict["typeA"], adict["timer"], adict["delay_alarm"])
        
   
