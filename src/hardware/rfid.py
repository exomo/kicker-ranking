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
    
    def getAdminToken():
        return getToken()

except:
    global fakeId
    global request_count
    fakeId = 42424242424242
    request_count = 0
    def getToken():
        global fakeId
        global request_count
        if request_count >= 15:
            uid = str(fakeId)
            fakeId += 1
            request_count = 0
            return uid
        else:
            request_count += 1
    
    def getAdminToken():
        return str(42424242424242)

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

    def getAdminToken(self):
        uid = getAdminToken()
        return self.Hash(uid) if uid else None
