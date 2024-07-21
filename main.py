from model.Node import Clock
from infra.config import config

# ======================================= BLOCO DE DEFINIÇÃO DE THREADS ========================================= #
# Tem uma thread para o menu
# Tem uma thread para receber algo do tcp
# Tem um pool de threads que servem para processar algo e responder




# ======================================= BLOCO PARA INICIAR O PROCESSO PRINCIPAL ========================================= #
if __name__ == "__main__":
    relogio = Clock(config['drift'], 0)


# A cada x segundos eu faço uma rodada pedindo todos os relógios
# Eu escolho o relógio mais adiantado para ser minha referência
# Se eu sou o mais adiantado