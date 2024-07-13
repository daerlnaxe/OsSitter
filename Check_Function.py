"""
Auteur : Alexandre CODOUL
Version: Alpha 4
TODO:
- Add argument to replace $varService
- Add Windows Compatibility
"""
import subprocess
import sys
from DxHelios import DxHelios
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
        
        # Return true if res greater than test
        if(alert.nom== "freemem" ):
            DxHelios.Say(self, f"freemem",1,1)

            res=self.freememoryperc()
            print (res)
            return  res > int(alert.trigger) , res
        elif(alert.nom=="freecpu"):
            DxHelios.Say(self, f"freecpu",1,1)

            res=self.freecpuperc()
            print (res)
            return  res > int(alert.trigger) , res
        
        elif(alert.nom=="freediskspace"):
            DxHelios.Say(self, f"freediskspace",1,1)

            res=self.freediskspaceperc(alert)
            print (res)
            return  res > int(alert.trigger) , res
        
            
        elif(alert.nom=="freediskinode"):
            DxHelios.Say(self, f"freediskinode",1,1)

            res=self.freediskinodeperc(alert)
            print (res)
            return  res > int(alert.trigger) , res

        



    # Memory
    ## Get used memory in percent
    def freememoryperc(self):
        rra=[]
        with open('/proc/meminfo') as f:
            rra=f.read().split('\n')

        result=int(re.search("[0-9]+", rra[1]).group(0)) * 100 / int(re.search("[0-9]+", rra[0]).group(0))
        print( result)
        return result



    # CPU
    def freecpuperc(self):
        values=[]
        with open('/proc/stat') as f:
            line=f.readline()
            print (line)
            tmp=line.replace('\n','').replace("cpu  ",'').split(' ')
            values=list(map(int,tmp))

        result=int(values[3])*100/ sum(values)
        print(result)
        return result
        
        
    # Disk
    ## Free Space
    def freediskspaceperc(self, alert):
        print(alert.param)
        tmp=subprocess.run(["df","-h", alert.param], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        err=(tmp.stderr).decode('utf-8')
        
        
        # in case of error
        #if(len(tmp)==1):
         #   print(tmp)
            
        tmp=(tmp.stdout).decode('utf-8').split('\n')[1]
        tmp=re.sub(r'\s+', ' ', tmp)
        result=int(tmp.split(' ')[4].replace('%',''))

        return 100- result
        
        
    def freediskinodeperc(self, alert):
        
        tmp=subprocess.run(["df","-i", alert.param], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        err=(tmp.stderr).decode('utf-8')
               
        
        # in case of error
        #if(len(tmp)==1):
        #    print(tmp)
        #    DxHelios.Say(self, tmp)
           
        tmp=(tmp.stdout).decode('utf-8').split('\n')[1]
        tmp=re.sub(r'\s+', ' ', tmp)
        result=int(tmp.split(' ')[4].replace('%',''))

        return 100- result
        