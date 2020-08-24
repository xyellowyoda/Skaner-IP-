#!/bin/python3

import pyfiglet 
import sys
import socket
import os
from datetime import datetime

ascii_banner = pyfiglet.figlet_format('*SKANER*') 
print(ascii_banner) 


#definiowanie targetu
try:
    if len(sys.argv) == 2:
        target = socket.gethostbyname(sys.argv[1]) #Tłumaczy hostname na IPv4
    else:
        print('Syntax: python3 scaner.py <ip/hostname>')
except socket.gaierror:
    print('\n''\33[1m \33[34m''Niepoprawny adres IP lub Hostname''\n')    
    sys.exit()
except KeyboardInterrupt:
    print('\nProgram zostal zamkniety\n')
    sys.exit()  

print('-' * 50)
print('Skanowany target '+target)
print('Data skanowania: '+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
print('-' * 50)


response = os.system('ping -c 1 '+target+'> /dev/null') #sprawdzenie czy host jest aktywny

if response > 0:
   # print(target, 'is up!') #response == 0 
#else:
    print('\33[1m \33[34m''Host ''\33[31m'+target+'\33[34m'' jest nieaktywny.')
    sys.exit()  


x=[] 
for port in range(1,880): #podaj zakres skanowanych portow
        
    s = socket.socket()
    socket.setdefaulttimeout(1)
    resoult = s.connect_ex((target,port))  
    if resoult ==0:
        x.append(int(port))
        s.close()   
    

try: 
    file = open(target+'.txt', 'r').readlines() #wczytaj z pliku
except FileNotFoundError:
    print('\33[1m \33[34m''\nNie odnleziono pliku ''\33[31m'+target+'\33[34m''.txt\n')
    sys.exit()

list2 = [int(x) for x in file[0].split(', ')]
list1 = x

''' 
print('skanowane porty: '+str(list1)) #przedstawia porty skanowane
print('porty z pliku: '+str(list2)) #przedstawia porty otwarte wskazane w pliku
print("-" * 50)
'''

subset = set(list1).difference(list2)

list = list(subset)

full_str = ' '.join([str(elem) for elem in list])

if len(full_str) > 0:
    print('\33[1m \33[32m''\n''Uwaga!! Nieautoryzowane otwarte porty to: '+'\33[31m'+full_str)
    print('\n')
else:
    print('\33[32m Nie wykryto nieutoryzowanych otwartych portow')
    
