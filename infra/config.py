import os

_defaultAddres = {"1": "172.16.103",
                  "2": "",
                  "3": ""}

config = {
    "port": 7798,
    "OtherNodes" : os.getenv('ADDRESNODES', _defaultAddres),
    "drift": os.getenv('DRIFT', 1),
    "nodeId": os.getenv('NODEID', "1"),
    "timeToRequestParticipant": 2 # Indica a cada x segundos o líder vai perguntar aos seus participantes
}