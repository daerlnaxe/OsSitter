"""
Auteur : Alexandre CODOUL
Version: Alpha 4
TODO:
- Add argument to replace $varService
- Add Windows Compatibility
"""
import subprocess
import sys
import DxHelios
import re


#@staticmethod
class Function:
    @property
    def lang(self):
        return self.__lang__

    # OS detection Accessor
    @property
    def osDetected(self):
        return self.__osdetected

    # Builder    
    def __init__(self, lang, os_detected):
        self.__lang__=lang
        self.__osdetected=os_detected

   
            
    def getresult(self, alert):
        DxHelios.Say(self, f"Function {alert.nom}",1,1)

        if(alert.nom== "mem" ):
            DxHelios.Say(self, f"mem",1,1)

            res=self.freepercmemory()
            print (res)
            return  res < int(alert.trigger) , res


        

    # Memory
    ## Get free memory in percent
    def freepercmemory(self):
        rra=[]
        with open('/proc/meminfo') as f:
            rra=f.read().split('\n')

        result=int(re.search("[0-9]+", rra[1]).group(0)) * 100 / int(re.search("[0-9]+", rra[0]).group(0))
        print( result)
        return result



