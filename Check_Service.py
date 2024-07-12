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


#@staticmethod
class Service:
    @property
    def lang(self):
        return self.__lang__
    
    @property
    def osDetected(self):
        return self.__osdetected
        
    def __init__(self, lang, os_detected):
        self.__lang__=lang
        self.__osdetected=os_detected
    
    def checkname(self, varService:str ):
        if self.osDetected=="windows":
            raise NotImplementedError(self.__class__.__name__ )
        elif self.osDetected == "linux":
            self.lin_checkname(varService)
    
    
    
    def lin_checkname(self, varService: str):
        #print(f"\tTest du nom de {varService}")
        #subprocess.Popen(f"systemctl status {varService}",  shell=True,stdout=subprocess.PIPE)
        check = subprocess.run(["systemctl", "status", varService], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if (b"could not be found" in check.stderr):
            DxHelios.Say(self, f"{self.lang['service_test']} {varService} : {self.lang['failed']}",1,1)
            raise ValueError(f"{self.lang['err_unknownservice']} {varService}")
            
        DxHelios.Say(self, f"{self.lang['service_test']} {varService} : {self.lang['success']}",1,1)
                
    
            
    def checkservice(self, varService:str):
        DxHelios.Say(self, f"Test de {varService}",1,1)
        
        if self.osDetected=="windows":
            raise NotImplementedError(self.__class__.__name__ ) 
        elif self.osDetected == "linux":
            return self.lin_checkservice(varService)

    
    def lin_checkservice(self, varService: str):
        
        check = subprocess.run(["systemctl", "is-active", varService], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(check.stdout)
        #active service
        if check.stdout.startswith(b"active"):  # Warning : result may end in a newline: b"active\n"
            return True
                
        #inactive service        
        return False
