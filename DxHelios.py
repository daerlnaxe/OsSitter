#! /usr/bin/env python3
# coding: utf-8
"""
Author: Alexandre Codoul
Version: alpha 4.1
Required Python 3.6
"""
import traceback

class DxHelios:
    # fichier=0, console=1
    static_output=2
    
    fileToWrite=None
    
    @staticmethod
    def set_outpufile(file):
        DxHelios.fileToWrite = open(file, "a");
        

    @staticmethod
    def get_sender(who):    
        if type(who) == str:
            return who
        else:
            return who.__class__.__name__
    
    
    @staticmethod
    def write_message(message):
        if(DxHelios.static_output==0):
            if(type(message) != str):
                message=message. __str__()
                
            DxHelios.fileToWrite.write(f"{message}\r\n")
            DxHelios.fileToWrite.flush()
        elif(DxHelios.static_output==1):
            print(message)

    
    @staticmethod
    # Write like 'who {tab} | {tab} message'
    def Say (who, message: str, ind_class=0, ind_mess=0):   
        #print (DxHelios.static_output)
        
        DxHelios.write_message("{}{} | {}{}".format(DxHelios.get_sender(who),"\t"*ind_class,"\t"*ind_mess, message))
        #print("{}{} | {}{}".format(DxHelios.DxHelios.get_sender(who),"\t"*ind_class,"\t"*ind_mess, message))
        #print(f"{DxHelios.get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + message) <-- Risque d'erreurs si None


    @staticmethod
    # Write like 'who {tab} | {tab} --Debug-- message'
    def Debug (who, message: str, ind_class=0, ind_mess=0):        
        #print("{}{} | {}--Debug-- {}".format(DxHelios.get_sender(who), "\t"*ind_class, "\t"*ind_mess, message))
        DxHelios.write_message("{}{} | {}--Debug-- {}".format(DxHelios.get_sender(who), "\t"*ind_class, "\t"*ind_mess, message))
        #print(f"{DxHelios.get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + "--Debug-- " + message)


    @staticmethod
    def Warning (who, message):
        mult=14
        DxHelios.Jump()
        
        
        #print("{} {} warning !!! {} {}".format('>'*mult,DxHelios.get_sender(who), message, '<'*mult))
        DxHelios.write_message("{} {} warning !!! {} {}".format('>'*mult,DxHelios.get_sender(who), message, '<'*mult))
        
        DxHelios.Jump()


    @staticmethod
    def Error (who,message,exc):
        DxHelios.write_message(">"*20+ DxHelios.get_sender(who))
       
        DxHelios.write_message(message)
        #print(f"{e} ({e.__traceback__.tb_lineno})")
        DxHelios.write_message(repr(traceback.extract_tb(exc.__traceback__)))
        DxHelios.write_message(exc)


    @staticmethod
    # write a title like #### who - bable ###
    def Title(who , title):
        mult=14
        DxHelios.write_message("{}{} - {}{}".format('#'*mult, DxHelios.get_sender(who), title,'#'*mult))
        #print('#'*mult+f" {DxHelios.get_sender(who)} - {title} " +'#'*mult)


    @staticmethod
    # Draw a line
    def DrawLine():
        DxHelios.write_message('-'*200)


    @staticmethod    
    # Write directly    
    def SayRaw(message):
        DxHelios.write_message(message)


    @staticmethod
    # Jump a line
    def Jump():
        DxHelios.write_message('')

        
    @staticmethod    
    def ShowParams(who, title, obj, param, debug=False):
        if not debug:
            DxHelios.Say(obj, title)
        else :
            DxHelios.Debug(obj,title)
            
        DxHelios.DrawLine()
        DxHelios.SayRaw(param)
        DxHelios.Jump()

    
    @staticmethod    
    def DebugMail(who, subject, message):
        DxHelios.Jump()
        DxHelios.Debug(who, subject)
        DxHelios.DrawLine()
        DxHelios.SayRaw(message)
        DxHelios.DrawLine()
