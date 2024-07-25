from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import threading
import logging
import os
import time
from infra.config import config
from model.Node import Clock
from model.Election import Election

## ======= Bloco para instânciação de objetos necessários ======= ##
app = Flask(__name__)

clock = Clock(config['drift'], 0)

### ================================================ BLOCO PARA ROTAS ==================================================== ###
@app.route('/', methods=['PATCH'])
def currentTime():
    '''Fornece o valor de clock atual. (ACESSADO EXCLUSIVAMENTE POR UM LIDER)'''
    content = request.json
    clock.insertTime(content['nodeId'], content['time'])
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

def send_clock_update(clock):
    '''Envia o estado atual do relógio para os outros nós.'''
    msg = {
        "nodeId": clock.id,
        "time": clock.getTime()
    }
    for node, address in config['OtherNodes'].items():
        # Se não for para o próprio nó
        if node != clock.id:
            url = f"http://{address}/"
            try:
                response = requests.post(url, json=msg)
                if response.status_code == 200:
                    print(f"Enviado para o nó {node}.")
                else:
                    print(f"Falha ao enviar para o nó {node}. Status Code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Erro ao enviar tempo para o nó {node}: {e}")




def send_periodically(clock, interval):
    '''Envia o estado atual do relógio para os outros nós periodicamente.'''
    while True:
        send_clock_update(clock)
        time.sleep(interval)  # Aguarda pelo intervalo especificado antes de enviar novamente




# Colocar a thread da rotina eterna
if __name__ == '__main__':
    # Tem uma thread para o menu
    thread_interface_manual = threading.Thread(target=menu, args=[clock])
    thread_interface_manual.daemon = True
    
    thread_clock_run = threading.Thread(target=clock.run)
    thread_clock_run.daemon = True

    # Inicia a thread para enviar atualizações periodicamente
    update_interval = 2  # Intervalo em segundos
    thread_send_updates = threading.Thread(target=send_periodically, args=[clock, update_interval])
    thread_send_updates.daemon = True

    # Iniciando as threads
    thread_interface_manual.start()
    thread_clock_run.start()
    thread_send_updates.start()

    # Levantando a API
    app.run(port=config['port'], host='0.0.0.0')

    # Caso as threads sejam interrompidas
    thread_interface_manual.join()
    thread_clock_run.join()
    thread_send_updates.join()
