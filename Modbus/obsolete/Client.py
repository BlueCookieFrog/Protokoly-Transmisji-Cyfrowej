
# skrypt pythona nie działa w środowisku PyCHARM, dlatego musze go wykonać w CMD
"""

from pyModbusTCP.client import *

client = ModbusClient(host="127.0.0.1", port=12345)

if client.open() == True:
    client.read_holding_registers(0)

"""
W CMD wpisuje :
Krok 1 : pip install pyModbusTCP
Krok 2 : from pyModbusTCP.client import *
Krok 3 : client = ModbusClient(host="127.0.0.1", port=12345)
Krok 4 : client.open()
Krko 5 : Jeżeli Krok 4 to True, wtedy przechodze do kroku 6
Krok 6 : client.read_holding_registers(0)
Krok 7 : sprawdzam odpowiedzi z servera