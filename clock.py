import socket
import threading
import time

# Configuração do host e das portas
HOST = '127.0.0.1'
PORT = 65431  # Porta única do relógio
PORTS = [65432, 65433]  # Portas dos outros relógios

# Variáveis globais
clock_time = 0.0  # Tempo inicial do relógio
leader = None  # Líder atual
is_leader = False  # Flag para verificar se este relógio é o líder
sockets = {}  # Dicionário para armazenar as conexões de socket
lock = threading.Lock()  # Lock para sincronizar o acesso ao clock_time
stop_event = threading.Event()  # Evento para sinalizar a parada das threads
increment = 0.10  # Valor inicial do incremento

def run_clock():
    """Função que incrementa o tempo do relógio"""
    global clock_time, increment
    while not stop_event.is_set():
        with lock:
            clock_time += increment
        time.sleep(1)  # A cada segundo, incrementa o valor especificado

def display_time():
    """Função que exibe o tempo constantemente"""
    global clock_time, leader
    while not stop_event.is_set():
        with lock:
            print(f"Tempo atual = {clock_time:.2f}, Líder = {leader}")
        time.sleep(1)

def handle_connection(conn):
    """Função que lida com a conexão recebida"""
    global clock_time, leader
    with conn:
        while not stop_event.is_set():
            try:
                data = conn.recv(1024)  # Recebe dados da conexão
                if not data:
                    break
                message = data.decode('utf-8')
                if message.startswith('TIME:'):
                    # Atualiza o clock_time se o tempo recebido for maior
                    remote_time = float(message.split(':')[1])
                    with lock:
                        if remote_time > clock_time:
                            clock_time = remote_time
                elif message.startswith('LEADER:'):
                    # Atualiza o líder
                    leader = int(message.split(':')[1])
            except Exception as e:
                print(f"Erro na conexão: {e}")
                break



def client():
    """Função do cliente que envia o tempo e o líder para outros relógios"""
    global clock_time, leader, is_leader, sockets
    while not stop_event.is_set():
        with lock:
            # Define se este relógio é o líder
            if leader is None or leader == PORT:
                is_leader = True
                leader = PORT
            else:
                is_leader = False
            for p in PORTS:
                try:
                    # Conecta aos outros relógios se ainda não estiver conectado
                    if p not in sockets:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((HOST, p))
                        sockets[p] = s
                    # Envia o tempo atual para o outro relógio
                    sockets[p].sendall(f'TIME:{clock_time}'.encode('utf-8'))
                    # Se for o líder, envia também a informação de liderança
                    if is_leader:
                        sockets[p].sendall(f'LEADER:{PORT}'.encode('utf-8'))
                except (ConnectionRefusedError, BrokenPipeError, OSError) as e:
                    print(f"Erro na conexão com a porta {p}: {e}")
                    if p in sockets:
                        sockets[p].close()
                        del sockets[p]
                    # Se o líder falhar, redefine o líder
                    if leader == p:
                        leader = None
        time.sleep(1)

def menu():
    """Função para o menu de alteração do incremento"""
    global increment
    while not stop_event.is_set():
        print("\nMenu:")
        print("1. Alterar valor do incremento")
        print("2. Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == "1":
            try:
                new_increment = float(input("Digite o novo valor do incremento: "))
                with lock:
                    increment = new_increment
                print(f"Novo valor do incremento definido para {new_increment}.")
            except ValueError:
                print("Por favor, insira um valor numérico válido.")
        elif choice == "2":
            stop_event.set()  # Define o evento para parar todas as threads
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    """Função principal que inicia as threads para o relógio"""
    try:
        threading.Thread(target=run_clock).start()
        threading.Thread(target=server).start()
        threading.Thread(target=client).start()
        threading.Thread(target=display_time).start()
        threading.Thread(target=menu).start()  # Adiciona a thread do menu
    except KeyboardInterrupt:
        stop_event.set()
        print("Encerrando...")

if __name__ == "__main__":
    time.sleep(1)
    main()
