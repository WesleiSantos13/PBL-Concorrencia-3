from flask import Flask, request, jsonify
import requests
import threading
import logging
import os
import time

from infra.config import config
from model.Node import Clock

## ======= Bloco para instânciação de objetos necessários ======= ##
app = Flask(__name__)

clock = Clock(config['drift'], 0)
app.logger.disabled = True
logging.getLogger('werkzeug').disabled = True

### ================================================ BLOCO PARA ROTAS ==================================================== ###
@app.route('/', methods=['POST'])
def currentTime():
    '''Fornece o valor de clock atual.'''
    content = request.json
    clock.insertOtherTime(content['nodeId'], content['time'])
    return jsonify({"mensagem": "ok"}), 200

### ================================================ BLOCO PARA FUNÇÕES DE THREADS ==================================================== ###
def menu(clock: Clock):
    """Função para o menu de alteração do incremento.
    Será executado como uma thread"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Drift={clock.getDrift()}  Time={clock.getTime()}")
        print("=======Menu=======")
        print("[1] Alterar valor do drift")
        print("[2] Alterar valor do relógio")
        print("[3] Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == "1":
            try:
                new_increment = float(input("Digite o novo valor do drift: "))
                clock.setDrift(new_increment)
            except ValueError:
                print("Por favor, insira um valor numérico válido.")
        elif choice == "2":
            try:
                new_time = float(input("Digite o novo valor do relógio: "))
                clock.setTime(new_time)
            except ValueError:
                print("Por favor, insira um valor numérico válido.")
        elif choice == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def send_clock_update(clock: Clock):######################################################################################ERRADO
    '''Envia o estado atual do relógio para os outros nós.'''
    msg = {
        "nodeId": clock.id,
        "time": clock.getTime()
    }
    # print(f"Os endereços {config['OtherNodes'].items()}")
    if len(config['OtherNodes'].items()) > 0:
        for node, address in config['OtherNodes'].items():
            # Se não for para o próprio nó
            if node != clock.id:
                url = f"http://{address}:{config['port']}/"
                try:
                    response = requests.post(url, json=msg)
                    if response.status_code == 200:
                        # print(f"Enviado para o nó {node}.")
                        pass
                    else:
                        pass
                        # print(f"Falha ao enviar para o nó {node}. Status Code: {response.status_code}")
                except requests.RequestException as e:
                    pass
                    # print(f"Erro ao enviar tempo para o nó {node}: {e}")




def send_periodically(clock, interval):
    '''Envia o estado atual do relógio para os outros nós periodicamente.'''
    while True:
        send_clock_update(clock)
        time.sleep(interval)  # Aguarda pelo intervalo especificado antes de enviar novamente


def changeTime(clock: Clock):
    while True:
        try:
            if len(clock.clock.values()) > 0:
                max_time = max(clock.clock.values())
                myTime = clock.getTime()
                # print(f"O maior, dentre os outros, é {max_time}; O meu é {myTime}")
                if max_time > myTime:
                    newTime = max_time
                    if max_time - myTime > config['DIFFER_LIMIT']:
                        newTime = myTime + (max_time - myTime)/4
                    clock.setTime(newTime)
                time.sleep(2)
        except Exception as e:
            # print(f"deu erro em mudar tempo:\n{e}")
            pass


# Colocar a thread da rotina eterna
if __name__ == '__main__':
    # Tem uma thread para o menu
    thread_interface_manual = threading.Thread(target=menu, args=[clock])
    thread_interface_manual.daemon = True
    
    thread_clock_run = threading.Thread(target=clock.run)
    thread_clock_run.daemon = True

    # Inicia a thread para enviar atualizações periodicamente
    thread_send_updates = threading.Thread(target=send_periodically, args=[clock, config['timeToRequestParticipant']])
    thread_send_updates.daemon = True

    # Thread que atualiza o relógio interno
    thread_changeTime = threading.Thread(target=changeTime, args=[clock])
    thread_changeTime.daemon = True
    # Iniciando as threads
    thread_interface_manual.start()
    thread_clock_run.start()
    thread_send_updates.start()
    thread_changeTime.start()

    # Levantando a API
    app.run(port=config['port'], host='0.0.0.0')

    # Caso as threads sejam interrompidas
    thread_interface_manual.join()
    thread_clock_run.join()
    thread_send_updates.join()
    thread_changeTime.join()
