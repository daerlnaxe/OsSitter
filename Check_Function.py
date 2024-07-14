"""
Auteur : Alexandre CODOUL
Version: Alpha 4
TODO:
- Add argument to replace $varService
- Add Windows Compatibility
"""
import subprocess
import sys
import re
from DxHelios import DxHelios


#@staticmethod
class Function:
    Helios=None

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
        self.Helios.Say(self, f"Function {alert.nom}",1,1)
        
        # Return true if res greater than test
        if(alert.nom== "freemem" ):
            self.Helios.Say(self, f"freemem",1,1)

            res=self.freememoryperc()
            print (res)
            return  res > int(alert.trigger) , res
        elif(alert.nom=="freecpu"):
            raise("deprecated")
            #self.Helios.Say(self, f"freecpu",1,1)

            #res=self.freecpuperc()            
            #return  res > int(alert.trigger) , res
        elif(alert.nom=="freevscpu"):
            self.Helios.Say(self, f"freevscpu")
            res=self.freevscpuperc()
            
            return res > int(alert.trigger), res
            
        elif(alert.nom=="freediskspace"):
            self.Helios.Say(self, f"freediskspace",1,1)

            res=self.freediskspaceperc(alert)
            return  res > int(alert.trigger) , res
        
            
        elif(alert.nom=="freediskinode"):
            self.Helios.Say(self, f"freediskinode",1,1)

            res=self.freediskinodeperc(alert)
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




    
    def freevscpuperc(self):
        check = subprocess.run(["vmstat", "1", "2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tmp=(check.stdout).decode('utf-8').split('\n')[3]
        # replace n space by a space, then split by space
        tmp=re.sub(r'\s+', ' ', tmp.strip()).split(' ')
        print(f"vscpu: tmp[14]")
        
        return int(tmp[14])
    
        
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
        #    self.Helios.Say(self, tmp)
           
        tmp=(tmp.stdout).decode('utf-8').split('\n')[1]
        tmp=re.sub(r'\s+', ' ', tmp)
        result=int(tmp.split(' ')[4].replace('%',''))

        return 100- result
        