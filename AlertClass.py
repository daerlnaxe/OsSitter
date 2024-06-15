"""
Auteur : Alexandre CODOUL
Version: Alpha 4
"""
class Alert:
    # Alert Name
    @property
    def nom(self):
        return self.__nom

    # Alert Type
    @property
    def typeA(self):
        return self.__typeA

    # Alert Trigger
    @property
    def trigger(self):
        return self.__trigger
    
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

    # Builder
    def __init__(self,nom: str,typeA: str, trigger: str, timer: int, delay_alarm: int):                
        self.__nom = nom
        self.__typeA=typeA
        self.__trigger=trigger
        self.__timer=timer
        self.__delay_alarm=delay_alarm


    @classmethod
    def dict_toAlert(self, adict:dict):
        typeA= adict["typeA"] 
        if( typeA =="service"):
            return Alert(adict["nom"], adict["typeA"], "",adict["timer"], adict["delay_alarm"])
        elif (typeA=="function"):
            return Alert(adict["nom"], adict["typeA"], adict["trigger"],adict["timer"], adict["delay_alarm"])
        
   
    """
    Showing Content 
    """        
    def __repr__(self):
        return str(self.__dict__)
