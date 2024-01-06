#! /usr/bin/env python3
# coding: utf-8
"""
Author: Alexandre Codoul
Version: alpha 3
Required Python 3.6
"""

def get_sender(who):    
    if type(who) == str:
        return who
    else:
        return who.__class__.__name__

# Write like 'who {tab} | {tab} message'
def Say (who, message: str, ind_class=0, ind_mess=0):   
    print(f"{get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + message)


# Write like 'who {tab} | {tab} --Debug-- message'
def Debug (who, message: str, ind_class=0, ind_mess=0):   
    print(f"{get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + "--Debug-- " + message)

def Error (who, message):
    print(">"*20+ get_sender(who))
    print(message)

# write a title like #### who - bable ###
def Title(who , title):
    mult=14
    print('#'*mult+f" {get_sender(who)} - {title} " +'#'*mult)


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
    
