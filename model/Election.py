# EM UMA ELEIÇÃO SÓ RESPONDE SE SEU TEMPO FOR MAIOR

# Se eu recebi uma eleição, eu convoco outra, a menos que já tenha convocado uma.
    # Se venci a aleiição, innformo a todo mundo que eu sou o novo líder

# Se não sou o líder
    # Se percebi que o líder está fora de hora ou caiu, inicio uma votação
        # Se ninguém responder, viro o líder
        # Se alguém responder, analiso para ver se o tempo dele é maior que o meu e ele vira o líder

# Se sou o líder
    # Se percebi que não consigo perguntar, deixo de ser o líder

# A mensagem de sinncronização que  o líder manda para todas é uma do tipo falando a hora que o mesmo deve sincronizar
    # Se o tempop de um nó é maior que a diferença permitida, então eu atualizo o tempo em 1/4 doq precisa para chegar no meu Int(DELE + (MEU-DELE)/4)


from model.Node import Clock
from infra.config import config
import logging

class Election:

    def __init__(self, clock: Clock) -> None:
        self.clock = clock
        self.logging= logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        # print(f"Em eleição o drif foi {self.clock.getDrift()}")

    def sendMessage(self, payload: dict, destination_ip: str, destination_port: str, close_conn: bool):
        pass
    
    def receiveMessage(self):
        pass
    
    def initElection(self):
        logging.info(f'START ELECTION - Uma eleição foi iniciada')
        iAmLeader = False
        msg = {
            "node": self.clock.id,
            "role": "CANDIDATE",
            "action": "ELECTION",
            "time": self.clock.time
        }
        #### FASE EM QUE ESTOU VERIFICANDO SE POSSO SER O LÍDER #### PERGUNTO A TODOS OS NÓS
        for node in config['OtherNodes'].keys(): # ["1", "2", "3"]
            # Se não for pro próprio nó
            if node != self.clock.id:
                logging.info(f'ELECTION - Irei testar votos com {node}')
                # Manda a mensagem de eleição e Aguarda a resposta do nó
                msg["time"] = self.clock.time # Altero o tempo para cada par de verificação
                res = self.sendMessage(msg, config["OtherNodes"][node], config["port"])
                # Se não recebi nada ou se deu erro na conexão ou se eu recebi a resposta e tenho o tempo maior, eu passo pro próximo nó (estou acreditando que sou o líder)
                if res == False:
                    logging.info(f'ELECTION - Venci {node}')
                    iAmLeader = True
                    continue
                # Caso contrário, encerro o processo pois já sei que não sou eu
                else:
                    logging.info(f'ELECTION - Venci {node}')
                    iAmLeader = False
                    break
        
        #### FASE EM QUE JÁ SEI QUE SOU O LÍDER ####
        # Se cheguei até aqui com True, eu inicio o processo de avisar que sou o líder
        if iAmLeader == True:
            self.reorganizing()
                
    
    def reorganizing(self):
        msg =   {
                "node": self.clock.id,
                "role": "LEADER",
                "action": "WIN_ELECTION"
                }
        ## SETO NO MEU PROPRIO NÓ QUE EU SOU O LíDER
        self.clock.leader = self.clock.id
        # Inicia o processo de avisar que sou o líder
        for node in config['OtherNodes'].keys(): # ["1", "2", "3"]
            # Se não for pro próprio nó
            if node != self.clock.id:
                self.sendMessage(msg, config["OtherNodes"][node], config["port"])
        