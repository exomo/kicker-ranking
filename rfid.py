# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# import nxppy
import time

class rfid():
    def __init__(self):
        print("init")
        # mifare = nxppy.Mifare()
        
    def TryGetToken(self):
        time.sleep(2)
        uid = "42424242424242"
        # uid = mifare.select()
        
        return uid 