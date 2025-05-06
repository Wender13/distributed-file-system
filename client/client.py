import xmlrpc.client
import os

HOST = "http://192.168.83.18:5001/"  # IP do servidor (mude conforme necessário)
proxy = xmlrpc.client.ServerProxy(HOST, allow_none=True)

def ls(args):
    path = args[0] if args else ""
    try:
        arquivos = proxy.listar_arquivos(path)
        print("\n".join(arquivos) if arquivos else "[vazio]")
    except Exception as e:
        print("[ERRO]", e)

def rm(args):
    for path in args:
        try:
            print(f"{path}: {proxy.remover(path)}")
        except Exception as e:
            print("[ERRO]", e)

def cp(args):
    for filepath in args:
        if not os.path.isfile(filepath):
            print(f"[ERRO] {filepath} nao encontrado.")
            continue
        nome = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            dados = f.read()
        try:
            print(f"[UPLOAD] Enviando {nome}...")
            print(proxy.upload(nome, xmlrpc.client.Binary(dados)))
        except Exception as e:
            print("[ERRO]", e)

def get(args):
    for nome in args:
        try:
            dados = proxy.download(nome)
            if isinstance(dados, xmlrpc.client.Binary):
                with open(os.path.basename(nome), "wb") as f:
                    f.write(dados.data)
                print(f"[DOWNLOAD] {nome} salvo.")
            else:
                print(f"[ERRO] {dados}")
        except Exception as e:
            print("[ERRO]", e)

def mkdir(args):
    if not args:
        print("[ERRO] Nome do diretorio nao informado")
        return
    try:
        print(proxy.criar_diretorio(args[0]))
    except Exception as e:
        print("[ERRO]", e)

def touch(args):
    if not args:
        print("[ERRO] Nome do arquivo nao informado")
        return
    try:
        print(proxy.criar_arquivo(args[0]))
    except Exception as e:
        print("[ERRO]", e)

def cat(args):
    if not args:
        print("[ERRO] Nome do arquivo nao informado")
        return
    try:
        print("\n📄 Conteúdo do arquivo:\n")
        print(proxy.cat_file(args[0]))
    except Exception as e:
        print("[ERRO]", e)

def echo(args):
    if not args:
        print("[ERRO] Nome do arquivo não informado")
        return
    filename = args[0]
    text = input("Digite o texto a ser adicionado: ")
    try:
        resposta = proxy.echo(filename, text)
        print(resposta)
    except Exception as e:
        print("[ERRO]", e)

def shell():
    print("Shell RPC do Sistema de Arquivos Distribuído")
    print("Comandos: ls, cat, rm, cp, get, mkdir, touch, echo, help, exit")
    while True:
        try:
            cmd = input("➜ ").strip()
            if not cmd:
                continue
            parts = cmd.split()
            action, args = parts[0], parts[1:]

            match action:
                case "ls": ls(args)
                case "rm": rm(args)
                case "cp": cp(args)
                case "get": get(args)
                case "mkdir": mkdir(args)
                case "touch": touch(args)
                case "cat": cat(args)
                case "help": print("Comandos: ls, cat, rm, cp, get, mkdir, touch, help, exit")
                case "echo": echo(args)
                case "exit": print("Saindo..."); break
                case _: print("Comando invalido.")
        except KeyboardInterrupt:
            print("\nSaindo...")
            break

if __name__ == "__main__":
    shell()