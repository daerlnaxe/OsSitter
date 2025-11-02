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
    #static_output=2
    output_mode=1
    
    fileToWrite=None
    
    
    def set_outpufile(self,file):
        DxHelios.fileToWrite = open(file, "a");
        

    
    def get_sender(self, who):    
        if type(who) == str:
            return who
        else:
            return who.__class__.__name__
    
    
    """
    Define the output:
        0: Write to file
        1: Write to screen
    """
    def write_message(self, message):
        if(self.output_mode==0):
            if(type(message) != str):
                message=message. __str__()
                
            self.fileToWrite.write(f"{message}\r\n")
            self.fileToWrite.flush()
        elif(self.output_mode==1):
            print(message)

    
    
    # Write like 'who {tab} | {tab} message'
    def Say (self, who, message: str, ind_class=0, ind_mess=0):   
        #print (self.static_output)
        
        self.write_message("{}{} | {}{}".format(self.get_sender(who),"\t"*ind_class,"\t"*ind_mess, message))
        #print("{}{} | {}{}".format(self.self.get_sender(who),"\t"*ind_class,"\t"*ind_mess, message))
        #print(f"{self.get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + message) <-- Risque d'erreurs si None


    
    # Write like 'who {tab} | {tab} --Debug-- message'
    def Debug (self, who, message: str, ind_class=0, ind_mess=0):        
        #print("{}{} | {}--Debug-- {}".format(self.get_sender(who), "\t"*ind_class, "\t"*ind_mess, message))
        self.write_message("{}{} | {}--Debug-- {}".format(self.get_sender(who), "\t"*ind_class, "\t"*ind_mess, message))
        #print(f"{self.get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + "--Debug-- " + message)


    
    def Warning (self, who, message):
        mult=14
        self.Jump()
        
        
        #print("{} {} warning !!! {} {}".format('>'*mult,self.get_sender(who), message, '<'*mult))
        self.write_message("{} {} warning !!! {} {}".format('>'*mult,self.get_sender(who), message, '<'*mult))
        
        self.Jump()


    
    def Error (self, who,message,exc):
        self.write_message(">"*20+ self.get_sender(who))
       
        self.write_message(message)
        #print(f"{e} ({e.__traceback__.tb_lineno})")
        self.write_message(repr(traceback.extract_tb(exc.__traceback__)))
        self.write_message(exc)


    
    # write a title like #### who - bable ###
    def Title(self, who , title):
        mult=14
        self.write_message("{}{} - {}{}".format('#'*mult, self.get_sender(who), title,'#'*mult))
        #print('#'*mult+f" {self.get_sender(who)} - {title} " +'#'*mult)


    
    # Draw a line
    def DrawLine(self):
        self.write_message('-'*200)


    
    # Write directly    
    def SayRaw(self, message):
        self.write_message(message)


    
    # Jump a line
    def Jump(self):
        self.write_message('')

        
    
    def ShowParams(self, who, title, obj, param, debug=False):
        if not debug:
            self.Say(obj, title)
        else :
            self.Debug(obj,title)
            
        self.DrawLine()
        self.SayRaw(param)
        self.Jump()

    
    
    def DebugMail(self, who, subject, message):
        self.Jump()
        self.Debug(who, subject)
        self.DrawLine()
        self.SayRaw(message)
        self.DrawLine()


    # destructor
    def __del__(self):
        fileToWrite.close()