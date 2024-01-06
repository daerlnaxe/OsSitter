def get_sender(who):    
    if type(who) == str:
        return who
    else:
        return who.__class__.__name__

def Say (who, message: str, ind_class=0, ind_mess=0):   
    print(f"{get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + message)

def Debug (who, message: str, ind_class=0, ind_mess=0):   
    print(f"{get_sender(who)}"+"\t"*ind_class+" | " + "\t"*ind_mess + "--Debug-- " + message)

def Title(who , title):
    mult=14
    print('#'*mult+f"{get_sender(who)}" + " - " + title +'#'*mult)

def DrawLine():
    print('-'*200)
    
def SayRaw(message):
    print(message)

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
    
