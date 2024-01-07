#! /usr/bin/env python3
# coding: utf-8
"""
Author: Alexandre Codoul
Version: alpha 4.1
Required Python 3.6
"""
import traceback


def get_sender(who):    
    if type(who) == str:
        return who
    else:
        return who.__class__.__name__

# Write like 'who {tab} | {tab} message'
def Say (who, message: str, ind_class=0, ind_mess=0):   
    print("{}{} | {}{}".format(get_sender(who),"\t"*ind_class,"\t"*ind_mess, message))
    #print(f"{get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + message) <-- Risque d'erreurs si None


# Write like 'who {tab} | {tab} --Debug-- message'
def Debug (who, message: str, ind_class=0, ind_mess=0):   
    print("{}{} | {}--Debug-- {}".format(get_sender(who), "\t"*ind_class, "\t"*ind_mess, message))
    #print(f"{get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + "--Debug-- " + message)


def Warning (who, message):
    mult=14
    Jump()
    print("{} {} warning !!! {} {}".format('>'*mult,get_sender(who), message, '<'*mult))
    Jump()
    
def Error (who,message,exc):
    print(">"*20+ get_sender(who))
    print(message)
    #print(f"{e} ({e.__traceback__.tb_lineno})")
    print(repr(traceback.extract_tb(exc.__traceback__)))
    print(exc)


# write a title like #### who - bable ###
def Title(who , title):
    mult=14
    print("{}{} - {}{}".format('#'*mult, get_sender(who), title,'#'*mult))
    #print('#'*mult+f" {get_sender(who)} - {title} " +'#'*mult)


# Draw a line
def DrawLine():
    print('-'*200)

    
# Write directly    
def SayRaw(message):
    print(message)


# Jump a line
def Jump():
    print('')
    
    
def ShowParams(who, title, obj, param, debug=False):
    if not debug:
        Say(obj, title)
    else :
        Debug(obj,title)
        
    DrawLine()
    SayRaw(param)
    Jump()
    
def DebugMail(who, subject, message):
    Jump()
    Debug(who, subject)
    DrawLine()
    SayRaw(message)
    DrawLine()
