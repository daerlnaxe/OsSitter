#! /usr/bin/env python3
# coding: utf-8

"""
Author: Alexandre Codoul
Version: See above
Required Python 3.6

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
from Check_Function import Function
#from SendMail import Mails
from datetime import datetime, timedelta
# Used to detect when stopped
import atexit 
# User to intercept sigkill and ...
import signal
from MailCreator import MailCreator



class OsSitter(object):
    __version="a5.1"

    # Used to quit loop
    __stopped=False
    
    # Directory path
    __directory=None    

    # idk
    _instance = None       # Attribut statique de classe
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
    
    @property
    def mail_params(self):
        return self.__mail_params
    
    @property
    def alerts(self):
        return self.__alerts

    # A Service object, used to managed services to watch     
    @property
    def srvc(self):
        return self.__srvc

    # A fction object, used to managed functions
    @property
    def fction(self):
        return self.__fction
        
    # Object to send mails
    @property
    def mailer(self):
        return self.__mailer

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
        
        self.normal_mail("sigterm")

        print(f"------------ Envoi de mail SIGTERM")
        self.__stopped=True
     

 
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
        print('#' +' '*17 +  f"OsSitter - v{self.__version}" +' '*17+ '#')
        print('#' + ' '*50 + '#')
        print('#'*52)
        
        self.InitLanguage()
        
        
        DxHelios.Say(self, "{} {}".format(lang.get('init_time'),datetime.now().strftime(self.timeFormat)));
        #print("Initialisation : {}".format(datetime.now().strftime(self.timeFormat)))
   
        # Check OS
        # its win32, maybe there is win64 too?
        if sys.platform.startswith('win'):
            self.__osDetected="windows"
        elif sys.platform.startswith('linux'):
            signal.signal(signal.SIGTERM, self.term_method)
            self.__osDetected="linux"
            
        DxHelios.Say(self, f"{lang.get('det_os')}: {self.osDetected}", ind_mess= 1)

        # Load and init configuration
        self.InitConfig()
        if self.mail_params.mute_mode:
            DxHelios.Warning(self, lang.get('warning_mutemode'))

        
        # Initialisation des objets
        self.__srvc=Service(lang, self.osDetected)
        self.__fction=Function(lang, self.osDetected)

        

    """ Initialize Language
    """
    def InitLanguage(self, fileName="./currentlang.json", reload=False):
        global lang
        # Load language (dict)
        if not reload:
            with open(fileName, "r") as read_file:
                lang = json.load(read_file)
                
            DxHelios.Say(self, f"{lang.get('load_lang')}: {lang.get('language')} -  v{lang.get('version')}", ind_mess= 1)
        else:
            DxHelios.Say(self, f"{lang.get('load_newlang')}: {lang.get('language')} -  v{lang.get('version')}", ind_mess= 1)
            try:
                with open(fileName, "r") as read_file:
                    lang = json.load(read_file)                   
                    os.remove("./currentlang.json")
                    os.rename("./new-lang.json", "./currentlang.json")
                    
            except Exception as exc:
                DxHelios.Error(self,f"{lang.get('err_langload')}")
                print(exc)
                return False


    """ Initialize Configuration
    """
    def InitConfig(self, fileName="./config.json", reload=False):
        filePath=os.path.join( self.__directory, fileName  )
        
        # Chargement de la configuration
        if not reload:
            if not os.path.isfile(filePath):
                Config.CF_Builder(filePath)
                
            DxHelios.Say(self, f"{lang.get('load_cfg')}", ind_mess= 1)
            self.__config= Config.Factory(filePath)            
        else:  
            
            DxHelios.Say(self, f"{lang.get('load_newcfg')}", ind_mess= 1)
            try:
                self.__config= Config.Factory(filePath)
                
                # --
                if (os.path.exists("./config.json")):
                    os.remove("./config.json")
                os.rename("./new-config.json", "./config.json")
                #new_config= Config.Factory()
                # self.__config=new_config
                # self.__debugMode = server_params.debug
            except Exception as exc:
                DxHelios.Error(self,f"{lang.get('err_cfgload')}", exc)
                print(exc)
                return False
            
        

        # Assignation
        #self.__srv_params=self.config.parameters
        self.__debugMode= self.config.parameters.debug        
        self.__mail_params =  self.config.parameters.mail
        self.__alerts =  self.config.alerts
        self.__mailer=MailCreator(lang, self.config.parameters)
        self.mailer.debugMode=self.debugMode
        
        # Set the next time alert
        self.__config.InitAlerts(datetime.now())
        

        return True

   

    
    """ Signal when program is stopped
    - doesn't work for shutdown PC
    - work in case of critical error
    
    Using register() as a decorator  
    @atexit.register  <-- self problem
    """
    def ACiaoi(self):
        self.__stopped=True
        self.mailer.normal_mail("ctrlc")
     

    """ Self Test 
    """
    def test(self):
        DxHelios.Title(self, "Tests")        
        DxHelios.Say(self, lang.get('lnch_tests'))
        
        # config
        if self.debugMode:            
            DxHelios.ShowParams(self, lang.get('repr_conf'), self, self.config, True)
            #print("\tReprésentation de la configuration: ",self.config.__repr__()) # fonctionnel
            DxHelios.ShowParams(self, lang.get('repr_params'), self, self.config.parameters, True)
            DxHelios.ShowParams(self, lang.get('repr_alerts'), self, self.alerts, True)
            DxHelios.ShowParams(self, lang.get('repr_mails'), self, self.mail_params, True)

        
        # mails
        if self.debugMode:
            # Tests for mails content
            old_mute_mode= self.mail_params.mute_mode
            try:
                DxHelios.Debug(self,f"Mails: {self.mail_params}")
                
                self.mail_params.mute_mode=True

                # normal
                
                self.mailer.normal_mail("supervision_started")
                self.mailer.normal_mail("ctrlc")
                self.mailer.normal_mail("sigterm")

                # alert
                pseudoalert=Alert("pseudo", "pseudo", "pseudo", 0, 0)
                self.mailer.mail_stoppedservice(pseudoalert)
                self.mailer.mail_restartedservice(pseudoalert)

                DxHelios.Debug(self, lang.get("mail_testsok"))
            except Exception as exc:
                DxHelios.Error(self, lang.get('mail_testsfail'), exc)
                return False
            
            self.mail_params.mute_mode=old_mute_mode
        
        # Check alerts 
        for alert in self.config.alerts:
            if alert.typeA =="service" :
                # Verify if service exists
                alert.state=self.srvc.checkname(alert.nom)

                
                    
        # Test mail - if everything is ok
        self.mailer.normal_mail("just_a_test")
        
        return True
 
 
 
 
    """ Begining
    """
    def main(self):
        self.mailer.normal_mail("supervision_started")

        # Register to intercept ctrl+c
        #linux < useless if decorator used
        atexit.register(self.ACiaoi)
    
        DxHelios.Jump()
        DxHelios.Title(self, "Run")        

        DxHelios.Say(self, "{} : {}".format(lang.get('starting'),datetime.now().strftime(self.timeFormat)))

        """
        import inspect
        obj=datetime.now()
        for attr in inspect.getmembers(obj):
            # Avoiding dunder methods
            if not attr[0].startswith("__"):
                print(attr)
        """
            #result = map (lambda x:x['address'], mail_params.to)

        while(not self.__stopped):
            DxHelios.Say(self,"{} {}".format(lang.get('time'),datetime.now()))
            
            # Force to reload a new configuration file
            if os.path.isfile("./new-config.json"):
                self.InitConfig("./new-config.json",reload=True)
                self.__config.InitAlerts(datetime.now())

            # Force to reload a new language file
            if os.path.isfile("./new-lang.json"):
                self.InitLanguage("./new-lang.json",reload=True)


            

            
            # Stop All
            if self.config.parameters.stop==True:
                self.__stopped=True
                break;

            
            # Alerts
            for alert in self.config.alerts:
                # Debug Mode -> show alert informations
                if self.debugMode:                    
                    DxHelios.Debug(self,f"{lang.get('next_exec')} {alert.nom}: {alert.next_execution}")

                # Traitement de l'alerte
                ## Common / Begin

                if (alert.typeA =="service" or alert.typeA == "function"):
                    old_state=alert.state
                    print(alert.next_execution)
                    if  datetime.now() >= alert.next_execution :            
                        DxHelios.Say(self, f"{lang.get('alert_handl')} {alert.nom} {lang.get('typeof')}: {alert.typeA}",0,1)
                    # No check                    
                    else:
                        DxHelios.Say(self, f"{lang.get('service_nextchk')} {alert.nom}: {alert.next_execution}",0,1)
                
                
                
                ## Type of service
                if  alert.typeA =="service":
                    # Check alert
                    #alert.next_execution == None or 
                                    
                    alert.state=self.srvc.checkservice(alert.nom)
                        
                                      
                    
                    if old_state==None:
                        old_state=alert.state

                    # Alerting
                    ## Etat ok
                    if old_state and alert.state:
                        DxHelios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_ok')}",0,1)
                    ## Service revenu
                    elif old_state is False and alert.state:                    
                        DxHelios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_rst')}",0,1)
                        self.mailer.mail_restartedservice( alert)                
                    ## Service stoppé
                    elif alert.state is False:  
                        DxHelios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_stpd')}",0,1)
                        self.mailer.mail_stoppedservice( alert)
                    ## Autre
                    else:
                        raise ValueError(lang.get('err_value'))                


                # Type of function                                 
                elif (alert.typeA == "function" ):
                    res=self.fction.getresult(alert)
                   
                    alert.state=res[0]
                    
                    if old_state==None:
                        old_state=alert.state
            
            
                    # Alerting
                    ## Etat ok
                    if old_state and alert.state:
                        DxHelios.Say(self,f"Mémoire inférieure à {alert.trigger}: {res[1]}",0,1)
                    ## Etat de la fonction, restauré
                    elif old_state is False and alert.state:
                        msg=f"Mémoire revenue à {alert.trigger} : {res[1]}"
                        DxHelios.Say(self,msg,0,1)
                        self.mailer.mail_function( alert, msg, "mémoire ok")                
                    ## Etat de la fonction, critique
                    elif alert.state is False:  
                        msg=f"Mémoire supérieure à {alert.trigger}: {res[1]}"
                        DxHelios.Say(self, msg,0,1)
                        self.mailer.mail_function( alert, msg, "alerte mémoire")
                    ## Autre
                    else:
                        raise ValueError(lang.get('err_value'))       




                ## Common / Next Execution
                if (alert.typeA =="service" or alert.typeA == "function"):
                    self.config.set_nextexecution(alert)
                    DxHelios.Say(self, f"{lang.get('next_execset')} {alert.next_execution}",0,1)


                # Gestion du check    
                if self.debugMode:
                    DxHelios.Debug(self, f"{lang.get('states')}, check: {alert.state} | old_state: {old_state}")



                    
            # Time to Sleep (see 
            DxHelios.Say(self,f"{lang.get('sleep_param')} {self.config.parameters.sleeper * 60 }s\n\n")
            time.sleep(self.config.parameters.sleeper * 60)
            
    

    # body of destructor
    def __del__(self):
        DxHelios.Title(self, f"{lang.get('destruct')} {self.__class__.__name__}")


"""
Starting point    
"""
if __name__ == '__main__':    
    sup = OsSitter()
    if not sup.test():
        DxHelios.Say("__main__", "Tests echoués")
        sys.exit()
    
    # Sys.exit to signal why
    sys.exit(sup.main())  # need to bettter use sys.exit
