#! /usr/bin/env python3
# coding: utf-8

"""
Author: Alexandre Codoul
Version: 1.1
Required Python 3.6

Linux :


"""
from MailSender import Mails
from AlertClass import Alert
from datetime import datetime, timedelta

#import DxHelios
from DxHelios import DxHelios


class MailCreator(object):

    @property
    def debugMode(self):
        return self.__debugMode
    
    @debugMode.setter
    def debugMode(self, value):
        self.__debugMode=value
    
    @property
    def lang(self):
        return self.__lang__

    @property
    def srv_params(self):
        return self.__srv_params
        
    @property
    def mail_params(self):
        return self.__mail_params
        
    # Builder    
    def __init__(self, lang, srv_params):
        self.__lang__=lang
        self.__srv_params=srv_params
        self.__mail_params =  srv_params.mail

        
        
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
            subject+=self.lang.get('mail_supactivated')
        elif mailtype=="ctrlc":
            subject+=self.lang.get('alert_stopped')
        elif mailtype=="sigterm":
            subject+=f"SIGTERM"
        elif mailtype=="reloadconf":
            subject+=f"changement de la configuration"
        elif mailtype=="reloadconffailed":
            subject+=f"echec de changement de la configuration"
            
        
        # message
        if mailtype == "just_a_test":    
            message+="It's just a test"    
        elif mailtype == "supervision_started":
            message+=f"\t{self.lang.get('mail_supactivated')}."
        elif mailtype=="ctrlc":
            message +=f"""        
    {self.lang.get('alert_stopped')} ({datetime.now()}) !
             
    {self.lang.get('alert_ctrlc')}
    """
        elif mailtype=="sigterm":
            message+=f"""
    {self.lang.get('mail_rsignal')} SIGTERM ({datetime.now()}) !
            
    {self.lang.get('warning_nowtch')}
    """
        elif mailtype=="reloadconf":
            message+=f"configuration modified"
        elif mailtype=="reloadconffailed":
            subject+=f"failed to modify configuration"
            
        message+=f"\r\n\r\n{self.lang.get('mail_sign')} OsSitter, {datetime.now()}." # {self.__class__.__name__}."
        
        if self.debugMode:
            DxHelios.DebugMail(self,subject, message)
            #DxHelios.DebugMail(self, self.mail_params)
        
        print("*******************************************test")
        print(message)
        mails.Send(self.mail_params.sender, subject , message, self.mail_params);

#---

    # Alerte générique utilisée par les autres fonctions
    def alert_mail(self, subject, ori_message):    
        # Creation of the object to send mails
        mails=Mails()
        subject=f"{self.srv_params.server_name} - {subject}"
        message=f"{self.srv_params.server_name}:\r\n\t{ori_message}"
        
        message+=f"\r\n\r\n{self.lang.get('mail_sign')}, {datetime.now()}." # {self.__class__.__name__}."
        
        if self.debugMode:
            DxHelios.DebugMail(self,subject, message)
        
        mails.Send(self.mail_params.sender, subject , message, self.mail_params);

## ---------------------
    
    """
    Functions       ----------------------------
    """
    # Function
    def mail_function(self, alert: Alert, message, title):
        print (alert)
        print (type(alert))
        
        # Keep a respectuous mail flow
        if alert.next_alarm == None or datetime.now() > alert.next_alarm:
            subject=f"{self.lang.get('function')} '{alert.nom}' - {title} "
            message=f"Function '{alert.nom}': {message}"
            self.alert_mail( subject, message)

            # Assign time for the next alert
            alert.next_alarm = datetime.now() + timedelta(minutes=alert.delay_alarm)
            DxHelios.Say(self, f"Prochaine alarme programmée: {alert.next_alarm}",0,1)
        else:
            DxHelios.Say(self, f"{alert.nom}: pas d'envoi de mail avant: {alert.next_alarm}",0,1)


            
            
    ## Send a mail "restarted service"
    def mail_functionrestaured(self, alert: Alert, message, title):
        subject=f"{self.lang.get('function')} '{alert.nom}' - {title} "
        
        message=f"Function '{alert.nom}': {message}"            
        
        self.alert_mail( subject, message)
        
        


        
    """
    Services        ----------------------------
    """
    # Service-
    ## Send a mail "stopped service"
    def mail_stoppedservice(self, alert: Alert):
        # Keep a respectuous mail flow
        if alert.next_alarm == None or datetime.now() > alert.next_alarm:
            subject=f"{self.lang.get('service')} '{alert.nom}' {self.lang.get('mail_isstopped')} "
            message=f"{self.lang.get('mail_wservice')} '{alert.nom}' {self.lang.get('mail_isstopped')} !"
            self.alert_mail( subject, message)

            # Assign time for the next alert
            alert.next_alarm = datetime.now() + timedelta(minutes=alert.delay_alarm)
            DxHelios.Say(self, f"Prochaine alarme programmée: {alert.next_alarm}",0,1)
        else:
            DxHelios.Say(self, f"{alert.nom}: pas d'envoi de mail avant: {alert.next_alarm}",0,1)



    ## Send a mail "restarted service"
    def mail_restartedservice(self, alert: Alert):
        subject=f"{self.lang.get('service')} '{alert.nom}' {self.lang.get('mail_isrestarted')} "
        
        message =f"{self.lang.get('mail_wservice')} '{alert.nom}' {self.lang.get('mail_isrestarted')} !"
        
        self.alert_mail( subject, message)


    """
    Mails - End Part
    """