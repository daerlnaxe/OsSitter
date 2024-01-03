"""
Auteur : Alexandre CODOUL
Version: 1.0
TODO:
- Add argument to replace $varService
- Ajouter une compatibilité Windows
"""
import subprocess
import sys



#@staticmethod
class Service:
    @staticmethod
    def lin_checkname(varService: str):
        #print(f"\tTest du nom de {varService}")
        #subprocess.Popen(f"systemctl status {varService}",  shell=True,stdout=subprocess.PIPE)
        check = subprocess.run(["systemctl", "status", varService], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if (b"could not be found" in check.stderr):
            print("\tTest échoué pour {varService}")
            raise ValueError(">>>Le service est inconnu, veuillez modifier le fichier de configuration")
            
        print(f"\tTest réussi pour {varService}")
                

            
        
    @staticmethod
    def lin_checkservice(varService: str):
        print(f"Test de {varService}")
        check = subprocess.run(["systemctl", "is-active", varService], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(check.stdout)
        #active service
        if check.stdout.startswith(b"active"):  # Warning : result may end in a newline: b"active\n"
            return True
                
        #inactive service        
        return False
