import socket
import os
import threading

HOST = '0.0.0.0'
PORT = 5001
FILES_DIR = './files'

os.makedirs(FILES_DIR, exist_ok=True)

def handle_client(conn, addr):
    print(f"[+] Conexão de {addr}")

    try:
        command = conn.recv(1024).decode().strip()

        if command.startswith("UPLOAD"):
            _, filename = command.split(maxsplit=1)
            filepath = os.path.join(FILES_DIR, filename)

            conn.send("OK".encode())  # Confirma que vai começar a receber o arquivo

            with open(filepath, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)

            print(f"[+] Arquivo {filename} recebido")

        elif command.startswith("DOWNLOAD"):
            _, filename = command.split(maxsplit=1)
            filepath = os.path.join(FILES_DIR, filename)

            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    conn.sendfile(f)
                print(f"[+] Arquivo {filename} enviado")
            else:
                conn.send("ERROR: Arquivo não encontrado".encode())

        elif command.startswith("DELETE"):
            _, filename = command.split(maxsplit=1)
            filepath = os.path.join(FILES_DIR, filename)

            if os.path.exists(filepath):
                os.remove(filepath)
                conn.send("Arquivo removido com sucesso.".encode())
                print(f"[-] Arquivo {filename} removido")
            else:
                conn.send("ERROR: Arquivo não encontrado".encode())

        elif command.strip() == "LIST":
            files = os.listdir(FILES_DIR)
            response = "\n".join(files) if files else "(vazio)"
            conn.send(response.encode())

    except Exception as e:
        print(f"[ERRO] {e}")
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVIDOR] Aguardando conexões em {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()