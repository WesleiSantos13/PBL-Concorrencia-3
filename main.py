from model.Node import Clock
from model.Election import Election
from infra.config import config

from datetime import datetime
import threading
import time
import os








            


# ======================================= BLOCO PARA INICIAR O PROCESSO PRINCIPAL ========================================= #
if __name__ == "__main__":
    clock = Clock(config['drift'], 0)
    election = Election(clock)

    # ======================================= BLOCO DE DEFINIÇÃO DE THREADS ========================================= #
    # Tem uma thread para o menu
    thread_interface_manual = threading.Thread(target=menu, args=[clock])
    thread_interface_manual.daemon = True
    # # Tem uma thread para verificar se o líder caiu
    # thread_watch_leader = threading.Thread(target=verifyContactLeader, args=[clock, election])
    # thread_watch_leader.daemon = True
    
    # # Tem um pool de threads que servem para processar algo e responder


    # ###### Dá start nas threads ######
    thread_interface_manual.start()
    # thread_watch_leader.start()
    # # thread_udp.start()
    # # thread_tcp.start()

    # ###### Pro caso de dar erro ######
    thread_interface_manual.join()
    # thread_watch_leader.join()
    # # thread_udp.join()
    # # thread_tcp.join()

## PRECISO DE UMA THREAD QUE FIQUE VERIFICANDO O ÚLTIMO CONTATO DO LIDER


# A cada x segundos eu faço uma rodada pedindo todos os relógios
# Eu escolho o relógio mais adiantado para ser minha referência
# Se eu sou o mais adiantado