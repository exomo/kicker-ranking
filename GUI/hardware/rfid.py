"""
Read the IDs of identification tokens.
"""

import time
import hashlib

# If the nxppy library is available (on pi) getToken() returns a real token id, 
# if the nxppy library is not available, use a fake id generator
try:
    import nxppy
    mifare = nxppy.Mifare()
    def getToken():
        try:
            uid = mifare.select()
        except:
            uid = None
        return uid
except:
    global fakeId
    fakeId = 42424242424242
    def getToken():
        global fakeId
        time.sleep(2)
        uid = str(fakeId)
        fakeId += 1
        return uid

class rfid():
    """
    Class to handle reading of rfid tokens
    """
    def __init__(self):
        print("Initialize RFID-Scanner")

    def TryGetToken(self):
        uid = getToken()

        return self.Hash(uid) if uid else None

    def Hash(self, tokenId):
        encodedTokenId = tokenId.encode()
        digest = hashlib.sha256(encodedTokenId).hexdigest()
        return digest