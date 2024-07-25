import threading
import time
import socket
from datetime import datetime, timedelta

from typing import TypedDict
from infra.config import config

from enum import Enum

class State(Enum):
    DOWN = 1 # Quando um processo cai
    NORMAL = 2 # Quando tudo está funcionando normalmente
    ELECTION = 3 # Quando se deve iniciar uma eleição
    REORGANIZING= 4 # Quando deve avisar aos demais o resultado da eleição



class ObjNode(TypedDict):
    ipAddres: int
    connTcp:  socket.socket
    lastTime: str 




class Clock:
    
    def __init__(self, drift: float, startTime: int) -> None:
        self.drift: float = drift #
        self.time: int = startTime # Tempo inicial do relógio
        self.lock = threading.Lock() # 
        self.id: str = config['nodeId'] # O id próprio do nó
        self.clock = {}
        
    def insertOtherTime(self, nodeId, time):
        self.lock.acquire()
        self.clock[nodeId] = time
        self.lock.release()
    
    def getTime(self):
        return self.time
    

    def getDrift(self):
        self.lock.acquire()
        aux = self.drift
        self.lock.release()
        return aux
    
    def setDrift(self, newDrift):
        self.lock.acquire()
        self.drift = newDrift
        self.lock.release()

    def setTime(self, newTime):
        self.lock.acquire()
        self.time = newTime
        self.lock.release()


    def run(self):
        '''Função chamada pela thread que irá prover o ciclo de vida do relógio no nó'''
        # Enquanto estiver ligado
        while (True):
            # Durma pelo tempo do drif
            time.sleep(self.getDrift())
            # Atualize seu relógio em +1
            self.incrementClock()

    def incrementClock(self):
        ''' Método para incrementar o valor do relógio em +1 '''
        self.lock.acquire()
        self.time = self.time + 1
        self.lock.release()

