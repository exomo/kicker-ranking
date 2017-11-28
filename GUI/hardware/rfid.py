# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# import nxppy
import time

fakeId = 42424242424242

class rfid():
    def __init__(self):
        print("Initialize RFID-Scanner")
        # mifare = nxppy.Mifare()
        
    def TryGetToken(self):
        global fakeId
        time.sleep(2)
        uid = str(fakeId)
        fakeId += 1
        # uid = mifare.select()
        
        return uid 