# import potrzebnych modułów

# zamiast importu dwóch poniżej wykonuje import poniżej ( import numer 3 )
#from pyModbusTCP.server import ModbusServer
#from pyModbusTCP.server import DataBank
# * jest tutaj parametrem pobierającym wszystko co znajduje sie w paczce server
from pyModbusTCP.server import *

# moduł time bedzie generował opóźnienie w reagowaniu naszego servera w celu oczekiwania na wykonanie operacji
from time import sleep

# pobieramy uniform do tworzenia losowych wartości testowych
from random import uniform

# tworze instancje server modbusa
server = ModbusServer('127.0.0.1', 12345, no_block = True)

# korzystam z konstrukcji try : ... except : ... , bowiem wten sposób serwer bedzie działał
# tak długo, reagując na wszelkie operacje do póki go nie wyłącze
try:
    print("Start server...")

    # włączam serwer
    server.start()

    # informacja o obecnym statusie serwera
    print("Server is online")
    # petla bedzie sie wykonywać tak długo jak tylko jest aktywny serwer dzieki - continue

    state = [0]

    while True:
        #continue
        # tutaj zaczynamy generować liczby losowe
        DataBank.set_words(0, [int(uniform(0,100))])
        if state != DataBank.get_words(1):
            state = DataBank.get_words(1)
            print("Wartość rejestru 1 zmieniła sie na " + str(state))
            sleep(0.5)


except:
    print("Shutdown server ...")
    # zatrzymuje serwer
    server.stop()

    # informacja o obecnym statusie serwera
    print("Server is offline")














