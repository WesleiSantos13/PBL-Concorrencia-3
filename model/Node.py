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
    '''É UMA CLASSE SINGLETON'''
    _instance = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Clock, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, drift: float, startTime: int) -> None:
        if not hasattr(self, 'initialized'):  # Verifica se já foi inicializado
            print("entrei")
            self.drift: float = drift #
            self.time: int = startTime # Tempo inicial do relógio
            self.lock = threading.Lock() # 
            self.power: bool = True # Indica se o relógio está ligado
            self.id: str = config['nodeId'] # O id próprio do nó
            self.state: State = State.PARTICIPANT # 
            self.leader:str = None # Aqui será o id do líder
            self.leaderLastContact: datetime = None

    def imLeader(self) -> bool:
        return self.leader == self.id
    
    def getLeader(self):
        return self.leader
    
    def setLeader(self, new_node_id_leader):
        self.lock.acquire()
        self.leader = new_node_id_leader
        self.lock.release()

    def leaderIsDead(self, now: datetime):
        '''Após 2 segundos do último contato do líder, irá retornar True'''
        # Se for None (acabei de inicializar), devo informar que devo iniciar uma eleição
        if self.leaderLastContact is None:
            return True
        # Caso contrário, faço a verificação de tempo
        self.lock.acquire()
        difference = abs(self.leaderLastContact - now)
        self.lock.release()

        return difference > timedelta(seconds=2)


    def setLeaderLastContact(self, leaderLastContact):
        self.lock.acquire()
        self.leaderLastContact = leaderLastContact
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

