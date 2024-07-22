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



from infra.config import config

class Election:
# {
#     "node": 1,
#     "role": "LEADER",
#     "action": "ELECTION"
# }
    def initElection(self, nodeId):
        iAmLeader = False
        #### FASE EM QUE ESTOU VERIFICANDO SE POSSO SER O LÍDER #### PERGUNTO A TODOS OS NÓS
        for node in config['OtherNodes'].keys(): # ["1", "2", "3"]
            # Se não for pro próprio nó
            if node != nodeId:
                # Manda a mensagem de eleição
                # Aguarda a resposta do nó
                # Se não recebi nada ou se deu erro na conexão ou se eu recebi a resposta e tenho o tempo maior, eu passo pro próximo nó (estou acreditando que sou o líder)
                # Caso contrário, encerro o processo pois já sei que não sou eu
                pass
        
        #### FASE EM QUE JÁ SEI QUE SOU O LÍDER ####
        # Se cheguei até aqui com True, eu inicio o processo de avisar que sou o líder
        if iAmLeader == True:
            # Inicia o processo de avisar que sou o líder
            pass
        