from flask import Flask, request, jsonify
from flask_caching import Cache

from datetime import datetime, timedelta

from infra.config import config

from model.Node import Clock
from model.Election import Election

## ======= Bloco para instânciação de objetos necessários ======= ##
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Configuração básica de cache

clock = Clock(config['drift'], 0)
# election = Election(clock)



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
    # Obtem o body da requisição
    content = request.json
    new_time = content['time']
    # Atualiza o tempo
    clock.setTime(new_time)
    return jsonify({"msg": "ok"}), 200



@app.route('/compare_election', methods=['POST'])
def post_mensagem():
    '''Utilizado como peça de uma eleição para comparação de vencedor dois a dois'''
    # Obtem o body da requisição
    content = request.json
    if content['time'] > clock.time:
        return jsonify({"msg": "you_win"}), 200
    else:
        return jsonify({"msg": "i_win"}), 200
        

@app.route('/define_election', methods=['POST'])
def post_mensagem(topic: str):
    '''Utilizado como peça de uma eleição para informar que sou um vencedor'''
    # Se não for um tópico permitido, já encerra e retorna o status
    if not topic.startswith('command'):
        return jsonify({"erro": "Você não tem permissão para este topico"}), 403
    # Obtem o body da requisição
    conteudo = request.json
    # Verifica se a solicitação contém um JSON
    if conteudo is None:
        return jsonify({"erro": "A solicitação deve conter um JSON"}), 400
    confirm = broker.publish_message(topic, conteudo['message'], '')
    status = 201
    msg = "Mensagem publicada com sucesso"
    if not confirm:
        status = 200
        msg = "Recebemos a solicitação, mas não conseguimos processar"
    return jsonify({"mensagem": msg}), status




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


# Colocar a thread da rotina eterna
if __name__ == '__main__':
    app.run(port=config['port'], host='0.0.0.0')