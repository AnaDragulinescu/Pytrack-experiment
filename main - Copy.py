import machine
import pycom
import math
import network
import os
import utime
import gc
from network import LoRa
from machine import SD
import socket
import time
import ubinascii
import struct
from machine import RTC
from L76GNSV5 import L76GNSS
from pytrack import Pytrack
from network import LoRa
from scriere import Scriere_param
from scriere import Scriere_param2
from scriere import init_scriere


#Garbage collector


# rtc.ntp_sync("pool.ntp.org")
# utime.sleep_ms(750)
# print('\nRTC Set from NTP to UTC:', rtc.now())
# utime.timezone(7200)
# print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

#Pytrack GPS si RTC
print('#######Start########')
py = Pytrack()
l76 = L76GNSS(py, timeout=30)
# setup rtc
rtc = machine.RTC()
l76.setRTCClock()

#card SD

#LoRa
# APPKEY="" 
APPKEY="" 


# DEVICE_ID = 0x03
# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
# lora.init(mode=LoRa.LORA,region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=12,\
# coding_rate=LoRa.CODING_4_5)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('')
app_key = ubinascii.unhexlify(APPKEY) #1
#uncomment to use LoRaWAN application provided dev_eui


# Uncomment for US915 / AU915 & Pygate
# for i in range(0,8):
#     lora.remove_channel(i)
# for i in range(16,65):
#     lora.remove_channel(i)
# for i in range(66,72):
#     lora.remove_channel(i)

# join a network using OTAA (Over the Air Activation)
#uncomment below to use LoRaWAN application provided dev_eui
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
pycom.heartbeat(0)
pycom.rgbled(0xFF0000)
time.sleep(1)
pycom.heartbeat(1)

# sd = SD()
# os.mount(sd, '/sd')
# writepath = '/sd/ExperimentePytrackCTA.txt'
# f = open(writepath, 'a+')
# init_scriere(writepath)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)
ID=0
while (True):
    print("Work")
    print(l76.coordinates())
    coordonate=l76.coordinates()
    latitudine=coordonate['latitude']
    longitudine=coordonate['longitude']
    if latitudine is None:
        latitudine=11
        longitudine=22
    date=struct.pack('!ffH', latitudine, longitudine, ID)
    print(ID)
    ID+=1
    # Scriere_param(writepath,rtc,l76,lora,ID)
    s.send(date)
    print("Pachet trimis")
    print(date)
    pycom.heartbeat(0)
    pycom.rgbled(0x00FF00)
    time.sleep(2)
    pycom.heartbeat(1)
    time.sleep(2)
