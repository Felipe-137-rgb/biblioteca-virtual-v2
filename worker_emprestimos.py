import threading
import time
import requests

API_URL = "http://127.0.0.1:8000/livros"

# Lock para garantir segurança ao manipular o estoque concorrentemente (evita Race Condition)
trava_estoque = threading.Lock()

# Lista expandida com vários alunos fazendo pedidos simultâneos
fila_pedidos = [
    {"aluno": "Felipe", "livro_id": 1},
    {"aluno": "Lucas", "livro_id": 2},
    {"aluno": "Mariana", "livro_id": 1},
    {"aluno": "Ana", "livro_id": 3},
    {"aluno": "Carlos", "livro_id": 1},
    {"aluno": "Beatriz", "livro_id": 2},
    {"aluno": "João", "livro_id": 3},
    {"aluno": "Camila", "livro_id": 1}
]

def processar_emprestimo(pedido):
    aluno = pedido["aluno"]
    livro_id = pedido["livro_id"]
    
    print(f"[Thread-{aluno}] Iniciando processamento do empréstimo do livro ID {livro_id}...")
    time.sleep(1.5)  # Simula tempo de processamento/validação

    # Região crítica protegida por Lock
    with trava_estoque:
        try:
            # 1. Consulta o livro na API (GET)
            resposta = requests.get(f"{API_URL}/{livro_id}")
            if resposta.status_code != 200:
                print(f"[Thread-{aluno}] Erro: Livro ID {livro_id} não encontrado.")
                return

            livro = resposta.json()

            # 2. Verifica disponibilidade e dá baixa no estoque (PUT)
            if livro["quantidade_disponivel"] > 0:
                livro["quantidade_disponivel"] -= 1
                requests.put(f"{API_URL}/{livro_id}", json=livro)
                print(f"[Thread-{aluno}] SUCESSO! Empréstimo de '{livro['titulo']}' confirmado. Restam: {livro['quantidade_disponivel']}")
            else:
                print(f"[Thread-{aluno}] NEGADO! '{livro['titulo']}' está sem estoque.")

        except requests.exceptions.ConnectionError:
            print(f"[Thread-{aluno}] Falha de conexão com a API.")

def iniciar_processamento_concorrente():
    print(f"=== INICIANDO PROCESSAMENTO SIMULTÂNEO DE {len(fila_pedidos)} EMPRÉSTIMOS ===\n")
    threads = []

    # Criando uma Thread dedicada para cada aluno da lista
    for pedido in fila_pedidos:
        t = threading.Thread(target=processar_emprestimo, args=(pedido,))
        threads.append(t)
        t.start() # Inicia a execução concorrente da Thread

    # Aguarda todas as threads terminarem o ciclo
    for t in threads:
        t.join()

    print("\n=== TODOS OS EMPRÉSTIMOS FORAM PROCESSADOS ===")

if __name__ == "__main__":
    iniciar_processamento_concorrente()