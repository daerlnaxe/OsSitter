
def Say (who, message, ind_class=0, ind_mess=0):
    print(f"{who.__class__.__name__}"+"\t"*ind_class+" | " + "\t"*ind_mess + message)
    
def DrawLine():
    print('-'*200)
    
def SayRaw(message):
    print(message)

def Jump():
    print('')
    
    
def ShowParams(who, title, obj, param):
    Say(obj, title)
    DrawLine()
    SayRaw(param)
    Jump()