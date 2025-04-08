import socket
import os

HOST = 'localhost'
PORT = 5001

def upload(filepath):
    if not os.path.exists(filepath):
        print(f"[ERRO] Arquivo '{filepath}' não existe.")
        return

    filename = os.path.basename(filepath)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(f"UPLOAD {filename}".encode())
        ack = s.recv(1024).decode()

        if ack != "OK":
            print("Servidor recusou upload.")
            return

        with open(filepath, 'rb') as f:
            while chunk := f.read(1024):
                s.send(chunk)

    print(f"[UPLOAD] Arquivo '{filename}' enviado com sucesso.")

def download(filename, save_as=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(f"DOWNLOAD {filename}".encode())
        data = s.recv(1024)

        if data.startswith(b"ERROR"):
            print(data.decode())
            return

        if save_as is None:
            save_as = filename

        with open(save_as, 'wb') as f:
            f.write(data)
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)

        print(f"[DOWNLOAD] Arquivo '{filename}' salvo como '{save_as}'")

def delete(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(f"DELETE {filename}".encode())
        response = s.recv(1024).decode()
        print(f"[DELETE] {response}")

def list_files():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send("LIST".encode())
        response = s.recv(4096).decode()
        print("[LISTA DE ARQUIVOS NO SERVIDOR]")
        print(response)

def find_files_in_home():
    home = os.path.expanduser("~")
    print(f"\n[ARQUIVOS ENCONTRADOS EM {home}]")
    arquivos = []
    for root, dirs, files in os.walk(home):
        for file in files:
            full_path = os.path.join(root, file)
            arquivos.append(full_path)
    return arquivos

def main_menu():
    while True:
        print("\n========= MENU =========")
        print("1. Listar arquivos no servidor")
        print("2. Enviar arquivo para o servidor")
        print("3. Baixar arquivo do servidor")
        print("4. Remover arquivo do servidor")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            list_files()

        elif opcao == "2":
            arquivos = find_files_in_home()
            for i, path in enumerate(arquivos[:20]):  # Limite visual inicial
                print(f"{i+1}. {path}")
            if len(arquivos) > 20:
                print("... (mais arquivos ocultos)")
            escolha = input("Digite o número do arquivo para enviar (ou caminho completo): ")

            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(arquivos):
                    upload(arquivos[idx])
                else:
                    print("Índice inválido.")
            except ValueError:
                if os.path.isfile(escolha):
                    upload(escolha)
                else:
                    print("Caminho inválido.")

        elif opcao == "3":
            nome = input("Digite o nome do arquivo para baixar: ")
            salvar = input("Salvar como (pressione ENTER para manter o nome original): ")
            download(nome, salvar if salvar else None)

        elif opcao == "4":
            nome = input("Digite o nome do arquivo para remover do servidor: ")
            delete(nome)

        elif opcao == "0":
            print("Encerrando o cliente.")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main_menu()