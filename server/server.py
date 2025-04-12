import socket
import os
import threading

HOST = 'localhost'
PORT = 5001
SERVER_DIR = os.path.join(os.path.dirname(__file__), 'storage')

os.makedirs(SERVER_DIR, exist_ok=True)

def handle_client(conn):
    try:
        request = conn.recv(1024).decode().strip()
        if not request:
            conn.close()
            return

        parts = request.split()
        command = parts[0]

        if command == 'LIST':
            path = os.path.join(SERVER_DIR, *parts[1:]) if len(parts) > 1 else SERVER_DIR
            if os.path.isdir(path):
                files = os.listdir(path)
                conn.send("\n".join(files).encode() if files else b"[vazio]")
            else:
                conn.send(b"Diretorio nao encontrado")

        elif command == 'DELETE':
            target = os.path.join(SERVER_DIR, *parts[1:])
            if os.path.isfile(target):
                os.remove(target)
                conn.send(b"Arquivo removido")
            elif os.path.isdir(target):
                import shutil
                shutil.rmtree(target)
                conn.send(b"Diretorio removido com sucesso")
            else:
                conn.send(b"Nenhum arquivo ou diretorio encontrado")


        elif command == 'UPLOAD':
            filename = parts[1]
            filepath = os.path.join(SERVER_DIR, filename)
            conn.send(b"OK")
            with open(filepath, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)

        elif command == 'DOWNLOAD':
            target = os.path.join(SERVER_DIR, *parts[1:])
            if os.path.isfile(target):
                with open(target, 'rb') as f:
                    while chunk := f.read(1024):
                        conn.send(chunk)
            elif os.path.isdir(target):
                files = os.listdir(target)
                if not files:
                    conn.send(b"ERROR: Diretorio vazio")
                else:
                    for fname in files:
                        conn.send(f"\n--- {fname} ---\n".encode())
                        with open(os.path.join(target, fname), 'rb') as f:
                            conn.send(f.read())
            else:
                conn.send(b"ERROR: Arquivo ou diretorio nao encontrado")

        elif command == 'MKDIR':
            path = os.path.join(SERVER_DIR, *parts[1:])
            os.makedirs(path, exist_ok=True)
            conn.send(b"Diretorio criado")

        elif command == 'TOUCH':
            path = os.path.join(SERVER_DIR, *parts[1:])
            open(path, 'a').close()
            conn.send(b"Arquivo vazio criado")

        else:
            conn.send(b"Comando invalido")
    except Exception as e:
        conn.send(f"Erro no servidor: {e}".encode())
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVIDOR] Online em {HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    main()