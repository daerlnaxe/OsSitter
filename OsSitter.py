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
from DxHelios import DxHelios
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
    __version="a5.5"

    # Used to quit loop
    __stopped=False
    
    # Directory path
    __directory=None    

    # idk
    _instance = None       # Attribut statique de classe
    
    Helios=None
        #return self.__helios
        
    #@Helios.setter
    #def Helios(self, value):
    #    self.__helios = value

        
    
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
    
    #@property
    #def mail_params(self):
    #    return self.__mail_params
    
    # Object to send mails
    @property
    def mailer(self):
        return self.__mailer
    
    
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
        


    #debugMode=None
    
    @staticmethod
    def myself():
        return self._instance
        
    def term_func(self, signum, frame):
        #global is_shutdown
        
        #-print(frame)
        self.Helios.Say(self, frame)
        #-print(signum)
        self.Helios.Say(self, signum)
        
        #is_shutdown = True
        #-print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SIGTERM: term_func')
        self.Helios.Say(self, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SIGTERM: term_func')
    

    def term_method(self, signum, frame):
        #-print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SIGTERM: term_method')
        self.Helios.Say(self, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SIGTERM: term_method')
        
        self.mailer.normal_mail("sigterm")

        #-print(f"------------ Envoi de mail SIGTERM")
        self.Helios.Say(self, f"------------ Envoi de mail SIGTERM")
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
        self.Helios.Say(self, '#'*52)
        self.Helios.Say(self, '#' + ' '*50 + '#')
        
        #OsSitter: 8 chars
        self.Helios.Say(self, '#' +' '*17 +  f"OsSitter - v{self.__version}" +' '*17+ '#')
        self.Helios.Say(self, '#' + ' '*50 + '#')
        self.Helios.Say(self, '#'*52)
        
        self.InitLanguage()
        
        
        self.Helios.Say(self, "{} {}".format(lang.get('init_time'),datetime.now().strftime(self.timeFormat)));
        #print("Initialisation : {}".format(datetime.now().strftime(self.timeFormat)))
   
        # Check OS
        # its win32, maybe there is win64 too?
        if sys.platform.startswith('win'):
            self.__osDetected="windows"
        elif sys.platform.startswith('linux'):
            signal.signal(signal.SIGTERM, self.term_method)
            self.__osDetected="linux"
            
        self.Helios.Say(self, f"{lang.get('det_os')}: {self.osDetected}", ind_mess= 1)

        # Load and init configuration
        self.InitConfig()
        
        # Warning if mute mode activated
        #if self.mail_params.mute_mode:
        if self.config.parameters.mail.mute_mode:
            self.Helios.Warning(self, lang.get('warning_mutemode'))

        
        # Initialisation des objets
        self.__srvc=Service(lang, self.osDetected)
        self.srvc.Helios=self.Helios
        
        self.__fction=Function(lang, self.osDetected)
        self.fction.Helios=self.Helios
        

    """ Initialize Language
    """
    def InitLanguage(self, fileName="./currentlang.json", reload=False):
        global lang
        # Load language (dict)
        if not reload:
            with open(fileName, "r") as read_file:
                lang = json.load(read_file)
                
            self.Helios.Say(self, f"{lang.get('load_lang')}: {lang.get('language')} -  v{lang.get('version')}", ind_mess= 1)
        else:
            self.Helios.Say(self, f"{lang.get('load_newlang')}: {lang.get('language')} -  v{lang.get('version')}", ind_mess= 1)
            try:
                with open(fileName, "r") as read_file:
                    lang = json.load(read_file)                   
                    os.remove("./currentlang.json")
                    os.rename("./new-lang.json", "./currentlang.json")
                    
            except Exception as exc:
                self.Helios.Error(self,f"{lang.get('err_langload')}")
                print(exc)
                return False


    """ Initialize Configuration
    """
    def InitConfig(self, fileName="./config.json", reload=False):

    
        filePath=os.path.join( self.__directory, fileName  )
        
        # Chargement de la configuration
        if not reload:
            if not os.path.isfile(filePath):
                self.Helios.Say("Config", f"Création du fichier de configuration: {filePath}",1,1)
                Config.CF_Builder(filePath)
                
            self.Helios.Say(self, f"{lang.get('load_cfg')}", ind_mess= 1)
            
            self.Helios.Say("Config", f"Chargement du fichier de configuration: {filePath}",1,1)
            self.__config= Config.Factory(filePath)
        # Load a new config file
        else:  
            self.Helios.Say(self, f"{lang.get('load_newcfg')}", ind_mess= 1)
            try:
                self.__config= Config.Factory(filePath)
                
                # --
                if (os.path.exists("./config.json")):
                    os.remove("./config.json")
                os.rename("./new-config.json", "./config.json")
                #new_config= Config.Factory()
                # self.__config=new_config
                # self.__debugMode = server_params.debug
                self.mailer.normal_mail("reloadconf")

            except Exception as exc:
                self.Helios.Error(self,f"{lang.get('err_cfgload')}", exc)
                print(exc)
                self.mailer.normal_mail("reloadconffailed")
                return False
            
        

        # Assignation
        #self.__srv_params=self.config.parameters
        self.__debugMode= self.config.parameters.debug        
        #self.__mail_params =  self.config.parameters.mail
        self.__alerts =  self.config.alerts
        
        # mailer
        self.__mailer=MailCreator(lang, self.config.parameters)
        self.mailer.Helios=self.Helios        
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
        self.Helios.Title(self, "Tests")        
        self.Helios.Say(self, lang.get('lnch_tests'))
        mail_params = self.config.parameters.mail
        
       
        # config
        if self.debugMode:            
            self.Helios.ShowParams(self, lang.get('repr_conf'), self, self.config, True)
            #print("\tReprésentation de la configuration: ",self.config.__repr__()) # fonctionnel
            self.Helios.ShowParams(self, lang.get('repr_params'), self, self.config.parameters, True)
            self.Helios.ShowParams(self, lang.get('repr_mails'), self, self.config.parameters.mail, True)
            self.Helios.ShowParams(self, lang.get('repr_alerts'), self, self.alerts, True)

        
        # mails
        if self.debugMode:
            # Tests for mails content
            old_mute_mode= mail_params.mute_mode
            
            try:
                self.Helios.Debug(self,f"Mails: {mail_params}")
                
                mail_params.mute_mode=True

                # normal
                
                self.mailer.normal_mail("supervision_started")
                self.mailer.normal_mail("ctrlc")
                self.mailer.normal_mail("sigterm")

                # alert
                pseudoalert=Alert("pseudo", "pseudo", "pseudo", "pseudo", 0, 0)
                self.mailer.mail_stoppedservice(pseudoalert)
                self.mailer.mail_restartedservice(pseudoalert)

                self.Helios.Debug(self, lang.get("mail_testsok"))
            except Exception as exc:
                self.Helios.Error(self, lang.get('mail_testsfail'), exc)
                return False
            
            mail_params.mute_mode=old_mute_mode
            
           
        
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
        mail_params = self.config.parameters.mail

        self.mailer.normal_mail("supervision_started")

        # Register to intercept ctrl+c
        #linux < useless if decorator used
        atexit.register(self.ACiaoi)
    
        self.Helios.Jump()
        self.Helios.Title(self, "Run")        

        self.Helios.Say(self, "{} : {}".format(lang.get('starting'),datetime.now().strftime(self.timeFormat)))

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
            self.Helios.Say(self,"{} {}".format(lang.get('time'),datetime.now()))
            
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
                    self.Helios.Debug(self,f"{lang.get('next_exec')} {alert.nom}: {alert.next_execution}")

                # Traitement de l'alerte
                ## Common / Begin

                if (alert.typeA =="service" or alert.typeA == "function"):
                    old_state=alert.state
                    print(alert.next_execution)
                    if  datetime.now() >= alert.next_execution :            
                        self.Helios.Say(self, f"{lang.get('alert_handl')} {alert.nom} {lang.get('typeof')}: {alert.typeA}",0,1)
                    # No check                    
                    else:
                        self.Helios.Say(self, f"{lang.get('service_nextchk')} {alert.nom}: {alert.next_execution}",0,1)
                
                
                
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
                        self.Helios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_ok')}",0,1)
                    ## Service revenu
                    elif old_state is False and alert.state:                    
                        self.Helios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_rst')}",0,1)
                        self.mailer.mail_restartedservice( alert)       

                        alert.next_alarm=None
                        
                    ## Service stoppé
                    elif alert.state is False:  
                        self.Helios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_stpd')}",0,1)
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
                        self.Helios.Say(self,f"{alert.nom}, stat supérieure à {alert.trigger}: {res[1]}",0,1)
                    ## Etat de la fonction, restauré
                    elif old_state is False and alert.state:
                        msg=f"stat revenue sous {alert.trigger} : {res[1]}"
                        self.Helios.Say(self, f"{alert.nom} - {msg}",0,1)
                        self.mailer.mail_functionrestaured( alert, msg, "Restauration")  

                        alert.next_alarm=None
                    ## Etat de la fonction, critique
                    elif alert.state is False:  
                        msg=f"alarme --> stat inférieure à {alert.trigger}: {res[1]}"
                        self.Helios.Say(self, f"{alert.nom} - {msg}",0,1)
                        self.mailer.mail_function( alert, msg, "Alerte")
                    ## Autre
                    else:
                        raise ValueError(lang.get('err_value'))       




                ## Common / Next Execution
                if (alert.typeA =="service" or alert.typeA == "function"):
                    self.config.set_nextexecution(alert)
                    self.Helios.Say(self, f"{lang.get('next_execset')}  {alert.next_execution} ({alert.timer})",0,1 )


                # Gestion du check    
                if self.debugMode:
                    self.Helios.Debug(self, f"{lang.get('states')}, check: {alert.state} | old_state: {old_state}")



                    
            # Time to Sleep (see 
            self.Helios.Say(self,f"{lang.get('sleep_param')} {self.config.parameters.sleeper * 60 }s\n\n")
            time.sleep(self.config.parameters.sleeper * 60)
            
    

    # body of destructor
    def __del__(self):
        OsSitter.Helios.Title(self, f"{lang.get('destruct')} {self.__class__.__name__}")
        print("OsSitter Stopped")


"""
Starting point    
"""
if __name__ == '__main__':    
    ############ temporaire #############
    OsSitter.Helios=DxHelios()
    OsSitter.Helios.output_mode=0
    OsSitter.Helios.set_outpufile("./ossitter.log")
    
    
    sup = OsSitter()
    
    if not sup.test():
        sup.Helios.Say("__main__", "Tests echoués")
        print("__main__", "Tests echoués")
        sys.exit()
    
    # Sys.exit to signal why
    sys.exit(sup.main())  # need to bettter use sys.exit
