import xmlrpc.client
import os

HOST = "http://localhost:5001/"  # IP do servidor (mude conforme necessário)
proxy = xmlrpc.client.ServerProxy(HOST, allow_none=True)

CLIENTE_HOME_DIR = os.path.expanduser("~")

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
    if len(args) != 2:
        print("[ERRO] Uso: cp origem destino")
        return

    origem, destino = args

    def parse_path(path, is_remote):
        if path.startswith("remote:"):
            subpath = path[7:]  # remove "remote:"
            return subpath if subpath else ""
        elif path.startswith("local:"):
            subpath = path[6:]  # remove "local:"
            return os.path.join(CLIENTE_HOME_DIR, subpath)
        return path  # caminho completo

    if origem.startswith("remote:"):
        # DOWNLOAD
        remote_path = parse_path(origem, is_remote=True)
        local_path = parse_path(destino, is_remote=False)

        try:
            dados = proxy.download(remote_path)
            if isinstance(dados, xmlrpc.client.Binary):
                # Trata "local:" como diretório home
                if local_path == "local:" or local_path == "local":
                    local_path = os.path.expanduser("~")

                # Se local_path for um diretório ou terminar com /, adiciona o nome do arquivo
                if os.path.isdir(local_path) or local_path.endswith(os.sep):
                    local_path = os.path.join(local_path, os.path.basename(remote_path))

                # Garante que diretórios intermediários existam
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                with open(local_path, "wb") as f:
                    f.write(dados.data)
                print(f"[DOWNLOAD] {remote_path} -> {local_path}")
            else:
                print(f"[ERRO] {dados}")
        except Exception as e:
            print("[ERRO]", e)

    else:
        # UPLOAD
        local_path = parse_path(origem, is_remote=False)
        remote_path = parse_path(destino, is_remote=True)

        if not os.path.exists(local_path):
            print(f"[ERRO] Caminho '{local_path}' não existe.")
            return
        if os.path.isdir(local_path):
            print(f"[ERRO] '{local_path}' é um diretório, não um arquivo.")
            return

        # Se o destino termina com '/', trate como diretório remoto
        if remote_path.endswith("/"):
            try:
                proxy.criar_diretorio(remote_path)  # Cria se não existir (deve ser implementado de forma idempotente no servidor)
            except Exception:
                pass  # Ignora erro se já existir

        nome_arquivo = os.path.basename(local_path)
        remote_path = os.path.join(remote_path, nome_arquivo)

        with open(local_path, "rb") as f:
            dados = f.read()
        try:
            print(f"[UPLOAD] Enviando {local_path} para remote:{remote_path}...")
            print(proxy.upload(remote_path, xmlrpc.client.Binary(dados)))
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

def help(args):
    comandos = {
        "ls": "ls [CAMINHO]\n  Lista arquivos e pastas do diretório remoto. Exemplo: ls ou ls pasta/",
        "rm": "rm CAMINHO1 CAMINHO2 ...\n  Remove um ou mais arquivos/diretórios remotos. Exemplo: rm arquivo.txt pasta/arquivo2.txt",
        "cp": (
            "cp ORIGEM DESTINO\n"
            "  Copia arquivos entre cliente e servidor.\n"
            "  Upload: cp local:arquivo.txt remote: [vai para HOME remota]\n"
            "  Download: cp remote:arquivo.txt local: [vai para HOME local]\n"
            "  Usa prefixos 'local:' e 'remote:' para indicar a origem e o destino."
        ),
        "mkdir": "mkdir NOME_DO_DIRETORIO\n  Cria um novo diretório remoto. Exemplo: mkdir nova_pasta",
        "touch": "touch NOME_DO_ARQUIVO\n  Cria um novo arquivo remoto. Exemplo: touch novo.txt",
        "cat": "cat NOME_DO_ARQUIVO\n  Exibe o conteúdo de um arquivo remoto. Exemplo: cat texto.txt",
        "echo": "echo NOME_DO_ARQUIVO\n  Solicita texto para adicionar ao arquivo remoto. Exemplo: echo notas.txt",
        "exit": "exit\n  Encerra o shell.",
        "help": "help [COMANDO]\n  Mostra ajuda para todos os comandos ou apenas para o comando informado.",
    }

    if not args:
        print("Comandos disponíveis:\n")
        for cmd in sorted(comandos.keys()):
            print(f"- {cmd}")
        print("\nUse 'help COMANDO' para ver detalhes sobre um comando específico.")
    elif len(args) == 1:
        cmd = args[0]
        if cmd in comandos:
            print(f"\n📘 Ajuda para '{cmd}':\n{comandos[cmd]}")
        else:
            print(f"[ERRO] Comando '{cmd}' não reconhecido.")
    else:
        print("[ERRO] Use no máximo um argumento. Exemplo: help cp")



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
                case "mkdir": mkdir(args)
                case "touch": touch(args)
                case "cat": cat(args)
                case "help": help(args)
                case "echo": echo(args)
                case "exit": print("Saindo..."); break
                case _: print("Comando invalido.")
        except KeyboardInterrupt:
            print("\nSaindo...")
            break

if __name__ == "__main__":
    shell()