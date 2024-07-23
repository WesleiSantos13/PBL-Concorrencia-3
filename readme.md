# Quando o líder pergunta o tempo do nó
A resposta
{
    "node": 1,
    "time": 14545454
}

# Quando o líder manda mudar o tempo do nó
{
    "node": 1,
    "role": "LEADER",
    "action": "CHANGE_TIME",
    "time" : 118825
}


# Quando alguém convoca uma eleição
{
    "node": 1,
    "role": "CANDIDATE",
    "action": "ELECTION",
    "time": 5615123
}
e recebe 
{
    "node": 1,
    "role": "CANDIDATE",
    "action": "ELECTION",
    "time": 5615123
}
# Quando alguém avisa que venceu eleição
{
    "node": 1,
    "role": "LEADER",
    "action": "WIN_ELECTION"
}

E se eu receber uma eleiçãi enquanto estou fazendo outra??


Para a rotina diaria
    - se sou o lider
        - fico pedindo os horários de cada um após x segundos
        - Se MEU_HORARIO - HORARIO_DELE > LIMITE, mando ele adiantar seu relógio em 1/4 da diferença
        - Se MEU_HORARIO - HORARIO_DELE <= LIMITE, mando ele receber meu horario
        - Se o horário dele é maior que o meu, convoco uma nova eleição********
    - Se não sou o líder, fico observando as portas para encaminhar as solicitações que recebo (tomar a ação certa)
        - Se recebi uma solicitação para um horario menor que o meu, convoco uma nova eleição********

Se eu morri detecto que talvez eu tenha morrido, tento uma nova eleição