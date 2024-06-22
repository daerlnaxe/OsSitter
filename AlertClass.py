"""
Auteur : Alexandre CODOUL
Version: Alpha 4
"""
class Alert:
    # Alert Name
    @property
    def nom(self):
        return self.__nom

    """
    Optionnal
    """
    # Alert Type
    @property
    def typeA(self):
        return self.__typeA

    # Alert param
    @property
    def param(self):
        return self.__param
 
    """
    Optionnal
    """
 
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
    def __init__(self,nom: str,typeA: str, param: str,trigger: str, timer: int, delay_alarm: int):                
        self.__nom = nom
        self.__typeA=typeA
        self.__param=param
        self.__trigger=trigger
        self.__timer=timer
        self.__delay_alarm=delay_alarm


    @classmethod
    def dict_toAlert(self, adict:dict):
        typeA= adict["typeA"] 
        nom=adict["nom"]
        param=adict.get("param")
        trigger=adict.get("trigger")


        if( typeA =="function"):
            
            if(trigger==None):
                raise Exception(f"Function {nom}: Trigger is null")
            elif((adict["nom"] != "freemem" and adict["nom"]!= "freecpu") and param==None):
                raise Exception(f"Function {nom}: Param is null")
        
        return Alert(adict["nom"], adict["typeA"], param, trigger,adict["timer"], adict["delay_alarm"])
        """elif (typeA=="function"):
            if(nom=="freemem"):
                return Alert(adict["nom"], adict["typeA"], adict["trigger"],adict["timer"], adict["delay_alarm"])
            else):
                return Alert(adict["nom"], adict["typeA"], adict[""],adict["trigger"],adict["timer"], adict["delay_alarm"])
        """
   
    """
    Showing Content 
    """        
    def __repr__(self):
        return str(self.__dict__)
