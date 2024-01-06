"""
Auteur : Alexandre CODOUL
Version: Alpha 1.2
TODO:
"""

import json
import DxHelios
from typing import List
from AlertClass import Alert
from SendMail import Mail_Block, Mail_Obj
from datetime import datetime, timedelta


      

class Parameters_Obj:
    @property
    def server_name(self):
        return self.__server_name

    @property
    def debug(self):
        return self.__debug
        
    @property
    def stop(self):
        return self.__stop
    
    @property
    def sleeper(self):
        return self.__sleeper
        
    @property    
    def mail(self):
        return self.__mail
   
    def __init__(self, ServerName:str, Debug: bool,Sleeper:int, Stop: bool, Mail: Mail_Block):
        self.__debug=Debug
        self.__sleeper=Sleeper
        self.__stop=Stop
        self.__mail=Mail
        self.__server_name=ServerName
    
    @classmethod
    def dict_toParams(self, adict:dict):
        #print("dict_toParams",adict["Mail"])
        mail_block = Mail_Block.dict_toMailBlock(adict["Mail"])

        return Parameters_Obj(adict["ServerName"], adict["Debug"], adict["Sleeper"], adict["Stop"], mail_block)
       
    
    @classmethod
    def filler(Stop:bool, Sleeper: int, Mail: Mail_Block):
        return Parameters_Obj(Sleeper, Stop, Mail)
    
    """
    Showing Content 
    """        
    def __repr__(self):
        return str(self.__dict__)    

# Root for config object
class Config:
    @property
    def parameters(self):
        return self.__Parameters
    
    @property 
    def alerts(self):
        return self.__Alerts
        
        
    def __init__(self, Parameters: Parameters_Obj, Alertes: List[Alert]):        
        
        #        
        self.__Parameters= Parameters_Obj.dict_toParams(Parameters)

        #
        self.__Alerts = []
        
        for item in Alertes:
            self.__Alerts.append (Alert.dict_toAlert( item))
        
    
    """
    Showing Content 
    """
    def __repr__(self):
        return str(self.__dict__)
        
    """
    Initialize the next execution for alerts
    """    
    def InitAlerts(self, initTime: datetime):
        for alert in self.__Alerts:
            alert.next_execution=initTime
            print(f"{alert.nom} : {alert.next_execution}")
            
    def set_nextexecution(self, alert: Alert):
        alert.next_execution = datetime.now() + timedelta(minutes=alert.timer)

#alerte1=Alerte(typeA="service", nom="Bozd")
#team= Config(Alertes=[alerte1])

#print(team)

#json_data = json.dumps(team, default=lambda o: o.__dict__, indent=4)
#print(type(json_data))
#print(json_data)



    ## Deserialization
#decoded_team = Config(**json.loads(json_data))
#print(decoded_team)

#print(type(decoded_team))
 
#with open('config.json') as f:
   #json_data = json.load(f)



    # create Factory static method
    @staticmethod
    def Factory(filePath):
        DxHelios.Say("Config", f"Chargement du fichier de configuration: {filePath}",1)
            
        with open(filePath, "r") as f:
            json_data = f.read()

        #print(json_data)
        # Deserialization
        return Config(**json.loads(json_data))



 
