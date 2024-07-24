from flask import Flask, request, jsonify

import requests

from datetime import datetime, timedelta

import threading

from infra.config import config

from model.Node import Clock
from model.Election import Election

## ======= Bloco para instânciação de objetos necessários ======= ##
app = Flask(__name__)

clock = Clock(config['drift'], 0)
election = Election(clock)



### ================================================ BLOCO PARA ROTAS ==================================================== ###
@app.route('/', methods=['GET'])
def currentTime():
    '''Fornece o valor de clock atual. (ACESSADO EXCLUSIVAMENTE POR UM LIDER)'''
    clock.setLeaderLastContact(datetime.now()) # já  salvo como último contato do líder
    msg = {
    "node": clock.id,
    "time": clock.time 
    }
    return jsonify({"mensagem": msg}), 200


@app.route('/updateTime', methods=['PATCH'])
def forced_time_update():
    '''Atualiza o tempo do relógio. (ACESSADO EXCLUSIVAMENTE POR UM LIDER)'''
    clock.setLeaderLastContact(datetime.now()) # já  salvo como último contato do líder
    # Obtem o body da requisição
    content = request.json
    # Se a mensagem veio de quem eu enxergo como líder
    if content['node'] == clock.getLeader():
        new_time = content['time']
        # Atualiza o tempo
        clock.setTime(new_time)
        return jsonify({"msg": "ok"}), 200
    # Se não veio do líder
    else:
        return jsonify({"msg": "__"}), 400



@app.route('/compare_election', methods=['POST'])
def compare_votes():
    '''Utilizado como peça de uma eleição para comparação de vencedor dois a dois'''
    # Obtem o body da requisição
    content = request.json
    if content['time'] > clock.time:
        # Quem receber este deverá continuar a eleição
        return jsonify({"msg": "you_win"}), 200
    else:
        # ?????????????????????????????????????????????????????????????????????????
        # Quem receber este deverá encerra eleição e aguardar que seja dito quem é o líder, eu devo prosseguir com a eleição (exceto para esse nó que eu já sei que sou maior) ???????
        return jsonify({"msg": "i_win"}), 200
        

@app.route('/define_election', methods=['POST'])
def result_election():
    '''Utilizado como peça de uma eleição para informar quem é o vencedor'''
    # Obtem o body da requisição
    content = request.json
    clock.setLeader(content['node']) # Salva o id do nó vencedor
    return jsonify({"msg": "ok"}), 200




### ================================================ BLOCO PARA FUNÇÕES DE THREADS ==================================================== ###
def menu(clock: Clock):
    """Função para o menu de alteração do incremento.
    Será executado como uma thread"""

    while True:
        print("\nMenu:")
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


def verifyContactLeader( clock: Clock, election: Election):
    ''' Este método só faz verificar se o líder caiu para poder iniciar uma eleição'''
    while True:
        # Se eu já passei do tempo para esperar contato do líder e eu não sou o líder. Ou se o líder é vazio (acontece quando inicia o nó)
        if ( clock.leaderIsDead(datetime.now()) ) and  (not clock.imLeader()):
            # Inicia a eleição
            election.initElection()



def leaderRoutine(clock:Clock, election: Election):
    withou_contact = 0
    len_nodes = len(config['OtherNodes'].keys())
    doElection = False #Se devo começar uma eleição

    while True:
        # Se eu que sou o líder
        if clock.imLeader():
            # Vou sair pedindo para todos os nós seus tempos
            for node in config['OtherNodes'].keys(): # ["1", "2", "3"]
                # Se não for pro próprio nó
                if node != clock.id:
                    try:
                        response = requests.get(f"http://{config['OtherNodes'][node]}:{config['port']}/", timeout=1)
                        # Se o tempo dele for maior que o meu, inicio uma eleição
                        if response['time'] > clock.getTime():
                            doElection = True
                            break
                        else:
                            differ = clock.getTime() - response['time']
                            # verifico se está muito defasado, se estiver eu mando atualizar com metade da defasagem. caso contrário eu mando o meu horário
                            if differ > config['LIMIT']:
                                new_time = clock.getTime() + differ/2
                            # 
                            payload = {
                                "node": clock.id,
                                "role": "LEADER",
                                "action": "CHANGE_TIME",
                                "time" : new_time
                            }
                            try:
                                requests.patch(f"http://{config['OtherNodes'][node]}:{config['port']}/updateTime", json=payload, timeout=1)
                            except: ### ===============OQ FAZER AQUI????????????????????????????????????????????????????????????????????????????
                                pass
                    except:
                        withou_contact = withou_contact +1 # Se eu não tive contato com o nó, digo que não consegui contactar mais um
            # Se não consegui me conectar com nenhum nó ou recebi um tempo maior que o meu, inicio a eleição
            if (withou_contact == len_nodes) or (doElection):
                election.initElection()


# Colocar a thread da rotina eterna
if __name__ == '__main__':
    # Tem uma thread para o menu
    thread_interface_manual = threading.Thread(target=menu, args=[clock])
    thread_interface_manual.daemon = True
    # Tem a thread que verifica se o líder caiu
    thread_verify_contactLeader = threading.Thread(target=verifyContactLeader, args=[clock, election])
    thread_verify_contactLeader.daemon = True
    # Tem thread que gera a rotina do líder 
    thread_leader_routine = threading.Thread(target=leaderRoutine, args=[clock, election])
    thread_leader_routine.daemon = True
    
    # Iniciando as threads
    thread_interface_manual.start()
    thread_verify_contactLeader.start()
    thread_leader_routine.start()
    # Levantando a API
    app.run(port=config['port'], host='0.0.0.0')
    # Caso as threads sejam interrompidas
    thread_interface_manual.join()
    thread_verify_contactLeader.join()
    thread_leader_routine.join()


# Colocar as thread do menu
# Colocar as thread que verifica se o líder caiu
# Colocar a thread de rotina diária de um líder (ficar sempre pedindo)

# referencias
# https://www.cin.ufpe.br/~avmm/arquivos/provas%20software/resuminho3.pdf
# https://www-di.inf.puc-rio.br/~endler/courses/DA/transp/Election.pdf