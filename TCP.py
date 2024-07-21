import socket
import time
from infra.config import config

def __createConn(ip: str):
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Faço a conexão
    socket_tcp.connect((ip, config['portToTCP']))
    socket_tcp.settimeout(1)



def controlParticipantTime():
    # Manda mensagem pedindo
    time1 = time.time()
    # Aguarda a reposta
    time2 = time.time()
    latence = time2 - time1
    # o tempo final recebido é t + latence

    # Se eu caí, tento iniciar uma eleição

def responseTimeToLeader():
    ''''''

isLeadder = True
while True:
    # Se sou o líder, fico sempre solicitando a cada timeToRequestParticipant segundos
    if isLeadder == True:
        controlParticipantTime()
        # Se percebi que não consegui conversar com ninguém, é um forte indício que eu caí. Devo iniciar uma eleição e continuar tentando até conseguir falar com apenas um
        time.sleep(config['timeToRequestParticipant'])
    # Se eu não sou o líder, fico esperando receber as solicitações
    else:
        # Aqui, supostamente deve receber as solicitações do lider para que eu envie meus dados
        # Se o líder demorou para me perguntar, eu tento virar o liver
        pass