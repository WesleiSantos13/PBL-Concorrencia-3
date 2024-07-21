import threading
import time
import socket
from typing import TypedDict
from infra.config import config

from enum import Enum

class State(Enum):
    CANDIDATE = 1 # Quando ele inicia uma eleição
    LEADER = 2 # Quando ele é o líder
    INACTIVE = 3 # Quando ele percebe que está inativo
    PARTICIPANT = 4 # Quando ele está ativo, mas não é líder



class ObjNode(TypedDict):
    ipAddres: int
    connTcp:  socket.socket
    lastTime: str 




class Clock:
    '''É UMA CLASSE SINGLETON'''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Clock, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, drift: float, startTime: int) -> None:
        self.drift: float = drift #
        self.time: int = startTime # Tempo inicial do relógio
        self.lock = threading.Lock() # 
        self.power: bool = True # Indica se o relógio está ligado
        self.nodes: ObjNode = {} # Aqui vai ser um hash que possui as infos de todos os relógios
        self.id: str = config['nodeId'] # O id próprio do nó
        self.state: State = State.PARTICIPANT # 
        self.otherNodes = config['OtherNodes'] # Dados sobre os outros nós, preciso fazer isso para garantir a exclusão mútua

    def updateConn(self, nodeId, conn):
        self.lock.acquire()
        self.otherNodes[nodeId]['conn'] = conn
        self.lock.release()

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
        while (self.power == True):
            # Durma pelo tempo do drif
            time.sleep(self.getDrift())
            # Atualize seu relógio em +1
            self.incrementClock()

    def incrementClock(self):
        ''' Método para incrementar o valor do relógio em +1 '''
        self.lock.acquire()
        self.time = self.time + 1
        self.lock.release()

