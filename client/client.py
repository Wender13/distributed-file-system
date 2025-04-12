import socket
import os
import sys

HOST = 'localhost'
PORT = 5001

def send_command(cmd, send_file=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(cmd.encode())

        if send_file:
            with open(send_file, 'rb') as f:
                while chunk := f.read(1024):
                    s.send(chunk)
            return

        data = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
        return data.decode(errors="ignore")

def ls(args):
    path = args[0] if args else ''
    result = send_command(f"LIST {path}")
    print(result)

def rm(args):
    for path in args:
        result = send_command(f"DELETE {path}")
        print(f"{path}: {result}")

def cp(args):
    for filepath in args:
        if not os.path.isfile(filepath):
            print(f"[ERRO] {filepath} nao encontrado.")
            continue
        filename = os.path.basename(filepath)
        print(f"[UPLOAD] Enviando {filename}...")
        send_command(f"UPLOAD {filename}", send_file=filepath)
        print(f"[UPLOAD] {filename} enviado.")

def get(args):
    for path in args:
        result = send_command(f"DOWNLOAD {path}")
        if "ERROR" in result:
            print(f"[ERRO] {result.strip()}")
        else:
            local_name = os.path.basename(path)
            with open(local_name, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"[DOWNLOAD] {local_name} salvo.")

def mkdir(args):
    if not args:
        print("[ERRO] Nome do diretorio nao informado")
        return
    result = send_command(f"MKDIR {args[0]}")
    print(result)

def touch(args):
    if not args:
        print("[ERRO] Nome do arquivo nao informado")
        return
    result = send_command(f"TOUCH {args[0]}")
    print(result)

def shell():
    print("Shell do Sistema de Arquivos Distribuído")
    print("Comandos: ls, rm, cp, get, mkdir, touch, exit")
    while True:
        try:
            cmd = input("➜ ").strip()
            if not cmd:
                continue
            parts = cmd.split()
            action, args = parts[0], parts[1:]

            match action:
                case 'ls': ls(args)
                case 'rm': rm(args)
                case 'cp': cp(args)
                case 'get': get(args)
                case 'mkdir': mkdir(args)
                case 'touch': touch(args)
                case 'exit': print("Saindo..."); break
                case _: print("Comando invalido.")
        except KeyboardInterrupt:
            print("\nSaindo...")
            break

if __name__ == "__main__":
    shell()