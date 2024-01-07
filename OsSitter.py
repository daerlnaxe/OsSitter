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
from SendMail import Mails
from datetime import datetime, timedelta
# Used to detect when stopped
import atexit 
# User to intercept sigkill and ...
import signal




class OsSitter(object):
    __version="a4.1"

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
        
    @property
    def srvc(self):
        return self.__srvc
        
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

        
        # 
        self.__srvc=Service(lang, self.osDetected)

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
                os.remove("./config.json")
                os.rename("./new-config.json", "./config.json")
                #new_config= Config.Factory()
                # self.__config=new_config
                # self.__debugMode = server_params.debug
            except Exception as exc:
                DxHelios.Error(self,f"{lang.get('err_cfgload')}")
                print(exc)
                return False
            
        

        # Assignation
        self.__srv_params=self.config.parameters
        self.__debugMode= self.config.parameters.debug        
        self.__mail_params =  self.config.parameters.mail
        self.__alerts =  self.config.alerts
        
        # Set the next time alert
        self.__config.InitAlerts(datetime.now())
        

        return True

   

    """ Mails - Part        
    """
    #
    def normal_mail(self, mailtype):
        # Creation of the object to send mails
        mails=Mails()
        subject=f"{self.srv_params.server_name} - "
        message=f"{self.srv_params.server_name}:\r\n"
        
        # subject
        if mailtype == "just_a_test":
            subject+=f"Just a test..."
        elif mailtype == "supervision_started":
            subject+=lang.get('mail_supactivated')
        elif mailtype=="ctrlc":
            subject+=lang.get('alert_stopped')
        elif mailtype=="sigterm":
            subject+=f"SIGTERM"
        
        # message
        if mailtype == "just_a_test":    
            message+="It's just a test"    
        elif mailtype == "supervision_started":
            message+=f"\t{lang.get('mail_supactivated')}."
        elif mailtype=="ctrlc":
            message +=f"""        
    {lang.get('alert_stopped')} ({datetime.now()}) !
             
    {lang.get('alert_ctrlc')}
    """
        elif mailtype=="sigterm":
            message+=f"""
    {lang.get('mail_rsignal')} SIGTERM ({datetime.now()}) !
            
    {lang.get('warning_nowtch')}
    """
           
            
        message+=f"\r\n\r\n{lang.get('mail_sign')} {self.__class__.__name__}."
        
        if self.debugMode:
            DxHelios.DebugMail(self,subject, message)
        
        mails.Send(self.mail_params.sender, subject , message, self.mail_params);

    #
    def alert_mail(self, subject, ori_message):    
        # Creation of the object to send mails
        mails=Mails()
        subject=f"{self.srv_params.server_name} - {subject}"
        message=f"{self.srv_params.server_name}:\r\n\t{ori_message}"
        
        message+=f"\r\n\r\n{lang.get('mail_sign')} {self.__class__.__name__}."
        
        if self.debugMode:
            DxHelios.DebugMail(self,subject, message)
        
        mails.Send(self.mail_params.sender, subject , message, self.mail_params);
    
    
    # Send a mail "stopped service"
    def manage_stoppedservice(self, alert: Alert):
        # Keep a respectuous mail flow
        if alert.next_alarm == None or datetime.now() > alert.next_alarm:
            subject=f"{lang.get('service')} '{alert.nom}' {lang.get('mail_isstopped')} "
            message=f"{lang.get('mail_wservice')} '{alert.nom}' {lang.get('mail_isstopped')} !"
            self.alert_mail( subject, message)

            # Assign time for the next alert
            alert.next_alarm = datetime.now() + timedelta(minutes=alert.delay_alarm)
            DxHelios.Say(self, f"Prochaine alarme programmée: {alert.next_alarm}",0,1)
        else:
            DxHelios.Say(self, f"{alert.nom}: pas d'envoi de mail avant: {alert.next_alarm}",0,1)


    # Send a mail "restarted service"
    def manage_restartedservice(self, alert: Alert):
        subject=f"{lang.get('service')} '{alert.nom}' {lang.get('mail_isrestarted')} "
        
        message =f"{lang.get('mail_wservice')} '{alert.nom}' {lang.get('mail_isrestarted')} !"
        
        self.alert_mail( subject, message)


    """
    Mails - End Part
    """

    
    """ Signal when program is stopped
    - doesn't work for shutdown PC
    - work in case of critical error
    
    Using register() as a decorator  
    @atexit.register  <-- self problem
    """
    def ACiaoi(self):
        self.__stopped=True
        self.normal_mail("ctrlc")
     

    """ Self Test 
    """
    def test(self):
        DxHelios.Title(self, "Tests")        
        DxHelios.Say(self, lang.get('lnch_tests'))
        
        # config
        if self.debugMode:            
            DxHelios.ShowParams(self, lang.get('repr_conf'), self, self.config, True)
            #print("\tReprésentation de la configuration: ",self.config.__repr__()) # fonctionnel
            DxHelios.ShowParams(self, lang.get('repr_params'), self, self.srv_params, True)
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
                self.normal_mail("supervision_started")
                self.normal_mail("ctrlc")
                self.normal_mail("sigterm")

                # alert
                pseudoalert=Alert("pseudo", "pseudo",0,0)
                self.manage_stoppedservice(pseudoalert)
                self.manage_restartedservice(pseudoalert)

                DxHelios.Debug(self, lang.get("mail_testsok"))
            except Exception as exc:
                DxHelios.Error(self, lang.get('mail_testsfail'), exc)
                return False
            
            self.mail_params.mute_mode=old_mute_mode
        
        # Check services names
        for alert in self.config.alerts:
            if alert.typeA =="service" :
                alert.state=self.srvc.checkname(alert.nom)
                    
        # Test mail - if everything is ok
        self.normal_mail("just_a_test")
        
        return True
 
 
    """ Begining
    """
    def main(self):
        self.normal_mail("supervision_started")

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
                #self.__config.InitAlerts(datetime.now())

            # Force to reload a new language file
            if os.path.isfile("./new-lang.json"):
                self.InitLanguage("./new-lang.json",reload=True)
                #self.__config.InitAlerts(datetime.now())
            

            
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
                if alert.typeA =="service" :
                    old_state=alert.state
                    # Check alert
                    #alert.next_execution == None or 
                    if  datetime.now() >= alert.next_execution :            
                        DxHelios.Say(self, f"{lang.get('alert_handl')} {alert.nom} {lang.get('typeof')}: {alert.typeA}",0,1)
                   
                                    
                        alert.state=self.srvc.checkservice(alert.nom)
                        
                        self.config.set_nextexecution(alert)
                        DxHelios.Say(self, f"{lang.get('next_execset')} {alert.next_execution}",0,1)

                        # Gestion du check    
                        if self.debugMode:
                            DxHelios.Debug(self, f"{lang.get('states')}, check: {alert.state} | old_state: {old_state}")
                           

                    # No check                    
                    else:
                        DxHelios.Say(self, f"{lang.get('service_nextchk')} {alert.nom}: {alert.next_execution}",0,1)

                                       
                    
                    if old_state==None:
                        old_state=alert.state

                    # Alerting
                    if old_state and alert.state:
                        DxHelios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_ok')}",0,1)
                    elif old_state is False and alert.state:                    
                        DxHelios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_rst')}",0,1)
                        self.manage_restartedservice( alert)                
                    elif alert.state is False:  
                        DxHelios.Say(self,f"{lang.get('service')} {alert.nom}: {lang.get('state_stpd')}",0,1)
                        self.manage_stoppedservice( alert)
                    else:
                        raise ValueError(lang.get('err_value'))                
                                    
                        
                    
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
        sys.exit()
    
    # Sys.exit to signal why
    sys.exit(sup.main())  # need to bettter use sys.exit
