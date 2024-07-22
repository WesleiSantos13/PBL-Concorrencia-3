import socket
import time
from infra.config import config
import threading




def acceptConnTCP():
    """Função do servidor que aceita conexões.
    A idéia é que sempre que alguém queira se comunicar, abra uma conexão antes de enviar a mensagem
    """
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_tcp.settimeout(2)
    
    socket_tcp.bind((config['OtherNodes'][config['nodeId']], config['port']))
    max_num_conn = len(list(config['OtherNodes'].keys()))
    socket_tcp.listen(max_num_conn)
    while True:
        try:
            conn, addr = socket_tcp.accept()
            threading.Thread(target=handle_connection, args=(conn,)).start()
        except Exception as e:
            print(f"Erro ao aceitar conexão: {e}")
            break

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