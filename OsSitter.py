#! /usr/bin/env python3
# coding: utf-8

"""
Auteur: Alexandre Codoul
Version: alpha 2.1
Requiert Python 3.6
Todo:
- Horodatage -> module à part
- Détection sortie clavier
- Détection reboot machine
- Envoyer mail au chargement
Features:
- Loop by /60s
- Load new config file if there is a file named 'new-config.json'
- Tests on init

Linux :
- Background launch : nohup ./OsSitter.py &
- Seein pid : ps -aux | grep OsSitter | grep -v grep
- Killing process : kill <pid>

"""

import os
import sys
import time 
from AlertClass import Alert
from Config import Config
from Check_Service import Service
from SendMail import Mails
from datetime import datetime, timedelta
# Used to detect when stopped
import atexit 
# User to intercept sigkill and ...
import signal


class OsSitter(object):
    @property
    def timeFormat(self):
        return "%Y-%m-%d %H:%M:%S"

    @property
    def osDetected(self):
        return self.__osDetected

    @property
    def config(self):
        return self.__config
    
    @property
    def debugMode(self):
        return self.__debugMode
    
    #debugMode=None
    
    @staticmethod
    def myself():
        return self._instance
    
    def stop(sig, frame):
        global stopped
        stopped = True
        out.write('caught SIGTERM\n')
        out.flush()
        ACiao()

    def ignore(sig, frsma):
        out.write('ignoring signal %d\n' % sig)
        out.flush()
        ACiao()



    _instance = None       # Attribut statique de classe
 
    def __new__(cls): # __new__ classmethod implicite: la classe 1e paramètre
        print("méthode de construction standard")
        if cls._instance is None:
            print("construction")
            cls._instance = object.__new__(cls)
        return cls._instance


    def __init__(self):
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.ignore)

    
        print("Initialisation : {}".format(datetime.now().strftime(self.timeFormat)))
        # Check OS
        # its win32, maybe there is win64 too?

        if sys.platform.startswith('win'):
            self.__osDetected="windows"
        elif sys.platform.startswith('linux'):
            self.__osDetected="linux"

        print( f"\tOS detecté: {self.osDetected}")
        # Chargement de la configuration
        print("\tChargement de la configuration")
                
        self.__config= Config.Factory()
        self.__debugMode= self.config.parameters.debug


        if self.debugMode:
            print("\tDebug mode activated")
            
            print(self.config.__repr__())
            print(f"\tParamètres : {self.config.parameters}")
            # Affichage des paramètres mails
     

     

    # Send a mail "stopped service"
    def manage_stoppedservice(self, alert: Alert):
        mail_params=self.config.parameters.mail
        server_params=self.config.parameters

        
        print("manage stopped service")
        print(alert.next_alarm)
        print(alert.delay_alarm)
        
        # Keep a respectuous mail flow
        if alert.next_alarm == None or datetime.now() > alert.next_alarm:
            # Creation of the object to send mails
            mails=Mails()
            
            # Show informations for debug mode
            if self.debugMode:
                print(f"Mails: {mail_params}")
                        
                                        
            message =f"""Message de {server_params.server_name}:
                    
    Attention le service '{alert.nom}' est stoppé !
             
            
    Mail généré par OsSitter.py
                    """
            print(mail_params.sender)
            #mails.Send(f"Etat du serveur '{server_params.server_name}'" , message, mail_params.sender, mail_params.get_toList(), mail_params.get_ccList(), mail_params.get_cciList());
            mails.Send(mail_params.sender,f"Etat du serveur '{server_params.server_name}'" , message, mail_params);
            
            print(f"{alert.nom} envoi de mail")
            
            # Assignation de la prochaine alerte
            alert.next_alarm = datetime.now() + timedelta(minutes=alert.delay_alarm)
            print(f"Prochaine alarme programmée: {alert.next_alarm}")
        else:
            print(f"{alert.nom}: pas d'envoi de mail avant {alert.next_alarm}")


    # Send a mail "restarted service"
    def manage_restartedservice(self, alert: Alert):
        mail_params=self.config.parameters.mail
        server_params=self.config.parameters

        mails=Mails()
        print(f"{alert.nom} envoi de mail restarted")
        message =f"""Message de {server_params.server_name}:
                    
    Attention le service '{alert.nom}' est redémarré !
             
            
    Mail généré par OsSitter.py
                    """
        print(mail_params.sender)
        #mails.Send(f"Etat du serveur '{server_params.server_name}'" , message, mail_params.sender, mail_params.get_toList(), mail_params.get_ccList(), mail_params.get_cciList());
        mails.Send(mail_params.sender,f"Etat du serveur '{server_params.server_name}'" , message, mail_params);


    # Signal when program is stopped
    # Using register() as a decorator  
    @atexit.register  
    def ACiao(): 
        obj= OsSitter()
        print(obj)
        print(type(obj))
        mail_params=obj.config.parameters.mail
        server_params=obj.config.parameters

        mails=Mails()
        print(f"Envoi de mail Arrêt du programme")
        message =f"""Message de {server_params.server_name}:
                    
    Arrêt de OsSitter à {datetime.now()} !
             
    Le serveur n'est plus surveillé ou a été redémarré.
                    """
       
        mails.Send(mail_params.sender,f"Arrêt du serveur '{server_params.server_name}'" , message, mail_params);
     




    """
    Test 
    """
    def test(self):
        print("Tests")        
        
        # Check services names
        for alert in self.config.alerts:
            if alert.typeA =="service" :
                if self.osDetected=="windows":
                    raise NotImplementedError(self.__class__.__name__ )
                elif self.osDetected == "linux":
                    alert.state=Service.lin_checkname(alert.nom)
                    
                    
        # Test mail - Si tout est ok
        mail_params=self.config.parameters.mail
        server_params=self.config.parameters
        # Creation of the object to send mails
        mails=Mails()
        message =f"""\Supervision activée sur de {server_params.server_name}.
        """
        print(mail_params.sender)
        #mails.Send(f"Etat du serveur '{server_params.server_name}'" , message, mail_params.sender, mail_params.get_toList(), mail_params.get_ccList(), mail_params.get_cciList());
        mails.Send(mail_params.sender,f"Initialisation de la surveillance de '{server_params.server_name}'" , message, mail_params);
            
        print(f"\tenvoi de mail")


                



    # Begining
    def main(self):
        # Assign
        server_params=self.config.parameters
        mail_params=self.config.parameters.mail
        # debugMode
        
        print("Démarrage : {}".format(datetime.now().strftime(self.timeFormat)))


        # Initialisation
        obj=datetime.now()
        print(type(obj))
        print(obj.date)


        """
        import inspect
        for attr in inspect.getmembers(obj):
            # Avoiding dunder methods
            if not attr[0].startswith("__"):
                print(attr)
        """

        #config.InitAlerts(datetime.now())


        while(True):

            
            if os.path.isfile("./new-config.json"):
                print("Nouvelle configuration détectée: Chargement")
                try:
                    new_config= Config.Factory()
                    self.__config=new_config
                    os.remove("./config.json")
                    os.rename("./new-config.json", "./config.json")
                    self.__debugMode = server_params.debug
                    self.__config.InitAlerts(datetime.now())

                    
                except Exception as exc:
                    print("Erreur de chargement du nouveau fichier, chargement refusé")
                    print(exc)
                    

             
            #print(type(config))
            #print(type(config.alertes))


                
            # Stop All
            if self.config.parameters.stop==True:
                break;


            #result = map (lambda x:x['address'], mail_params.to)
            #print(list(result))
            #result = mail_params.get_toList()
            #result = mail_params.get_ccList()
            #result = mail_params.get_cciList()
            
            
            for alert in self.config.alerts:
                # Debug Mode -> show alert informations
                if self.debugMode:
                    print("typealerte")
                    print(type(alert))
                    print("Il est: {}".format(datetime.now()))
                    print(f"Prochaine éxécution: {alert.next_execution}")

                # Traitement de l'alerte
                if alert.typeA =="service" :
                    old_state=alert.state
                    # Check alert
                    if alert.next_execution == None or  datetime.now() > alert.next_execution :            
                        print(f"Traitement de l'alerte {alert.nom} de type {alert.typeA}")
                   
                                    
                        if self.osDetected=="windows":
                            raise NotImplementedError(self.__class__.__name__ ) 
                        elif self.osDetected == "linux":
                            alert.state=Service.lin_checkservice(alert.nom)
                        
                        self.config.set_nextexecution(alert)
                        print(f"Réglage de la prochaine éxécution : {alert.next_execution}")

                        # Gestion du check    
                        if self.debugMode:
                            print(f"Etats, check: {alert.state} | old_state: {old_state}")
                           

                    # No check                    
                    else:
                        print(f"Prochain check du service {alert.nom} : {alert.next_execution}")
                    
                    
                    if old_state==None:
                        old_state=alert.state

                    # Alerting
                    if old_state and alert.state:
                        print(f"Service {alert.nom}: opérationnel")
                    elif old_state is False and alert.state:                    
                        print(f"Service {alert.nom}: redémarré")
                        self.manage_restartedservice( alert)                
                    elif alert.state is False:  
                        print(f"Service {alert.nom}: stoppé")
                        self.manage_stoppedservice( alert)
                    else:
                        raise ValueError("Le paramètre entré ne correspond pas au type attendu")                
                                    
                        
                    
            # Time to Sleep (see 
            print(f"Wake me up in {self.config.parameters.sleeper * 60 }s\n\n")
            time.sleep(self.config.parameters.sleeper * 60)
            
    
        print("don't stop me now")


# Starting point    
if __name__ == '__main__':    
    sup = OsSitter()
    sup.test()
    
    # Sys.exit to signal why
    sys.exit(sup.main())  # need to bettter use sys.exit
