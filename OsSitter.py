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
import json 
import DxHelios
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
    def srv_params(self):
        return self.__srv_params
        
    @property
    def debugMode(self):
        return self.__debugMode
    
    @property
    def mail_params(self):
        return self.__mail_params
    
    @property
    def alerts(self):
        return self.__alerts
        
    #debugMode=None
    
    @staticmethod
    def myself():
        return self._instance
        
    def term_func(self, signum, frame):
        #global is_shutdown
        print(frame)
        print(signum)
        #is_shutdown = True
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SIGTERM: term_func')

    

    def term_method(self, signum, frame):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SIGTERM: term_method')
        mail_params=self.config.parameters.mail
        server_params=self.config.parameters

        mails=Mails()
        
        message =f"""{server_params.server_name} :
                    
    OsSitter a reçu un SIGTERM à {datetime.now()} !
             
    Le serveur n'est plus surveillé ou a été redémarré.
                    """
       
        mails.Send(mail_params.sender,f"Réception d'un SIGTERM pour '{server_params.server_name}'" , message, mail_params);
     
        print(f"------------ Envoi de mail SIGTERM")
        self.__stopped=True
     
        
    

    # Used to quit loop
    __stopped=False
    
    # Directory path
    __directory=None    

    # idk
    _instance = None       # Attribut statique de classe
 
    def __new__(cls): # __new__ classmethod implicite: la classe 1e paramètre
        #méthode de construction standard
        if cls._instance is None:
            print("CLS: construction")
            # Get directory
            cls.__directory=os.path.dirname(os.path.realpath(__file__))
        
            cls._instance = object.__new__(cls)
        return cls._instance

    """ Constructor
    """
    def __init__(self):
        # Prez
        print('#'*52)
        print('#' + ' '*50 + '#')
        
        #OsSitter: 8 chars
        print('#' +' '*21 +  "OsSitter" +' '*21+ '#')
        print('#' + ' '*50 + '#')
        print('#'*52)
        
        global lang
        # Load language (dict)
        with open("./currentlang.json", "r") as read_file:
            lang = json.load(read_file)        
        
        
        DxHelios.Say(self, "{} {}".format(lang['timeinit'],datetime.now().strftime(self.timeFormat)));
        #print("Initialisation : {}".format(datetime.now().strftime(self.timeFormat)))
   
        # Check OS
        # its win32, maybe there is win64 too?
        if sys.platform.startswith('win'):
            self.__osDetected="windows"
        elif sys.platform.startswith('linux'):
            signal.signal(signal.SIGTERM, self.term_method)
            self.__osDetected="linux"
        DxHelios.Say(self, f"OS detecté: {self.osDetected}", ind_mess= 1)

        # Load and init configuration
        self.InitConfig()

        # Register to intercept ctrl+c
        #linux < useless if decorator used
        atexit.register(self.ACiaoi)


    """ Initialize Configuration
    """
    def InitConfig(self, fileName="./config.json", reload=False):
        # Chargement de la configuration
        if not reload:
            DxHelios.Say(self, f"Chargement de la configuration", ind_mess= 1)
            self.__config= Config.Factory(os.path.join( self.__directory, fileName  ))
        else:  
            DxHelios.Say(self, f"Chargement nouvelle configuration", ind_mess= 1)
            try:
                self.__config= Config.Factory(os.path.join( self.__directory, fileName  ))
                
                # --
                os.remove("./config.json")
                os.rename("./new-config.json", "./config.json")
                #new_config= Config.Factory()
                # self.__config=new_config
                # self.__debugMode = server_params.debug
            except Exception as exc:
                print("Erreur de chargement du nouveau fichier, chargement refusé")
                print(exc)
                return False
            
        

        # Assignation
        self.__srv_params=self.config.parameters
        self.__debugMode= self.config.parameters.debug        
        self.__mail_params =  self.config.parameters.mail
        self.__alerts =  self.config.alerts
        
        # Set the next time alert
        self.__config.InitAlerts(datetime.now())
        
        if self.debugMode:            
            DxHelios.ShowParams(self, "Représentation de la configuration", self, self.config, True)
            #print("\tReprésentation de la configuration: ",self.config.__repr__()) # fonctionnel
            
            DxHelios.ShowParams(self, "Représentation des Paramètres", self, self.srv_params, True)
                        
            DxHelios.ShowParams(self, "Représentation des Alertes:", self, self.alerts, True)
           
            DxHelios.ShowParams(self, "Représentation paramètres mail:", self, self.mail_params, True)



        return True



     

    """ Mails - Part
    
    """
    def Send_Mail():

        mails=Mails()
        mails.Send(mail_params.sender,f"Etat du serveur '{server_params.server_name}'" , message, mail_params);
    
    # Send a mail "stopped service"
    def manage_stoppedservice(self, alert: Alert):
        
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

        print(f"{alert.nom} envoi de mail restarted")
        message =f"""Message de {server_params.server_name}:
                    
    Attention le service '{alert.nom}' est redémarré !
             
            
    Mail généré par OsSitter.py
                    """
        #mails.Send(f"Etat du serveur '{server_params.server_name}'" , message, mail_params.sender, mail_params.get_toList(), mail_params.get_ccList(), mail_params.get_cciList());
        mails.Send(mail_params.sender,f"Etat du serveur '{server_params.server_name}'" , message, mail_params);

    """
    Mails - End Part
    """
    
    
    # Signal when program is stopped < doesn't work for shutdown PC
    # Using register() as a decorator  
    #@atexit.register  
    def ACiaoi(self):
        self.__stopped=True
        mail_params=self.config.parameters.mail
        server_params=self.config.parameters

        mails=Mails()
        
        message =f"""Message de {server_params.server_name}:
                    
    Arrêt de OsSitter à {datetime.now()} !
             
    Le serveur n'est plus surveillé ou a été redémarré.
                    """
       
        mails.Send(mail_params.sender,f"Arrêt du serveur '{server_params.server_name}'" , message, mail_params);
     

    """ Self Test 
    """
    def test(self):
        print(">>> Tests <<<")        
        
        # Check services names
        for alert in self.config.alerts:
            if alert.typeA =="service" :
                if self.osDetected=="windows":
                    raise NotImplementedError(self.__class__.__name__ )
                elif self.osDetected == "linux":
                    alert.state=Service.lin_checkname(alert.nom)
                    
                    
        # Test mail - Si tout est ok
        subject=f"Initialisation de la surveillance de '{server_params.server_name}'"
        message =f"""Supervision activée sur {server_params.server_name}.
        """
                
        mails.Send(mail_params.sender, subject , message, mail_params);
            
            
    """ Begining
    """
    def main(self):
        print("Démarrage : {}".format(datetime.now().strftime(self.timeFormat)))

        # Initialisation
        obj=datetime.now()

        """
        import inspect
        for attr in inspect.getmembers(obj):
            # Avoiding dunder methods
            if not attr[0].startswith("__"):
                print(attr)
        """
            #result = map (lambda x:x['address'], mail_params.to)

        while(not self.__stopped):

            # Force to reload a new configuration file
            if os.path.isfile("./new-config.json"):
                InitConfig("./new-config.json",reload=True)
                #self.__config.InitAlerts(datetime.now())

                
            # Stop All
            if self.config.parameters.stop==True:
                self.__stopped=True
                break;

            
            # Alerts
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
                    #alert.next_execution == None or 
                    if  datetime.now() >= alert.next_execution :            
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

    # body of destructor
    def __del__(self):
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Destruction de l'objet OsSitter")


"""
Starting point    
"""
if __name__ == '__main__':    
    sup = OsSitter()
    sup.test()
    
    # Sys.exit to signal why
    sys.exit(sup.main())  # need to bettter use sys.exit
