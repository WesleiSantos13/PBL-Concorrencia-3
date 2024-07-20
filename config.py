import os

_defaultAddres = []

config = {
    "OtherNodes" : os.getenv('ADDRESNODES', _defaultAddres)
}