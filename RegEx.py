import re

#a = input()
#c = re.compile('[\s\t\n]{1,}')
#a = c.sub(" ",a)
#print("###########",a)
#b = re.findall(r'[\w.+%-]{1,20}@[\Da-zA-Z]{1,20}.com',a)        #\w  :  [a-zA-Z0-9_]
#pas = input()
#p = len(re.findall(r'[\w\W]{8,}',pas))
#if not p>=8:
#    print("try again")                                                              #\W   : everything except \w 
#                                                                #\d    : [0-9]
#for i in b:                                                             #\D     : everything except \w 
#    print(i)
#
#print(pas)


def spaces(check):      #function to get gid of spaces and tabs in a sentence
    a = re.compile(r'[\s\t\n]{1,}')
    check = a.sub(' ',check)    
    b = check
    return b

def emailCheck(check):
    #check if an email has spaces or tabs then get rid of it
    #a = re.compile('[\n\t]{1,}')
    #check = a.sub('',check)
    if len(re.findall(r'[\s\n\t]{1,}',check)) > 0:
        return "Sorry, wrong input! please try again."
    #now check the patrern
    b = re.findall(r'^[\w\W]{1,20}@[\Da-zA-Z]{1,15}\.com$',check)     
    
    for i in b:
        if len(b) == 0:
            return "Sorry, wrong input! please try again."
        else:
            return True

def pas(check):
    a = re.findall(r'^[\w\W]{8,}$',check)
    if len(a) > 1 or len(a) == 0 or len(a[0]) < 8:
        return "try again and make sure your password must have the length of 8 or more."
    else:
        return True


if __name__ == "__main__":
   pass

