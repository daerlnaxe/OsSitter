# coding: utf-8
"""
Creator: Alexandre CODOUL
Objet: Transmit mails
Version: Alpha 1.2

Notes:
    - Using a current version of the protocol
"""

import smtplib
from datetime import datetime
from typing import List



from email.message import EmailMessage


# Declare small objects first to avoid errors
class SMTP_Obj:

    @property
    def smtpstring(self):
        return self.__smtpstring
    
    
    @property
    def port(self):
        return self.__port
    
   
    @property
    def auth(self):
        return self.__auth
        
    @property
    def login(self):
        return self.__login
        
    @property
    def password(self):
        return self.__password
    
    def __init__(self,smtpstring: str, port: int, auth: bool, login: str, password: str):
        self.__smtpstring = smtpstring
        self.__port = port
        self.__auth = auth
        self.__login = login
        self.__password = password
        
    @classmethod
    def dict_toSMTPObj(self, adict:dict):

        return SMTP_Obj(adict["smtpstring"],adict["port"], adict["auth"], adict["login"], adict["app-password"])


    
    # Affichage du contenu
    def __repr__(self):
        return str(self.__dict__)
    
"""
Utile ?
"""        
class Mail_Obj:
    def get_nom(self):
        return self.__nom
    
    def get_address(self):
        return self.__address
        
    def __init__(self, nom: str, address: str):
        self.__nom=nom
        self.__address=address

            


# Object with all parameters for mails
class Mail_Block:
    @property
    def mute_mode(self):
        return self.__mutemode
        
    @property
    def sender(self):
        return self.__sender

    @property
    def smtpobj(self):
        return self.__smtpobj

    @property
    def to(self):
        return self.__to

    @property
    def cc(self):   
        return self.__cc
    
    @property
    def cci(self):
        return self.__cci
    
    def __init__(self, mutemode: bool, sender: str, smtobj: SMTP_Obj,to: List[Mail_Obj], cc: List[Mail_Obj], cci: List[Mail_Obj]):
        self.__mutemode=mutemode
        self.__sender=sender
        self.__smtpobj=SMTP_Obj.dict_toSMTPObj(smtobj)
        self.__to=to
        self.__cc=cc
        self.__cci=cci
    
    @classmethod
    def dict_toMailBlock(self, adict:dict):
        # Return an empty list if None
        return Mail_Block(adict["mutemode"],adict["sender"],adict["smtp"], adict["to"], adict["cc"], adict["cci"])


    def get_toList(self):
        if len(self.to) > 0:
            result=[]
            for mail in self.to:
                result.append(mail["address"])
            return result
        else:
            return None

    def get_ccList(self):
        if len(self.cc) > 0:
            result=[]
            for mail in self.cc:
                result.append(mail["address"])
            return result
        else:
            return None

    def get_cciList(self):
        if len(self.cci) > 0:
            result=[]
            for mail in self.cci:
                result.append(mail["address"])
            return result
        else:
            return None
            
    """
    Showing Content 
    """        
    def __repr__(self):
        return str(self.__dict__)

				
            
"""
"""
class Mails:
#    def Send(self, subject:str ,message: str, sender: str, receiver : list, receiverCC:list = None, receiverCCI:list = None):
    def Send(self, sender: str, subject:str ,message: str, mail_params:Mail_Block ):
        if mail_params.mute_mode:
            print(f"----> MuteMode: Envoi annulé pour {subject}")
            return
        
        msg = EmailMessage()

        #Il faut être du bon domaine
        
        msg['From'] = sender
        
        msg['To'] = ",".join(mail_params.get_toList())
        if mail_params.cc:
            msg['CC'] = ",".join(mail_params.get_ccList())
        
        print(mail_params.cci)
        if mail_params.cci:
            #msg['CCI']=",".join(receiverCCI)
            msg['CCI']=",".join(mail_params.get_cciList())
            

        msg['Subject'] = subject
        
        msg.set_content(message)

        # Debug
        #print("smtpobj",mail_params.smtpobj.__repr__())
        # Préparation du serveur
        mailserver = smtplib.SMTP(mail_params.smtpobj.smtpstring, mail_params.smtpobj.port)
        mailserver.ehlo()
        
        
        # Only if authentification needed
        if mail_params.smtpobj.auth:
            mailserver.starttls()
            mailserver.ehlo()
            # Penser à utiliser un  Mot de passe d'application pour outlook, etc...
            mailserver.login(mail_params.smtpobj.login, mail_params.smtpobj.password)

        #Dernières versions de Python
        mailserver.send_message(msg)
        mailserver.quit()

        print(f"----- Envoi de mail {subject}")
